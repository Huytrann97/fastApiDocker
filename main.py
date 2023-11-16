from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated

from database import SessionLocal, engine
from sqlalchemy.orm import Session
from uuid import UUID
import models

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import os
import shutil

from documentProcessing.main_path import process_document
from documentProcessing.uploadS3 import upload_image_to_s3

from PIL import Image
import io

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class User(BaseModel):
    card_id: str
    full_name: str
    birthday: str
    address: str
    expire_date: str

@app.post("/")
def create_info(user: User, db: Session = Depends(get_db)):
    db_user = models.User()
    db_user.card_id = user.card_id
    db_user.full_name = user.full_name
    db_user.birthday = user.birthday
    db_user.address = user.address
    db_user.expire_date = user.expire_date
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/<imageName>")
def read_image(imageName):
    result = process_document(imageName)
    return {"Result": result}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    target_folder = "processing_image"
    # Create the target folder if it doesn't exist
    os.makedirs(target_folder, exist_ok=True)
    # Save the uploaded image to the local folder
    file_path = os.path.join(target_folder, file.filename)
    with open(file_path, "wb") as image:
        shutil.copyfileobj(file.file, image)
        print("successfully uploaded to local")

    # Replace 'your_destination_key' with the desired key in your S3 bucket
    if file:
        uploaded = upload_image_to_s3(file.filename)
        if uploaded:
            return "File uploaded successfully to S3."
        else:
            return "Error in uploading to S3."
    else:
        return "No file provided for upload."
