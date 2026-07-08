from langchain_core.messages import ToolMessage

from agent.state import AgentState
from tools.registry import TOOL_MAP


#定义tool执行节点 返回工具消息。
def tool_node(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]    #取最后一条消息。这里最后一条应该是模型刚刚生成的 AI 消息。
    steps = state.get("steps", [])

    tool_messages = []  #准备一个列表，用来保存所有工具执行结果。

    #遍历模型请求的所有工具调用。模型可能一次请求一个工具，也可能一次请求多个工具。
    for tool_call in last_message.tool_calls:
        tool = TOOL_MAP[tool_call["name"]]
        result = tool.invoke(tool_call["args"])

        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
            )
        )

    return {
        "messages": tool_messages,
        "steps": steps + ["执行工具调用"],
    }