from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from src.upload_image_to_site import upload_image_to_site
from src.process_image_openai import process_image_with_gpt4
from src.generate_recipes import generate_recipes_with_gemini

from PIL import Image
from io import BytesIO


app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

@app.post("/upload-image/")
async def upload_image(request: Request, file: UploadFile = File(...)):
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
    image_url = await upload_image_to_site(image)

    food_items: list = process_image_with_gpt4(image_url)

    recipes: str = generate_recipes_with_gemini(food_items)

    return templates.TemplateResponse(
        "display_result.html",
        {"request": request, "food_items": food_items, "recipes": recipes}
    )
