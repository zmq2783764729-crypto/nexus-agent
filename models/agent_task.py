from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.time import beijing_now
from db.base import Base

#任务执行表  保存每一次 Agent 的完整执行记录（识别意图，判断是否需要工具，选择 calculator 工具，执行工具，生成最终答案）
class AgentTask(Base):
    __tablename__ = "agent_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)   #任务ID
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), index=True)  #会话ID

    user_input: Mapped[str] = mapped_column(Text)   #用户原始输入
    status: Mapped[str] = mapped_column(String(20), default="success")  #执行状态(success/failed/running)
    steps: Mapped[str | None] = mapped_column(Text, nullable=True)  #执行步骤
    final_answer: Mapped[str | None] = mapped_column(Text, nullable=True)   #最终回答

    created_at: Mapped[datetime] = mapped_column(DateTime, default=beijing_now) #创建时间