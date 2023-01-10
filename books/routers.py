from fastapi import APIRouter, HTTPException, Query, status

from books.db import books_collection
from books.models import Book, PopulateBooksBody, SaveBooksResult, SortingParam
from books.services import BooksFilters, BooksService

responses = {
    404: {"description": "Book not found"},
}


books_router = APIRouter(
    prefix="/books",
    tags=["books"],
)


books_service = BooksService(books_collection)


@books_router.get("/")
async def get_all_books(
    published_date: str = None,
    sort: SortingParam = SortingParam.ascending,
    page: int = 1,
    page_size: int = 10,
    authors: list[str] | None = Query(default=None),
) -> list[Book]:
    return await books_service.get_books_by_filters(
        BooksFilters(
            published_date=published_date,
            sort=sort,
            page=page,
            page_size=page_size,
            authors=authors,
        )
    )


@books_router.get(
    "/{book_id}", responses=responses, summary="Retrieves a single book by id"
)
async def get_book_by_id(book_id: str) -> Book:
    if result := await books_service.get_book_by_id(book_id):
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@books_router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=responses,
    summary="Delete a single book by id",
)
async def delete_book_by_id(book_id: str):
    if result := await books_service.delete_book(book_id):
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@books_router.post(
    "/populate",
    status_code=status.HTTP_201_CREATED,
    summary="Populate database with new books from google search",
)
async def upload_new_books(body: PopulateBooksBody) -> SaveBooksResult:
    return await books_service.populate_db_with_books(body.query)
