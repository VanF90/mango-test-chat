import bcrypt
from sqlalchemy.orm import Session
from typing import Optional

from app.api.chat import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    db_user = models.User(
        username=user.username,
        password=hashed_password,
        avatar=user.avatar,
        bio=user.bio,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, user: schemas.UserUpdate, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if user.password is not None:
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
        db_user.password = hashed_password

    if user.username is not None:
        db_user.username = user.username

    if user.avatar is not None:
        db_user.avatar = user.avatar

    if user.bio is not None:
        db_user.bio = user.bio

    db.commit()
    db.refresh(db_user)

    return db_user


def get_chat(db: Session, chat_id: int):
    return db.query(models.Chat).filter(models.Chat.id == chat_id).first()


def get_chat_by_name(db: Session, name: str):
    return db.query(models.Chat).filter(models.Chat.name == name).first()


def get_chats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Chat).offset(skip).limit(limit).all()


def create_chat(db: Session, chat: schemas.ChatCreate):
    db_chat = models.Chat(
        name=chat.name,
        avatar=chat.avatar,
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    return db_chat


def update_chat(db: Session, chat: schemas.ChatUpdate, chat_id: int):
    db_chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()

    if chat.name is not None:
        db_chat.name = chat.name

    if chat.avatar is not None:
        db_chat.avatar = chat.avatar

    db.commit()
    db.refresh(db_chat)

    return db_chat


def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def get_group_by_name(db: Session, name: str):
    return db.query(models.Group).filter(models.Group.name == name).first()


def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()


def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(
        name=group.name,
        avatar=group.avatar,
        users=[get_user(db, user_id) for user_id in group.users],
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    return db_group


def update_group(db: Session, group: schemas.GroupUpdate, group_id: int):
    db_group = db.query(models.Group).filter(models.Group.id == group_id).first()

    if group.name is not None:
        db_group.name = group.name
