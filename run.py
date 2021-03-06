from flask import Flask
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

import routes

if __name__ == '__main__':
    app.run()