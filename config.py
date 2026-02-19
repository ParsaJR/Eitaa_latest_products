from dotenv import load_dotenv
import os

_ = load_dotenv()

liara_api_key = os.getenv("LIARA_API_KEY")
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
