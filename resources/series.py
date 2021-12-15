import models
import datetime
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
    new_series = models.Series.create(title=payload['title'], author=payload['author'], artist=payload['artist'], chaptercount=0, cover=payload['cover'], submittedBy=payload['submittedBy'])
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
    result = models.Chapter.select().where(models.Chapter.seriesid == id)
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
    result = models.Chapter.select().where((models.Chapter.seriesid == id) & (models.Chapter.number == id2))
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

    new_chapter = models.Chapter.create(seriesid=id, pagenumber=payload['pagenumber'], number=payload['number'], submittedBy=payload['submittedBy'])

    models.Series.update({models.Series.chaptercount: models.Series.chaptercount + 1, models.Series.updated: new_chapter.uploaded}).where(models.Series.id == id).execute()

    chapter_dict = model_to_dict(new_chapter)

    return jsonify({
    'data': chapter_dict,
    'message': 'Chapter added.',
    'status': 201
    }), 201

    return "Chapter added."

@series.route('/<id>/<id2>', methods=['DELETE'])
def delete_chapter(id, id2):
    delete_query = models.Chapter.delete().where((models.Chapter.number == id2) & (models.Chapter.seriesid == id))
    nums_of_rows_deleted = delete_query.execute()
    print(nums_of_rows_deleted)

    models.Series.update({models.Series.chaptercount: models.Series.chaptercount - 1}).where(models.Series.id == id).execute()


    return jsonify(
        data={},
        message=f"Deleted {nums_of_rows_deleted} chapters",
        status=200
    ), 200

@series.route('/<id>/<id2>', methods=['PUT'])
def edit_chapter(id, id2):
    payload = request.get_json()

    models.Chapter.update(**payload).where((models.Chapter.seriesid == id) & (models.Chapter.number == id2)).execute()

    return jsonify(
        data=model_to_dict(models.Chapter.get_by_id(id)),
        message="Updated chapter",
        status=200
    ), 200


#PAGE ROUTES
@series.route('/<id>/<id2>/pages', methods=['GET'])
def pages_index(id, id2):
    result = models.Page.select().where((models.Page.seriesid == id) & (models.Page.chapternumber == id2))
    print('')
    print('All Pages: ')
    print(result)

    pages_dict = [model_to_dict(pages) for pages in result]

    return jsonify({
    'data': pages_dict,
    'message': f'Successfully found {len(pages_dict)} pages.',
    'status': 200
    }), 200

    return "Pages list fetched."

@series.route('/<id>/<id2>/<id3>', methods=['GET'])
def get_one_page(id, id2, id3):
    result = models.Page.select().where((models.Page.seriesid == id) & (models.Page.number == id3) & (models.Page.chapternumber == id2))
    print('')
    print('Found page: ')
    print(result)

    page_dict = [model_to_dict(page) for page in result]

    return jsonify({
    'data': page_dict,
    'message': f'Successfully found {len(page_dict)} page.',
    'status': 200
    }), 200

@series.route('/<id>/<id2>', methods = ['POST'])
def pages_post(id, id2):
    payload = request.get_json()
    # current_chapter = models.Chapter.select().where((models.Chapter.seriesid == id) & (models.Chapter.number == id2))
    # print('')
    # print(current_chapter)
    # print('')
    new_page = models.Page.create(chapternumber=id2, seriesid=id, link=payload['link'], number=payload['number'])

    models.Chapter.update({models.Chapter.pagenumber: models.Chapter.pagenumber + 1}).where((models.Chapter.seriesid == id) & (models.Chapter.number == id2)).execute()

    page_dict = model_to_dict(new_page)

    return jsonify({
    'data': page_dict,
    'message': 'Page added.',
    'status': 201
    }), 201

    return "Page added."

@series.route('/<id>/<id2>/<id3>', methods=['DELETE'])
def delete_page(id, id2, id3):
    delete_query = models.Page.delete().where((models.Page.number == id3) & (models.Page.seriesid == id) & (models.Page.chapternumber == id2))
    nums_of_rows_deleted = delete_query.execute()
    print(nums_of_rows_deleted)

    models.Chapter.update({models.Chapter.pagenumber: models.Chapter.pagenumber - 1}).where((models.Chapter.seriesid == id) & (models.Chapter.number == id2)).execute()

    return jsonify(
        data={},
        message=f"Deleted {nums_of_rows_deleted} pages",
        status=200
    ), 200

@series.route('/<id>/<id2>/<id3>', methods=['PUT'])
def edit_page(id, id2, id3):
    payload = request.get_json()

    models.Page.update(**payload).where((models.Page.seriesid == id) & (models.Page.number == id3) & (models.Page.chapternumber == id2)).execute()

    return jsonify(
        data=model_to_dict(models.Page.get_by_id(id)),
        message="Updated page.",
        status=200
    ), 200
