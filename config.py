import os
from os import getenv
from typing import Type


class Config:
    """
    Base config class
    """
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    ENV = 'production'
    BUNDLE_ERRORS = True
    MONGO_USERNAME = getenv('MONGO_USERNAME', '')
    MONGO_USER_PASSWORD = getenv('MONGO_USER_PASSWORD', '')
    MONGO_DB_NAME = getenv('PROD_MONGO_DB_NAME', '')
    MONGO_CLUSTER_NAME = getenv('MONGO_CLUSTER_NAME', '')

    @property
    def MONGO_URI(self):  # noqa
        return f'mongodb+srv://{self.MONGO_USERNAME}:{self.MONGO_USER_PASSWORD}' \
               f'@{self.MONGO_CLUSTER_NAME}/{self.MONGO_DB_NAME}?retryWrites=true&w=majority'


class DevelopmentConfig(Config):
    """
    Development config class
    """
    FLASK_ENV = 'development'
    ENV = 'development'
    DEBUG = True
    MONGO_DB_NAME = getenv('DEV_MONGO_DB_NAME', '')


class TestingConfig(Config):
    """
    Testing config class
    """
    FLASK_ENV = 'development'
    ENV = 'development'
    TESTING = True
    MONGO_DB_NAME = getenv('TEST_MONGO_DB_NAME', '')


def get_config() -> Type[Config]:
    """
    Returns configuration class depends on environment variable ENV
    """
    env = os.getenv('ENV')

    if env == 'prod':
        return Config
    if env == 'test':
        return TestingConfig

    return DevelopmentConfig
