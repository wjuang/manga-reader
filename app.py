from flask import Flask, jsonify, after_this_request

from resources.series import series

from flask_cors import CORS

from dotenv import load_dotenv
import os

import models

load_dotenv()

DEBUG = True

PORT=8000

app = Flask(__name__)

CORS(series, origins=['http://localhost:3000', 'https://makima-reader.herokuapp.com'], supports_credentials=True)

app.register_blueprint(series, url_prefix='/reader')

@app.before_request # use this decorator to cause a function to run before reqs
def before_request():

    """Connect to the db before each request"""
    print("you should see this before each request") # optional -- to illustrate that this code runs before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
    models.DATABASE.connect()

    @after_this_request # use this decorator to Executes a function after this request
    def after_request(response):
        """Close the db connetion after each request"""
        print("you should see this after each request") # optional -- to illustrate that this code runs after each request
        models.DATABASE.close()
        return response # go ahead and send response back to client
                      # (in our case this will be some JSON)

@app.route('/')
def test():
    return 'App works!'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)

if os.environ.get('FLASK_ENV') != 'development':
  print('\non heroku!')
  models.initialize()
