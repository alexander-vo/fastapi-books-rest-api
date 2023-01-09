from flask_pymongo import PyMongo

from books.collections import BooksCollection

mongo = PyMongo()
books_collection = BooksCollection(mongo)
