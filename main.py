from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import models
from sqlalchemy.orm import Session
from database import engine
from sqlalchemy import select

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool = False


class UserUpdate(UserCreate):
    id: int


@app.post("/users/")
def create_user(user: UserCreate, db: Session = Session(bind=engine)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Session(bind=engine)):
    user = db.execute(select(models.User).where(models.User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/")
def update_user(user: UserUpdate, db: Session = Session(bind=engine)):
    db_user = db.execute(select(models.User).where(models.User.id == user.id)).scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Session(bind=engine)):
    user = db.execute(select(models.User).where(models.User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}

