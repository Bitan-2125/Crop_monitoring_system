import os
from dotenv import load_dotenv

load_dotenv()

weather_api_key = os.getenv("WEATHER_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
