from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.time import beijing_now
from db.base import Base

#工具调用表 保存 Agent 调用工具的记录
class ToolCall(Base):
    __tablename__ = "tool_calls"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)   #工具ID
    task_id: Mapped[int] = mapped_column(ForeignKey("agent_tasks.id"), index=True)  #任务ID

    tool_name: Mapped[str] = mapped_column(String(50))  #工具名称
    tool_input: Mapped[str | None] = mapped_column(Text, nullable=True) #工具输入
    tool_output: Mapped[str | None] = mapped_column(Text, nullable=True)    #工具输出
    status: Mapped[str] = mapped_column(String(20), default="success")  #调用状态(success/failed)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)  #错误信息(status failed时)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=beijing_now) #创建时间