from dotenv.main import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

SERVER_URL = 'localhost'
PORT = 8900
ENV = "dev"

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
print(GEMINI_API_KEY)
