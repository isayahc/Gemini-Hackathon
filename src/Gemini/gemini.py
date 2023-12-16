from src.Config.config import GEMINI_API_KEY

import google.generativeai as genai



genai.configure(api_key=GEMINI_API_KEY)