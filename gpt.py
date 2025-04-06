import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv("project.env")
# Set up the Gemini API key
genai.configure(api_key=os.getenv('API_KEY'))

def get_summarise(system, text):
    model = genai.GenerativeModel("gemini-2.0-flash")
    contents = [
        {"role": "user", "parts": [f"{system} Topic: {text}"]},
    ]
    response = model.generate_content(contents)
    return response.text

