from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.time import beijing_now
from db.base import Base


#消息表 表示一次聊天会话
class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)   #消息ID
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), index=True)  #会话ID

    role: Mapped[str] = mapped_column(String(20))  #消息角色
    content: Mapped[str] = mapped_column(Text)  #消息内容

    created_at: Mapped[datetime] = mapped_column(DateTime, default=beijing_now) #创建时间