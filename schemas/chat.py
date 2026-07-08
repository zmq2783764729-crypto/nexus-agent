from pydantic import BaseModel, Field

#定义聊天数据格式(给后端的数据要这样：)
class ChatRequest(BaseModel):
    session_id: int | None = Field(default=None, description="会话 ID，不传则创建新会话")
    message: str = Field(min_length=1, description="用户输入内容")


#定义后端要返回什么格式(给前端的数据要这样:)
class ChatResponse(BaseModel):
    session_id: int = Field(description="会话 ID")
    task_id: int = Field(description="本次 Agent 执行任务 ID")
    answer: str = Field(description="Agent 最终回答")
    steps: list[str] = Field(default_factory=list, description="Agent 执行步骤")