from typing import List

import pytest
from pymongo import ASCENDING, DESCENDING

from books.db import mongo, books_collection
from books.models import Pagination, Book
from config import TestingConfig


@pytest.mark.usefixtures('client')
def test_db_name():
    assert mongo.db.name == TestingConfig.MONGO_DB_NAME


@pytest.mark.parametrize(
    'book_id, expected_title',
    [
        ('CSUeAQAAIAAJ', 'The Hobbit'),
        ('KY0BDObXftUC', 'Exploring J.R.R. Tolkien\'s The Hobbit'),
        ('8_YUAgAAQBAJ', 'The Hobbit, the Desolation of Smaug'),
        (None, None),
        ('some_random_string', None)
    ]
)
def test_get_book_by_id(book_id: str, expected_title: str):
    book = books_collection.get_book_by_id(book_id)
    title = book.title if book else None
    assert title == expected_title


@pytest.mark.parametrize(
    'page, page_size, expected_ids',
    [
        (1, 5, ['CSUeAQAAIAAJ', 'KY0BDObXftUC', 'H8ON-dTgQQYC', 'hFfhrCWiLSMC', 'Wy0svf_7NzsC']),
        (8, 5, ['NzhFw7ZMsMAC', 'A6kbTwEACAAJ', 'rHeGmAEACAAJ', 'wFMO7R-qvDUC', 'a5yPPwAACAAJ']),
        (7, 10, []),
        (14, 3, ['a5yPPwAACAAJ']),
        (15, 2, ['arsgAgAAQBAJ', 'yZSLAAAACAAJ']),
        (-1, -2, ['Wy0svf_7NzsC', '8ef3-s6fixIC']),
        (-3, -5, ['SQz2AAAAQBAJ', 'TdDhBAAAQBAJ', '8KdEAgAAQBAJ', '1rogAgAAQBAJ', '-3HK5oU_OPgC']),
    ]
)
def test_get_books_pagination(page: int, page_size: int, expected_ids: List[str]):
    pagination = Pagination(page=page, page_size=page_size)
    books = books_collection.get_books({}, (), pagination)
    ids = [book.id for book in books]
    assert ids == expected_ids


@pytest.mark.parametrize(
    'published_date, expected_ids',
    [
        ('', []),
        ('2012', ['KY0BDObXftUC', 'H8ON-dTgQQYC', 'Wy0svf_7NzsC', 'ouD2ugAACAAJ']),
        ('2001', ['yZSLAAAACAAJ', 'tFWlPwAACAAJ']),
        ('2008', ['T2YYQrkcplAC']),
        ('10000', []),
        ('random_str', []),
        (2012, []),
    ]
)
def test_get_books_search_by_published_date(published_date: str, expected_ids: List[str]):
    search_filter = {'published_date': published_date}
    books = books_collection.get_books(search_filter, ())
    ids = [book.id for book in books]
    assert ids == expected_ids


@pytest.mark.parametrize(
    'authors, expected_ids',
    [
        ([], []),
        (['J.R.R. Tolkien'], ['ouD2ugAACAAJ', 'OlCHcjX0RT4C', 'tFWlPwAACAAJ', 'rHeGmAEACAAJ', 'a5yPPwAACAAJ']),
        (['J.R.R. Tolkien', 'Charles Dixon'], ['tFWlPwAACAAJ']),
        (['Charles Dixon', 'J.R.R. Tolkien'], ['tFWlPwAACAAJ']),
        (['Random Author'], []),
        (['Ruth Perry', 'Allan Jay Friedman', 'David Rogers'], ['wFMO7R-qvDUC']),
        (['Ruth Perry', 'David Rogers', 'Allan Jay Friedman'], ['wFMO7R-qvDUC']),
        (['David Rogers', 'Ruth Perry'], ['wFMO7R-qvDUC']),
    ]
)
def test_get_books_search_by_authors(authors: List[str], expected_ids: List[str]):
    search_filter = {'authors': {'$all': authors}}
    books = books_collection.get_books(search_filter, ())
    ids = [book.id for book in books]
    assert ids == expected_ids


@pytest.mark.parametrize(
    'order, expected_ids',
    [
        (ASCENDING, ['wFMO7R-qvDUC', 'hFfhrCWiLSMC', 'XiRea3tWUK0C', 'CSUeAQAAIAAJ', 'rHeGmAEACAAJ']),
        (DESCENDING, ['3XGlBAAAQBAJ', 'ariQBAAAQBAJ', 'TdDhBAAAQBAJ', 'glFsAwAAQBAJ', 'arsgAgAAQBAJ']),
    ]
)
def test_get_books_sorting(order: int, expected_ids: List[str]):
    sort = ('published_date', order)
    books = books_collection.get_books({}, sort, Pagination(page_size=5))
    ids = [book.id for book in books]
    assert ids == expected_ids


TEST_SAVE_BOOKS_BOOKS_PARAM = [
    # test 3 new books
    [{'_id': 'T1', 'title': 'T1_T'}, {'_id': 'T2', 'title': 'T2_T'}, {'_id': 'T3', 'title': 'T3_T'}],
    # test 2 new books and 1 updated
    [{'_id': 'T4', 'title': 'T4_T'}, {'_id': 'T5', 'title': 'T5_T'}, {'_id': 'T1', 'title': 'T1_TT'}],
    # test 1 new books and 2 updated
    [{'_id': 'T6', 'title': 'T6_T'}, {'_id': 'T2', 'title': 'T2_TT'}, {'_id': 'T3', 'title': 'T3_TT'}],
    # test 0 new books and 3 updated
    [{'_id': 'T4', 'title': 'T4_TT'}, {'_id': 'T5', 'title': 'T5_TT'}, {'_id': 'T6', 'title': 'T6_TT'}],
    # test 0 new books and 0 updated
    [],
    # test 0 new books and 0 updated with unchanged books
    [{'_id': 'T5', 'title': 'T5_TT'}, {'_id': 'T6', 'title': 'T6_TT'}]
]

TEST_SAVE_BOOKS_EXPECTED_RESULTS_PARAM = [
    {'inserted_ids': ['T1', 'T2', 'T3'], 'updated_count': 0},
    {'inserted_ids': ['T4', 'T5'], 'updated_count': 1},
    {'inserted_ids': ['T6'], 'updated_count': 2},
    {'inserted_ids': [], 'updated_count': 3},
    {'inserted_ids': [], 'updated_count': 0},
    {'inserted_ids': [], 'updated_count': 0},
]


@pytest.mark.parametrize(
    'books, expected_results',
    list(zip(TEST_SAVE_BOOKS_BOOKS_PARAM, TEST_SAVE_BOOKS_EXPECTED_RESULTS_PARAM))
)
def test_save_books(books: List[dict], expected_results: dict):
    books_to_save = [Book(**book) for book in books]
    result = books_collection.save_books(books_to_save)
    assert result == expected_results
