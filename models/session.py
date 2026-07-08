from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.time import beijing_now
from db.base import Base

#会话表    表示一次聊天会话    一个session 对应 多个 message
class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)   #会话ID
    title: Mapped[str | None] = mapped_column(String(100), nullable=True)   #标题
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)    #摘要

    created_at: Mapped[datetime] = mapped_column(DateTime, default=beijing_now) #创建时间
    updated_at: Mapped[datetime] = mapped_column(                   #更新时间
        DateTime,
        default=beijing_now,
        onupdate=beijing_now,
    )