import json

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agent.graph import agent_graph
from models.agent_task import AgentTask
from models.message import Message
from models.session import Session
from models.tool_call import ToolCall
from schemas.chat import ChatRequest, ChatResponse

#定义聊天业务函数   db用来读写 MySQL    request是前端传来的聊天请求(包括session_id和message)
async def chat_service(db: AsyncSession, request: ChatRequest) -> ChatResponse: #最终接口返回给前端的数据
    session = await _get_or_create_session(db, request.session_id)

    history_messages = await _load_history_messages(db, session.id)

    user_message = Message(     #创建一条用户消息 ORM 对象
        session_id=session.id,
        role="user",
        content=request.message,
    )
    db.add(user_message)    #把用户消息加入数据库 session。等后面 commit() 时才会真正写入 MySQL。

    task = AgentTask(   #创建一条 Agent 执行任务记录。表示这次用户请求启动了一次 Agent 执行。
        session_id=session.id,
        user_input=request.message,
        status="running",
    )
    db.add(task)    #把 Agent 任务加入数据库 session。

    await db.flush()    #把前面 db.add() 的对象先同步到数据库，但不提交事务。

    graph_result = agent_graph.invoke(  #调用 LangGraph Agent。
        {
            "session_id": session.id,
            "messages": history_messages + [HumanMessage(content=request.message)],
            "steps": [],
        }
    )

    answer = _extract_answer(graph_result)  #从图执行结果里提取最终回答 需要辅助函数找出最终那条 AI 回复
    steps = graph_result.get("steps", [])     #从图执行结果里取执行步骤。

    await _save_tool_calls(db, task.id, graph_result)   #保存工具调用记录

    assistant_message = Message(    #创建一条 assistant 消息。 也就是 Agent 最终回答
        session_id=session.id,
        role="assistant",
        content=answer,
    )
    db.add(assistant_message)   #把 assistant 回复加入数据库 session

    task.status = "success"     #把 Agent 任务状态改成成功
    task.steps = json.dumps(steps, ensure_ascii=False)  #把步骤列表转成 JSON 字符串，保存到数据库
    task.final_answer = answer  #把最终回答保存到任务记录里

    await db.commit()   #提交数据库事务

    return ChatResponse(    #返回接口响应对象
        session_id=session.id,
        task_id=task.id,
        answer=answer,
        steps=steps,
    )

#获取或创建会话    如果前端传了 session_id，就查已有会话。如果没传，就创建新会话。
async def _get_or_create_session(db: AsyncSession, session_id: int | None) -> Session:
    if session_id is not None:
        result = await db.execute(
            select(Session).where(Session.id == session_id)
        )
        session = result.scalar_one_or_none()

        if session is None:
            raise ValueError(f"会话不存在: {session_id}")

        return session

    session = Session(title="新会话")
    db.add(session)
    await db.flush()
    return session

#加载历史消息 从 MySQL 读取这个会话以前的聊天记录，然后转换成 LangChain 消息：
async def _load_history_messages(db: AsyncSession, session_id: int) -> list:
    result = await db.execute(
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.id.asc())
    )

    messages = []

    for item in result.scalars().all():
        if item.role == "user":
            messages.append(HumanMessage(content=item.content))
        elif item.role == "assistant":
            messages.append(AIMessage(content=item.content))

    return messages

#从图执行结果里拿最终回答。
def _extract_answer(graph_result: dict) -> str:
    messages = graph_result["messages"]

    for message in reversed(messages):
        if isinstance(message, AIMessage) and not getattr(message, "tool_calls", None):
            return str(message.content)

    return "没有生成有效回答"

#保存工具调用记录。把 模型请求调用什么工具,工具参数是什么,工具结果是什么 写入tool_calls表
async def _save_tool_calls(
    db: AsyncSession,
    task_id: int,
    graph_result: dict,
) -> None:
    messages = graph_result["messages"]

    tool_call_map = {}

    for message in messages:
        if isinstance(message, AIMessage) and getattr(message, "tool_calls", None):
            for tool_call in message.tool_calls:
                tool_call_map[tool_call["id"]] = tool_call

        if isinstance(message, ToolMessage):
            tool_call = tool_call_map.get(message.tool_call_id)

            db.add(
                ToolCall(
                    task_id=task_id,
                    tool_name=tool_call["name"] if tool_call else "unknown",
                    tool_input=json.dumps(
                        tool_call["args"] if tool_call else {},
                        ensure_ascii=False,
                    ),
                    tool_output=str(message.content),
                    status="success",
                )
            )