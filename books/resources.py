import pymongo

from books.db import books_collection
from books.models import Pagination
from books.utils import get_new_books_by_query
from flask_restful import Resource, abort, reqparse


class Books(Resource):

    # Creating settings for books endpoint query args
    parser = reqparse.RequestParser()
    parser.add_argument('published_date', type=str, trim=True)
    parser.add_argument('author', action='append', dest='authors')
    parser.add_argument('sort', type=str, trim=True)
    parser.add_argument('page', type=int, default=1)
    parser.add_argument('page_size', type=int, default=10)

    def get(self):
        """
        GET request parser for Books resource.
        Takes additional query params for filtering like 'author' and 'published_date'.
        Sorting allowed using 'sort' param. Pagination is enabled using 'page' and 'page_size' params.
        """
        args = self.parser.parse_args()

        pagination = Pagination(page=args['page'], page_size=args['page_size'])

        sort = ()
        if args['sort']:
            order = pymongo.DESCENDING if args['sort'].startswith('-') else pymongo.ASCENDING
            sort = ('published_date', order)

        search_filter = {}
        if args['authors']:
            search_filter.update({'authors': {'$all': args['authors']}})
        if args['published_date']:
            search_filter.update({'published_date': args['published_date']})

        books = books_collection.get_books(search_filter, sort, pagination)
        return {'data': [book.dict(by_alias=True) for book in books]}


class Book(Resource):

    def get(self, book_id):
        """
        GET request parser for Book resource.
        Takes additional path param 'book_id'.
        Performs search by 'book_id'
        """
        result = books_collection.get_book_by_id(book_id)
        if not result:
            abort(404, data=[], message=f'No book with id: {book_id}')
        return {'data': [result.dict(by_alias=True)]}


class AddBooks(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('q', type=str, required=True, location='json', help='q param need to be defined')

    def post(self):
        """
        POST request parser for AddBooks resource.
        Additional param 'q' is required in POST body.
        Search books by search param 'q' using Google Books API.
        Save new books to db or updates existing ones.
        """
        args = self.parser.parse_args()
        # Getting books from Google books API
        books = get_new_books_by_query(args['q'])
        result = books_collection.save_books(books)
        return {'data': [result.dict()]}, 201
