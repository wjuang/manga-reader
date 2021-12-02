import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

series = Blueprint('series', 'series')

@series.route('/', methods=['GET'])
def series_index():
    print('index route hit')
    return('index route hit')
