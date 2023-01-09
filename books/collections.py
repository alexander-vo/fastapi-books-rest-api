from typing import Optional, List

from flask_pymongo import PyMongo
from pymongo import UpdateOne
from pymongo.collection import Collection
from pymongo.database import Database

from books.models import Book, Pagination, SaveBooksResults


class BooksCollection:
    collection_name: str = 'books'

    def __init__(self, mongo: PyMongo):
        self._mongo = mongo

    @property
    def mongo(self) -> PyMongo:
        return self._mongo

    @property
    def db(self) -> Database:
        return self._mongo.db

    @property
    def collection(self) -> Collection:
        return self.db.get_collection(self.collection_name)

    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """
        Search book by id in the database
        """
        book = self.collection.find_one({'_id': book_id})
        return Book(**book) if book else None

    def get_books(self, search_filter: dict, sort: tuple, pagination: Pagination = Pagination()) -> List[Book]:
        """
        Find books by search params in 'search_filter'.
        Sort films by 'published_date' field and order in 'sort'
        Paginate through books using 'pagination'
        """
        cursor = self.collection.find(search_filter)

        if sort:
            cursor.sort(*sort)

        skip = pagination.page_size * (pagination.page - 1)
        cursor.skip(skip).limit(pagination.page_size)

        return [Book(**book) for book in cursor]

    def save_books(self, books: List[Book]) -> SaveBooksResults:
        """
        Save new books entries and update already existing ones
        """
        if not books:
            return SaveBooksResults()

        # Creating list of operations for bulk update operation
        # upsert=True perform an insert if no documents match the filter
        operations = [UpdateOne({'_id': book.id}, {'$set': book.dict(by_alias=True)}, upsert=True) for book in books]
        bulk_results = self.collection.bulk_write(operations)

        return SaveBooksResults(
            inserted_ids=list(bulk_results.upserted_ids.values()),
            updated_count=bulk_results.modified_count
        )
