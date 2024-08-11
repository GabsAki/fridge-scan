from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from io import BytesIO
import os

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Check if the uploaded file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    # Read the image file
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing image.")

    # Example: Convert image to grayscale
    grayscale_image = image.convert("L")

    # Save the processed image to a temporary location
    output_path = os.path.join("processed_images", file.filename)
    os.makedirs("processed_images", exist_ok=True)
    grayscale_image.save(output_path)

    return FileResponse(output_path, media_type="image/jpeg", filename=file.filename)
