from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import JWTAuthentication, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.api.chat import crud, models, schemas
from app.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Authentication
JWT_SECRET = "secret"
jwt_authentication = JWTAuthentication(secret_key=JWT_SECRET, algorithm="HS256")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/chats/", response_model=schemas.Chat)
def create_chat(chat: schemas.ChatCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(jwt_authentication)):
    if current_user.id not in chat.user_ids:
        raise HTTPException(status_code=400, detail="Current user not in chat participants.")
    return crud.create_chat(db=db, **chat.dict())


@app.post("/groups/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db),
                 current_user: models.User = Depends(jwt_authentication)):
    if current_user.id not in group.user_ids:
        raise HTTPException(status_code=400, detail="Current user not in group participants.")
    return crud.create_group(db=db, **group.dict())


@app.post("/chats/{chat_id}/messages/", response_model=schemas.Message)
def create_message(chat_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(jwt_authentication)):
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if current_user not in chat.users:
        raise HTTPException(status_code=400, detail="Current user is not a participant of the chat.")
    return crud.create_message(db=db, chat_id=chat_id, user_id=current_user.id, content=message.content)


@app.post("/messages/{message_id}/like/", response_model=schemas.MessageLike)
def like_message(message_id: int, db: Session = Depends(get_db),
                 current_user: models.User = Depends(jwt_authentication)):
    message = crud.get_message(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if current_user.id in [u.id for u in message.liked_by_users]:
        raise HTTPException(status_code=400, detail="User has already liked the message")
    return crud.like_message(db, message_id=message_id, user_id=current_user.id)


@app.get("/chats/{chat_id}/messages/", response_model=List[schemas.Message])
def get_messages(chat_id: int, db: Session = Depends(get_db),
                 current_user: models.User = Depends(jwt_authentication)):
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if current_user not in chat.users:
        raise HTTPException(status_code=400, detail="Current user is not a participant of the chat.")
    return crud.get_messages(db, chat_id=chat_id)
