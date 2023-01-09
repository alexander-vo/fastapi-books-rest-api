from typing import List

from pydantic import BaseModel, Field


class Book(BaseModel):
    id: str = Field(..., alias='_id')
    title: str = ''
    authors: List[str] = []
    published_date: str = ''
    categories: List[str] = []
    average_rating: float = .0
    ratings_count: int = 0
    thumbnail: str = ''


class Pagination(BaseModel):
    page: int = 1
    page_size: int = 10


class SaveBooksResults(BaseModel):
    inserted_ids: List[str] = []
    updated_count: int = 0
