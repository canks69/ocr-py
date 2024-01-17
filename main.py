from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from ocr import get_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload-image")
async def upload_image(file: UploadFile = UploadFile(...), filename: str = Form(...)):
    # Check image size
    max_size_bytes = 5 * 1024 * 1024  # 5 MB
    file_content = await file.read()
    if len(file_content) > max_size_bytes:
        raise HTTPException(status_code=400, detail="Image size exceeds the allowed limit")

    # Check image MIME type
    allowed_mime_types = ["image/jpeg", "image/png"]
    if file.content_type not in allowed_mime_types:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are allowed.")

    # Save the uploaded image
    save_path = f"storage/{filename}"  # Specify the path to save the image
    with open(save_path, "wb") as f:
        f.write(file_content)

    try :
        text = get_text(save_path)
        return {
            "filename": filename,
            "content_type": file.content_type,
            "text": text
        }
    except Exception as e:
        return {
            "filename": filename,
            "content_type": file.content_type,
            "text": "Cannot get text"
        }


    
