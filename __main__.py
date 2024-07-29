from dotenv import load_dotenv
from web.web_main import app

load_dotenv(dotenv_path='.env')

if __name__ == '__main__':
    print("\n App Running and website is available at http://localhost:5000/")
    app.run(debug=True, host='127.0.0.1')
