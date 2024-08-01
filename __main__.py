"""Start point of the application."""

from dotenv import load_dotenv

from models import create_db_and_tables
from web.web_main import app

load_dotenv('.env')


if __name__ == '__main__':
    """Run the application."""
    create_db_and_tables()
    print('\n App Running and website is available at http://localhost:5000/')
    app.run(debug=True, host='127.0.0.1')
