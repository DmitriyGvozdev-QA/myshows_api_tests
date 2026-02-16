import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("HOST", "http://localhost/api")
