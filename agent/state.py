from typing import TypedDict,Any

import Any


#
class AgentState(TypedDict, total=False):#total=T 表示这些字段不是一开始都必须有，一开始可能只有sessionid
    session_id: int | None
    user_message: str       #用户的原始输入

    intent: str         #Agent判断的用户意图
    need_tool: bool     #需要的工具
    tool_name: str | None   #要调用哪个工具
    tool_args: dict[str, Any]  #给工具的内容
    tool_result: str | None #工具输出的内容

    answer: str     #最终给用户的答案
    steps: list[str]    #记录Agent的执行步骤 先识别意图 选择工具  执行工具 生成答案