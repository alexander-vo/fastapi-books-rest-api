from enum import IntEnum

import pymongo
from pydantic import BaseModel, Field


class Book(BaseModel):
    id: str = Field(..., alias="_id")
    title: str = ""
    authors: list[str] = []
    published_date: str = ""
    categories: list[str] = []
    average_rating: float = 0.0
    ratings_count: int = 0
    thumbnail: str = ""


class Pagination(BaseModel):
    page: int = 1
    page_size: int = 10


class SortingParam(IntEnum):
    ascending = pymongo.ASCENDING
    descending = pymongo.DESCENDING


class BooksFilters(BaseModel):
    published_date: str | None
    sort: SortingParam
    page: int
    page_size: int
    authors: list[str]


class SaveBooksResult(BaseModel):
    inserted_ids: list[str] = []
    updated_count: int = 0


class DeleteBookResult(BaseModel):
    deleted_id: str
    deleted_count: int = 0


class PopulateBooksBody(BaseModel):
    query: str
