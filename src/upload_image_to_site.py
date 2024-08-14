import httpx
import base64
import os

from io import BytesIO
from PIL import Image
from fastapi import HTTPException


async def upload_image_to_site(image: Image.Image):
    # Your API key
    FREEIMAGE_API_KEY = os.getenv("FREEIMAGE_API_KEY")

    # The URL to which the request will be sent
    url = "https://freeimage.host/api/1/upload"

    # Convert the PIL Image object to bytes
    buffered = BytesIO()
    image.save(buffered, format="JPEG")  # You can change the format if needed
    image_bytes = buffered.getvalue()

    # Encode the image bytes to base64
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')

    # Set up the parameters for the API request
    params = {
        "key": FREEIMAGE_API_KEY,
        "action": "upload",
        "source": encoded_image,
        "format": "json"
    }

    # Make the API call using httpx
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=params)

    # Handle the response from the API
    if response.status_code == 200:
        json_response = response.json()
        
        return json_response.get('image', {}).get('url')
    else:
        raise HTTPException(status_code=response.status_code, detail="Error uploading image.")
