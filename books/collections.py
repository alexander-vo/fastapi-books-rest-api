from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo import UpdateOne
from pymongo.results import BulkWriteResult, DeleteResult

from books.models import Book, Pagination


class BooksCollection:
    collection_name: str = "books"

    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self._db = mongo_db

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self._db.get_collection(self.collection_name)

    async def get_book_by_id(self, book_id: str) -> Book | None:
        book = await self.collection.find_one({"_id": book_id})
        return Book(**book) if book else None

    async def get_books(
        self, search_filter: dict, sort: tuple, pagination: Pagination = Pagination()
    ) -> list[Book]:
        cursor = self.collection.find(search_filter)

        if sort:
            cursor.sort(*sort)

        skip = pagination.page_size * (pagination.page - 1)
        cursor.skip(skip).limit(pagination.page_size)

        return [Book(**book) async for book in cursor]

    async def delete_book(self, book_id: str) -> DeleteResult:
        return await self.collection.delete_one({"_id": book_id})

    async def save_books(self, books: list[Book]) -> BulkWriteResult:
        operations = [
            UpdateOne({"_id": book.id}, {"$set": book.dict(by_alias=True)}, upsert=True)
            for book in books
        ]
        return await self.collection.bulk_write(operations)
