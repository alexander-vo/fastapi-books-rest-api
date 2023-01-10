from motor.motor_asyncio import AsyncIOMotorClient

from books.collections import BooksCollection
from settings import DB_NAME, MONGO_DB_URL

mongo = AsyncIOMotorClient(MONGO_DB_URL)
db = mongo.get_database(DB_NAME)

books_collection = BooksCollection(db)
