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

class User(BaseModel):
    card_id: str
    full_name: str
    birthday: str
    address: str
    expire_date: str

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
@app.get("/<imageName>")
def read_image(imageName):
    result = process_document(imageName)
    return {"Result": result}
