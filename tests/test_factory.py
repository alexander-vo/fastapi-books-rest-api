from typing import Type

import pytest

from books import create_app
from config import Config, DevelopmentConfig, TestingConfig


@pytest.mark.parametrize(
    'config',
    [
        Config,
        DevelopmentConfig,
        TestingConfig,
    ]
)
def test_config(config: Type[Config]):
    app = create_app(config)
    config_obj = config()
    assert app.testing == config_obj.TESTING
    assert app.debug == config_obj.DEBUG
    assert app.config['MONGO_URI'] == config_obj.MONGO_URI
    assert app.config['ENV'] == config_obj.ENV
    assert app.config['FLASK_ENV'] == config_obj.FLASK_ENV
