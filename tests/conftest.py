import json
import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from books.collections import BooksCollection
from settings import MONGO_DB_URL

DB_NAME = "test_db"
TESTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))


@pytest.fixture(scope="session")
def mongo_client() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(MONGO_DB_URL)
    yield client
    client.close()


@pytest.fixture(scope="module")
def mongodb(mongo_client: AsyncIOMotorClient):
    db: AsyncIOMotorDatabase = mongo_client[DB_NAME]
    yield db
    mongo_client.drop_database(DB_NAME)


@pytest.fixture(scope="function")
def mock_data():
    with open(os.path.join(TESTS_DIR, "test_books.json"), "r") as f:
        return json.load(f)


@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def books_collection(
    mongodb: AsyncIOMotorDatabase, mock_data: list[dict]
) -> BooksCollection:
    collection = BooksCollection(mongodb)
    await collection.collection.insert_many(mock_data)
    yield collection
    collection.collection.drop()


@pytest.fixture(scope="module")
def client() -> TestClient:
    app = FastAPI()
    yield TestClient(app)
