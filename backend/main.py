from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from db_conn import Base, engine, Local_Sesion, get_db
import uvicorn
from uuid import uuid4
import models
from hash_pswrd import hash_pswd, verify_pswd
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World"}


@app.post("/auth/login", tags=["Auth"])
async def login_user(user: schemas.LoginUser, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_pswd(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {"message": "Login successful"}


@app.post("/auth/register", tags=["Auth"])
async def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    exsist_username = db.query(models.Users).filter(models.Users.username == user.username).first()
    if exsist_username:
        raise HTTPException(status_code=400, detail="Username already exists")
    exsist_email = db.query(models.Users).filter(models.Users.email == user.email).first()
    if exsist_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = models.Users(
        username=user.username,
        email=user.email,
        session_id=str(uuid4()),
        password=hash_pswd(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users", tags=["users"])
async def get_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@app.get("/users/{me}", tags=["users"])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


@app.put("/users/{user_id}", tags=["users"])
async def update_user(user_id: int, user: schemas.UpdateUser, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = hash_pswd(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.patch("/users/{user_id}", tags=["users"])
async def patch_user(user_id: int, user: schemas.PatchUser, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = hash_pswd(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
