from os import getenv


ENV = getenv('ENVIRONMENT', 'development')
MONGO_DB_URL = getenv('MONGO_DB_URL')
DB_NAME = getenv('MONGO_INITDB_DATABASE')
