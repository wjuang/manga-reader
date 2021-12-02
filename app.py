from flask import Flask, jsonify

from resources.series import series

import models

DEBUG = True

PORT=8000

app = Flask(__name__)

app.register_blueprint(series, url_prefix='/reader')

@app.route('/')
def test():
    return 'App works!'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
