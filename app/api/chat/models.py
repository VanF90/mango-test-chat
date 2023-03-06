from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.core.db import Base

chat_users = Table(
    "chat_users",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("chat_id", Integer, ForeignKey("chats.id")),
)

group_users = Table(
    "group_users",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("group_id", Integer, ForeignKey("groups.id")),
)


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = relationship("User", secondary=chat_users, back_populates="chats")
    messages = relationship("Message", back_populates="chat")

    def __repr__(self):
        return f"<Chat {self.name}>"


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = relationship("User", secondary=group_users, back_populates="groups")
    messages = relationship("Message", back_populates="group")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    chat = relationship("Chat", back_populates="messages")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="messages")
    liked_by_users = relationship("User", secondary="message_likes")

    def __repr__(self):
        return f"<Message {self.id}>"


class MessageLike(Base):
    __tablename__ = "message_likes"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    message_id = Column(Integer, ForeignKey("messages.id"), primary_key=True)

    def __repr__(self):
        return f"<Like user_id={self.user_id}, message_id={self.message_id}>"
