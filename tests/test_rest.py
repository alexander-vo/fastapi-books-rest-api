from typing import List

import pytest
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    'book_id, expected_status, expected_title',
    [
        ('CSUeAQAAIAAJ', 200, 'The Hobbit'),
        ('hFfhrCWiLSMC', 200, 'The Hobbit, Or, There and Back Again'),
        ('N_0VhzQKIIAC', 200, 'Finding God in the Hobbit'),
        ('KUSn4G6eiCUC', 200, 'A Hobbit Devotional'),
    ]
)
def test_get_book_by_id_success(client: FlaskClient, book_id: str, expected_status: int, expected_title: str):
    response = client.get(f'/api/books/{book_id}')
    assert response.content_type == 'application/json'
    assert response.status_code == expected_status
    assert response.json.get('data')[0]['title'] == expected_title


@pytest.mark.parametrize(
    'book_id, expected_status',
    [
        ('', 404),
        ('random_string', 404),
        (2221221, 404),
    ]
)
def test_get_book_by_id_fail(client: FlaskClient, book_id: str, expected_status: int):
    response = client.get(f'/api/books/{book_id}')
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'published_date, author, sort, page, page_size, expected_status, expected_ids',
    [
        ('2012', None, None, None, None, 200, ['KY0BDObXftUC', 'H8ON-dTgQQYC', 'Wy0svf_7NzsC', 'ouD2ugAACAAJ']),
        ('2001', ['J.R.R. Tolkien'], None, None, None, 200, ['tFWlPwAACAAJ']),
        ('2001', ['J.R.R. Tolkien'], None, None, None, 200, ['tFWlPwAACAAJ']),
        ('2001', ['Chuck Dixon', 'John Ronald Reuel Tolkien'], None, None, None, 200, ['yZSLAAAACAAJ']),
        ('2001', ['John Ronald Reuel Tolkien', 'Chuck Dixon'], None, None, None, 200, ['yZSLAAAACAAJ']),
        (None, ['Brian Sibley'], None, None, None, 200, ['e5srNGZN70wC', 'X_YUAgAAQBAJ']),
        (None, ['Jay Richards', 'Jonathan Witt'], None, None, None, 200, ['TdDhBAAAQBAJ']),
        (None, ['J.R.R. Tolkien'], '+published_date', None, None, 200,
         ['rHeGmAEACAAJ', 'tFWlPwAACAAJ', 'a5yPPwAACAAJ', 'ouD2ugAACAAJ', 'OlCHcjX0RT4C']),
        (None, ['J.R.R. Tolkien'], '-published_date', None, None, 200,
         ['OlCHcjX0RT4C', 'ouD2ugAACAAJ', 'a5yPPwAACAAJ', 'tFWlPwAACAAJ', 'rHeGmAEACAAJ']),
        (None, None, '-published_date', 10, 3, 200, ['N_0VhzQKIIAC', 'U4nM6f26XjgC', '8ef3-s6fixIC']),
        (None, None, '+published_date', 5, 2, 200, ['a5yPPwAACAAJ', 'NzhFw7ZMsMAC']),

    ]
)
def test_get_books_endpoint(
        client: FlaskClient,
        published_date: str,
        author: List[str],
        sort: str,
        page: int, page_size: int, expected_status: int, expected_ids: List[str]
):
    query = {
        'published_date': published_date,
        'author': author,
        'sort': sort,
        'page': page,
        'page_size': page_size
    }
    response = client.get('/api/books', query_string=query)

    assert response.content_type == 'application/json'
    assert response.status_code == expected_status
    ids = [book['_id'] for book in response.json['data']]
    assert ids == expected_ids
