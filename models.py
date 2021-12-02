from peewee import *
import datetime

DATABASE = SqliteDatabase('manga.sqlite')

class Series(Model):
    title = CharField()
    author = CharField()
    artist = CharField()
    updated = DateTimeField(default=datetime.datetime.now)
    chapters = IntegerField()
    cover = CharField()
    id = PrimaryKeyField()

    class Meta:
        database = DATABASE

class Chapter(Model):
    series = ForeignKeyField(Series, related_name='chapters')
    uploaded = DateTimeField(default=datetime.datetime.now)
    pages = IntegerField()
    number = IntegerField()
    id = PrimaryKeyField()

    class Meta:
        database = DATABASE

class Page(Model):
    chapter = ForeignKeyField(Chapter, related_name='pages')
    link = CharField()
    number = IntegerField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Series, Chapter, Page], safe=True)
    print('Tables created.')
    DATABASE.close()
