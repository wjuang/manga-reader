from flask import Flask

import models

DEBUG = True

PORT=8000

app = Flask(__name__)

@app.route('/')
def test():
    return 'App works!'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
