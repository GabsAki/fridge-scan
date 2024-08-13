# References: https://www.datacamp.com/tutorial/gpt4o-api-openai-tutorial
# https://medium.com/@jxnlco/bridging-language-model-with-python-with-instructor-pydantic-and-openais-function-calling-f32fb1cdb401

from openai import OpenAI
import json
import base64

# Load the OpenAI API key from a file
with open("credentials.json") as f:
    openai_key = json.load(f)["api_key"]

client = OpenAI(api_key=openai_key)
MODEL="gpt-4o"

URL = "https://images.squarespace-cdn.com/content/5ae63d7c8f51303ed37a8ab3/1563891519689-0BQ7XJHJN43MF6SYOJVZ/JUL03779-Edit.jpg"

from pydantic import BaseModel
from typing import List
import instructor

instructor.patch(client)

class FoodItemsResponse(BaseModel):
    food_items: List[str]

response = client.chat.completions.create(
    model=MODEL,
    response_model=FoodItemsResponse,
    #response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "You are a helpful assistant that identifies food items in fridge photos and lists them out so then another assistant can help the user with recipes. Your output is an exhaustive list of the food items identified in the picture"},
        {"role": "user", "content": [
            {"type": "text", "text": "What food items are in this picture?"},
            {"type": "image_url", "image_url": {
                "url": URL}
            }
        ]}
    ],
    temperature=0.0,
)

print(response)
