# References: https://www.datacamp.com/tutorial/gpt4o-api-openai-tutorial
# https://medium.com/@jxnlco/bridging-language-model-with-python-with-instructor-pydantic-and-openais-function-calling-f32fb1cdb401

from openai import OpenAI
from pydantic import BaseModel
from typing import List
import instructor
import os

OPENAI_KEY = openai_key = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=openai_key)
MODEL="gpt-4o"

instructor.patch(client)


class FoodItemsResponse(BaseModel):
    food_items: List[str]


def process_image_with_gpt4(image_url: str) -> list:
    response: FoodItemsResponse = client.chat.completions.create(
        model=MODEL,
        response_model=FoodItemsResponse,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that identifies food items in fridge photos and lists them out so then another assistant can help the user with recipes. Your output is an exhaustive list of the food items identified in the picture"},
            {"role": "user", "content": [
                {"type": "text", "text": "What food items are in this picture?"},
                {"type": "image_url", "image_url": {
                    "url": image_url}
                }
            ]}
        ],
        temperature=0.0,
    )

    return response.food_items
