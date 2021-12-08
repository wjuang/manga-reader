from flask import Flask, jsonify

from resources.series import series

from flask_cors import CORS

import models

DEBUG = True

PORT=8000

app = Flask(__name__)

CORS(series, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(series, url_prefix='/reader')

@app.route('/')
def test():
    return 'App works!'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
