from fastapi import Depends, HTTPException, BackgroundTasks, UploadFile, File, Form, FastAPI
from fastapi.staticfiles import StaticFiles
# from dark_swag import FastAPI
from sqlalchemy.orm import Session
from ai.Chat.chat import chat_with_history_model
from ai.Image.image_create import generate_image_pollinations
from ai.Video.generate_video import generate_video
# from ai.RAG.rag_chat import chat_rag
from ai.RAG.vektor_database import save_document_chroma
from db_conn import Base, engine, Local_Sesion, get_db
import uvicorn
from uuid import uuid4
import models
from hash_pswrd import hash_pswd, verify_pswd
import schemas_models
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/files", StaticFiles(directory="Users_files"), name="files")


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World"}


@app.post("/auth/login", tags=["Auth"])
async def login_user(user: schemas_models.LoginUser, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_pswd(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {"message": "Login successful"}


@app.post("/auth/register", tags=["Auth"])
async def create_user(user: schemas_models.CreateUser, db: Session = Depends(get_db)):
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
async def update_user(user_id: int, user: schemas_models.UpdateUser, db: Session = Depends(get_db)):
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
async def patch_user(user_id: int, user: schemas_models.PatchUser, db: Session = Depends(get_db)):
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


@app.post("/chat", tags=["AI TOOLS"])
async def chat_ai(message: str, session_id: str, db: Session = Depends(get_db)):
    response = chat_with_history_model(request=message, session_id=session_id)
    return response['message']


@app.get("/chat_history", tags=["AI TOOLS"])
async def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    db_chat_history = db.query(models.ChatHistory).filter(models.ChatHistory.session_id == session_id).all()
    if not db_chat_history:
        return {"message": "Chat history not found"}
    else:
        return {"chats": db_chat_history}


def saved_image_data(file_name: str, file_path: str, session_id: str):
    db = Local_Sesion()
    image = models.Images(
        session_id=session_id,
        image_path=file_path,
        image_name=file_name
    )
    db.add(image)
    db.commit()
    db.refresh(image)


@app.post("/create_image", tags=["AI TOOLS"])
async def create_image(message: str, bg_task: BackgroundTasks, session_id: str, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.session_id == session_id).first()
    if not db_user:
        return {"message": "User not found"}
    response = generate_image_pollinations(session_id=session_id, request=message)
    bg_task.add_task(
        saved_image_data,
        session_id=session_id,
        file_name=response["image_name"],
        file_path=response["image_path"]
    )
    return response


@app.get("/images/{session_id}", tags=["AI TOOLS"])
async def get_image(session_id: str, db: Session = Depends(get_db)):
    db_image = db.query(models.Images).filter(models.Images.session_id == session_id).all()
    if not db_image:
        return {"message": "Image not found"}
    else:
        return {"images": db_image}


@app.get("/images", tags=["AI TOOLS"])
async def get_all_images(db: Session = Depends(get_db)):
    return {"all_images": db.query(models.Images).all()}


def saved_video(file_name: str, file_path: str, session_id: str):
    db = Local_Sesion()
    video = models.Videos(
        session_id=session_id,
        video_path=file_path,
        video_name=file_name
    )
    db.add(video)
    db.commit()
    db.refresh(video)


@app.post("/video", tags=["AI TOOLS"])
async def create_video(message: str, session_id: str, bg_task: BackgroundTasks, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.session_id == session_id).first()
    if not db_user:
        return {"message": "User not found"}
    response = generate_video(topic=message, session_id=session_id)
    bg_task.add_task(
        saved_image_data,
        session_id=session_id,
        file_name=response["video_name"],
        file_path=response["video_path"]
    )
    return response


@app.get("/video/{session_id}", tags=["AI TOOLS"])
async def get_video(session_id: str, db: Session = Depends(get_db)):
    db_video = db.query(models.Videos).filter(models.Videos.session_id == session_id).all()
    if not db_video:
        return {"message": "Video not found"}
    else:
        return {"video": db_video}


@app.get("/video", tags=["AI TOOLS"])
async def get_video_all(db: Session = Depends(get_db)):
    db_videos = db.query(models.Videos).all()
    if not db_videos:
        return {"message": "Video not found"}
    else:
        return {"videos": db_videos}


@app.post("/file", tags=["AI TOOLS"])
async def file_uploaded(bg_task: BackgroundTasks, session_id: str, file: UploadFile = File(...),
                        db: Session = Depends(get_db)):
    folder_check = f"Users_files/{session_id}"
    os.makedirs(folder_check, exist_ok=True)
    with open(f"{folder_check}/" + f"{file.filename}", "wb") as f:
        f.write(file.file.read())
        saved = save_document_chroma(file_name=file.filename, collection_name=session_id,
                                     file_path=f"{folder_check}/{file.filename}")
        if saved['message'] == "Bazaga saqlandi":
            return {"message": "Vector bazaga saqlandi", "file_path": f"Users_files/{session_id}/{file.filename}",
                    "file_name": file.filename}
        else:
            return {"message": "Vector bazaga saqlanmadi"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
