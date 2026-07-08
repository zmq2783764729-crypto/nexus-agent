from typing import Literal

from langgraph.graph import END

from agent.state import AgentState

#条件路由节点 判断需不需要调用工具
def should_continue(state: AgentState) -> Literal["tool_node", "__end__"]:
    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):   #判断模型最后一条消息里有没有工具调用请求。
        return "tool_node"

    return END