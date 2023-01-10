from dataclasses import dataclass

from books.collections import BooksCollection
from books.models import (Book, BooksFilters, DeleteBookResult, Pagination,
                          SaveBooksResult)
from books.utils import get_new_books_by_query


@dataclass
class BooksService:
    books_collection: BooksCollection

    async def get_books_by_filters(self, filters: BooksFilters) -> list[Book]:
        pagination = Pagination(page=filters.page, page_size=filters.page_size)

        search_filter = {}
        if filters.authors:
            search_filter.update({"authors": {"$all": filters.authors}})
        if filters.published_date:
            search_filter.update({"published_date": filters.published_date})

        mongo_sort = ("published_date", filters.sort)

        return await self.books_collection.get_books(
            search_filter, mongo_sort, pagination
        )

    async def get_book_by_id(self, book_id: str) -> Book | None:
        return await self.books_collection.get_book_by_id(book_id)

    async def delete_book(self, book_id: str) -> DeleteBookResult | None:
        result = await self.books_collection.delete_book(book_id)
        if not result.deleted_count:
            return None
        return DeleteBookResult(deleted_id=book_id, deleted_count=result.deleted_count)

    async def populate_db_with_books(self, query: str) -> SaveBooksResult:
        books = await get_new_books_by_query(query)
        if not books:
            return SaveBooksResult()
        result = await self.books_collection.save_books(books)
        return SaveBooksResult(
            inserted_ids=list(result.upserted_ids.values()),
            updated_count=result.modified_count,
        )
