import os
import logging
from flask import Flask
from distutils.util import strtobool

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    logging.basicConfig(filename='log/flask.log', level=logging.DEBUG)

    app.run(debug=strtobool(os.getenv('FLASK_DEBUG', True)), host='0.0.0.0', port=8888)