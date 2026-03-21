import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(MONGO_URL)
db = client.performos_one_on_one

# Collections
users_collection = db.users
members_collection = db.members
sessions_collection = db.sessions
flags_collection = db.flags

async def init_db():
    """Initialize database with indexes"""
    # Create indexes
    await users_collection.create_index("email", unique=True)
    await members_collection.create_index("manager_id")
    await sessions_collection.create_index("member_id")
    await sessions_collection.create_index("manager_id")
    await flags_collection.create_index("member_id")
    await flags_collection.create_index("session_id")
    print("✅ Database indexes created")