from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage

from agent.state import AgentState
from core.config import settings
from tools.registry import TOOLS


model = init_chat_model(settings.llm_model, temperature=0)
model_with_tools = model.bind_tools(TOOLS)


SYSTEM_PROMPT = """
你是 NexusAgent Core，一个可以使用工具完成任务的智能体。
如果用户问题需要计算、查询或外部能力，请优先调用合适的工具。
如果不需要工具，直接回答。
"""

#定义大模型分析节点:
def llm_node(state: AgentState) -> AgentState:
    messages = state["messages"]    #取出当前对话消息列表。里面通常有用户消息、AI 消息、工具消息。
    steps = state.get("steps", [])  #取出执行步骤；如果没有，就用空列表。

    response = model_with_tools.invoke(
        [SystemMessage(content=SYSTEM_PROMPT)] + messages   #调用模型。这里把系统提示词放在最前面，再拼接历史消息。
    )

    return {
        "messages": [response],
        "steps": steps + ["模型分析用户问题"],
    }