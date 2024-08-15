# Script Goal: receive a JSON with a list in the 'food_items' key and return a list of recipes that can be made with the food items.
import google.generativeai as genai
import os
import json

GEMINI_API_KEY = gemini_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_key)

# Create the model
generation_config = {
    # Lower values of temperature, top_p and top_k mean the model will be less creative
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
system_instruction="You're a helpful assistant that creates detailed recipes using only the ingredients provided by the user. Each recipe must include step-by-step instructions and should never introduce ingredients not listed. You don't need to use all the ingredients provided, but no extras should be included. Under no circumstances should you add or suggest any ingredients not explicitly listed. Stick strictly to the provided list.",
)

def generate_recipes_with_gemini(food_items: list) -> str:
    response = model.generate_content("\n".join(food_items))
    return response.text