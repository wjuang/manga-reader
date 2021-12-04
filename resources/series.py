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

@series.route('/<id>', methods=['GET'])
def single_series(id):
    series = models.Series.get_by_id(id)

    return jsonify(
        data=model_to_dict(series),
        message="Got one series",
        status=200
    ), 200

@series.route('/<id>', methods=['PUT'])
def update_series(id):
    payload = request.get_json()

    models.Series.update(**payload).where(models.Series.id == id).execute()

    return jsonify(
        data=model_to_dict(models.Series.get_by_id(id)),
        message="Updated series",
        status=200
    ), 200

@series.route('/<id>', methods=['DELETE'])
def delete_series(id):
    delete_query = models.Series.delete().where(models.Series.id == id)
    nums_of_rows_deleted = delete_query.execute()
    print(nums_of_rows_deleted)
    #if no rows were deleted, return some message

    return jsonify(
        data={},
        message=f"Deleted {nums_of_rows_deleted} series with id {id}",
        status=200
    ), 200
