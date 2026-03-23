import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "performos_one_on_one_v2")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Collections
users_collection = db.users
members_collection = db.members
submissions_collection = db.submissions  # Changed from sessions to submissions
flags_collection = db.flags

async def init_db():
    """Initialize database with indexes"""
    # Create indexes
    await users_collection.create_index("email", unique=True)
    await members_collection.create_index("manager_id")
    await submissions_collection.create_index("member_id")
    await submissions_collection.create_index("date")
    await submissions_collection.create_index([("member_id", 1), ("date", 1)], unique=True)
    await flags_collection.create_index("member_id")
    await flags_collection.create_index("submission_id")
    print("✅ Database indexes created")