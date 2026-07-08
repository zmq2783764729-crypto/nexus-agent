from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict, total=False):   #total=T 表示这些字段不是一开始都必须有，一开始可能只有sessionid
    session_id: int | None
    messages: Annotated[list[AnyMessage], add_messages]
    answer: str         #最终给用户的答案
    steps: list[str]    #记录Agent的执行步骤 先识别意图 选择工具  执行工具 生成答案