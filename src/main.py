from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from io import BytesIO
from src.process_image import process_image

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("take_picture_form.html", {"request": request})


@app.post("/process-image/")
async def process_image_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(BytesIO(contents))

    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Apply the processing function
    detected_objects = process_image(image)

    return JSONResponse(content=detected_objects)
