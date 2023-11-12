from fastapi import FastAPI
from pydantic import BaseModel
from documentProcessing.main_path import process_document

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import shutil
import os


from PIL import Image
import io

app = FastAPI()

# image_path = "image1.jpg"# with open(image_path, "rb") as image_file:
#     url = io.BytesIO(image_file.read())
# url = "https://scontent.fdad2-1.fna.fbcdn.net/v/t1.15752-9/373483333_720806080085391_8759204674535948605_n.png?_nc_cat=101&ccb=1-7&_nc_sid=8cd0a2&_nc_ohc=S20DrnQ3xpwAX8ixdNr&_nc_ht=scontent.fdad2-1.fna&oh=03_AdSRvrpeDhzhpC_q76x1nscHL5olKYAcGu37h_ukfecoEg&oe=65759087"


@app.get("/")
async def read_root():
    return {"message": "Hello, !"}

@app.get("/<imageName>") 
def read_image(imageName):

    result = process_document(imageName)  
    return {"Result": result}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    
    target_folder = "processing_image"
    
    # Tạo thư mục lưu trữ nếu chưa tồn tại
    os.makedirs(target_folder, exist_ok=True)
    
    # Lưu hình ảnh vào thư mục D:\image
    with open(f"{target_folder}/{file.filename}", "wb") as image:
        shutil.copyfileobj(file.file, image)
    
    return {"successfully uploaded": file.filename}

