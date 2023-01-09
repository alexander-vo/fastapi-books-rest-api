from books import create_app
from config import get_config

config = get_config()
app = create_app(config)

if __name__ == '__main__':
    # If runs on local machine, other are for gunicorn
    app.run()
