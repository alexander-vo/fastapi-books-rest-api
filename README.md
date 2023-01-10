# fastapi-books-rest-api

Books REST API

Books taken from Google Books API [https://www.googleapis.com/books/v1/volumes](https://www.googleapis.com/books/v1/volumes )
searched with additional query parameter `q`.

Example:

[https://www.googleapis.com/books/v1/volumes?q=Hobbit](https://www.googleapis.com/books/v1/volumes?q=Hobbit)

In code used with additional query parameters:

```json
{
  "langRestrict": "en",
  "maxResults": 40,
  "startIndex": 0
}
```

`"maxResults": 40` - max value for books per page

Example:

[https://www.googleapis.com/books/v1/volumes?q=Hobbit&langRestrict=en&maxResults=40&startIndex=0](https://www.googleapis.com/books/v1/volumes?q=Hobbit&langRestrict=en&maxResults=40&startIndex=0)


## Configuration

Environment variables are required (take a look at .env.template):

```dotenv
MONGO_DB_URL="mongodb://user:password@mongodb:27017"
MONGO_ROOT_USERNAME=user
MONGO_ROOT_PASSWORD=password
MONGO_INITDB_DATABASE=books-db
```

You can use them already using `cp .env.template .env` command.


## Python version 

`python 3.10`

## How to run

1) Install docker and docker-compose
2) Run `make start` or `docker-compose up` command
3) Check application home page [http://localhost:3000](http://localhost:3000)
4) Check api docs [http://localhost:3000/docs](http://localhost:3000/docs) or [http://localhost:3000/redoc](http://localhost:3000/redoc)
6) Stop application using `make stop` or `docker-dompose down` command
