from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str
    avatar: Optional[str] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class ChatBase(BaseModel):
    name: str
    avatar: Optional[str] = None


class ChatCreate(ChatBase):
    pass


class ChatUpdate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    messages: List['Message'] = []

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    name: str
    avatar: Optional[str] = None
    users: List[int] = []


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    messages: List['Message'] = []

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    text: str
    image: Optional[str] = None


class MessageCreate(MessageBase):
    chat_id: int
    group_id: Optional[int] = None


class Message(MessageBase):
    id: int
    chat_id: int
    group_id: Optional[int] = None
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Like(BaseModel):
    user_id: int
    message_id: int


class Pinned(BaseModel):
    chat_id: Optional[int] = None
    group_id: Optional[int] = None
    message_id: int
