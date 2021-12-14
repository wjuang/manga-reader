from peewee import *
import datetime

DATABASE = SqliteDatabase('manga.sqlite')

class Series(Model):
    title = CharField()
    author = CharField()
    artist = CharField()
    updated = DateTimeField(default=datetime.datetime.now)
    chaptercount = IntegerField(default=0, null=True)
    cover = CharField(null=True)
    submittedBy = CharField()
    id = PrimaryKeyField()

    class Meta:
        database = DATABASE

class Chapter(Model):
    seriesid = ForeignKeyField(Series, related_name='chapters')
    uploaded = DateTimeField(default=datetime.datetime.now)
    pagenumber = IntegerField(default=0, null=True)
    number = IntegerField(null=True)
    submittedBy = CharField()
    id = PrimaryKeyField()

    class Meta:
        database = DATABASE

class Page(Model):
    chapternumber = IntegerField()
    seriesid = ForeignKeyField(Series, related_name='pages')
    link = CharField()
    number = IntegerField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Series, Chapter, Page], safe=True)
    print('Tables created.')
    DATABASE.close()
