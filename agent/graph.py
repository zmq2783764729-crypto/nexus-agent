from langgraph.graph import START, StateGraph

from agent.state import AgentState
from nodes.llm_node import llm_node
from nodes.routing import should_continue
from nodes.tool_node import tool_node

#构图函数
def build_agent_graph():
    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("llm_node", llm_node)
    graph_builder.add_node("tool_node", tool_node)

    graph_builder.add_edge(START, "llm_node")

    graph_builder.add_conditional_edges(        #条件判断
        "llm_node",
        should_continue,
        {
            "tool_node": "tool_node",
            "__end__": "__end__",
        },
    )

    graph_builder.add_edge("tool_node", "llm_node")

    return graph_builder.compile()


agent_graph = build_agent_graph()