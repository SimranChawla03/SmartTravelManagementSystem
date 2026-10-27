
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")
database_name = os.getenv("DATABASE_NAME")

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    client.admin.command("ping")
    print("MongoDB Atlas connected successfully!")
    print("Database name:", database_name)
    client.close()
except Exception as e:
    print("MongoDB connection failed.")
    print("Error:", e)
