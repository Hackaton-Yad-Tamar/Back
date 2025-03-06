# App configurationss
from dotenv import load_dotenv
import os

load_dotenv()


DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "yad-tamar"),
    "user": os.getenv("POSTGRES_USER", "yad-tamar"),
    "password": os.getenv("POSTGRES_PASSWORD", "shovalking123!"),
    "host": os.getenv("DB_HOST", "20.50.143.29"),
    "port": os.getenv("DB_PORT", "5432"),
}