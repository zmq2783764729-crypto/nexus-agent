from langchain_core.tools import BaseTool

from tools.calculator import calculator

#当前系统有哪些工具
TOOLS: list[BaseTool] = [
    calculator,
]

#把工具列表变成字典，方便通过名字查工具。
TOOL_MAP: dict[str, BaseTool] = {
    tool.name: tool for tool in TOOLS
}

#根据名字 获取工具
def get_tool(name: str) -> BaseTool:
    if name not in TOOL_MAP:
        raise ValueError(f"工具不存在: {name}")
    return TOOL_MAP[name]