import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

series = Blueprint('series', 'series')

@series.route('/', methods=['GET'])
def series_index():
    result = models.Series.select()
    print('')
    print('All Series: ')
    print(result)

    series_dict = [model_to_dict(series) for series in result]

    return jsonify({
    'data': series_dict,
    'message': f'Successfully found {len(series_dict)} series.',
    'status': 200
    }), 200

    return "Series list fetched."

@series.route('/', methods=['POST'])
def series_post():
    payload = request.get_json()
    new_series = models.Series.create(title=payload['title'], author=payload['author'], artist=payload['artist'], chapters=0, cover=payload['cover'])
    print(new_series)

    series_dict = model_to_dict(new_series)

    return jsonify({
    'data': series_dict,
    'message': 'Series added.',
    'status': 201
    }), 201

    return "Series added."
