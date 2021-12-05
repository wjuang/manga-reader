import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

series = Blueprint('series', 'series')
chapter = Blueprint('chapter', 'chapter')

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


#CHAPTER ROUTES

@series.route('/<id>/chapters', methods=['GET'])
def get_chapters(id):
    result = models.Chapter.select().where(models.Chapter.series == id)
    print('')
    print('Chapters found: ')
    print(result)

    chapters_dict = [model_to_dict(chapter) for chapter in result]

    return jsonify({
    'data': chapters_dict,
    'message': f'Successfully found {len(chapters_dict)} chapters.',
    'status': 200
    }), 200

    return "Chapter list fetched."

@series.route('/<id>/<id2>', methods=['GET'])
def get_one_chapter(id, id2):
    result = models.Chapter.select().where((models.Chapter.series == id) & (models.Chapter.number == id2))
    print('')
    print('Found chapter: ')
    print(result)

    chapter_dict = [model_to_dict(chapter) for chapter in result]

    return jsonify({
    'data': chapter_dict,
    'message': f'Successfully found {len(chapter_dict)} chapter.',
    'status': 200
    }), 200


@series.route('/<id>', methods=['POST'])
def post_chapter(id):
    payload = request.get_json()
    print(payload['pages'])
    print(type(payload['pages']))
    new_chapter = models.Chapter.create(series=id, pagenumber=payload['pages'], number=payload['number'])

    chapter_dict = model_to_dict(new_chapter)

    return jsonify({
    'data': chapter_dict,
    'message': 'Chapter added.',
    'status': 201
    }), 201

    return "Chapter added."

@series.route('/<id>/<id2>', methods=['DELETE'])
def delete_chapter(id, id2):
    delete_query = models.Chapter.delete().where((models.Chapter.number == id2) & (models.Chapter.series == id))
    nums_of_rows_deleted = delete_query.execute()
    print(nums_of_rows_deleted)
    #if no rows were deleted, return some message

    return jsonify(
        data={},
        message=f"Deleted {nums_of_rows_deleted} chapters",
        status=200
    ), 200

@series.route('/<id>/<id2>', methods=['PUT'])
def edit_chapter(id, id2):
    payload = request.get_json()

    models.Chapter.update(**payload).where((models.Chapter.series == id) & (models.Chapter.number == id2)).execute()

    return jsonify(
        data=model_to_dict(models.Chapter.get_by_id(id)),
        message="Updated chapter",
        status=200
    ), 200
