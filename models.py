import os
from peewee import *
import datetime
from flask_login import UserMixin, current_user
from playhouse.db_url import connect
if 'ON_HEROKU' in os.environ:
	DATABASE = connect(os.environ.get('DATABASE_URL'))



else:
	DATABASE = SqliteDatabase('asanas.sqlite',
		pragmas = {'foreign_keys': 1})

class User(UserMixin, Model):
	username=CharField(unique=True)
	email=CharField(unique=True)
	password=CharField(unique=True)
	zipcode=CharField()
	created_on= DateTimeField(default=datetime.date.today)

	class Meta:
		database = DATABASE
class Session(Model):
	date=DateTimeField(default=datetime.date.today)
	length=TextField()
	notes=TextField()
	user=ForeignKeyField(User, backref='sessions', on_delete="CASCADE")

	class Meta:
		database = DATABASE

class Asana(Model):
	name=CharField()
	difficulty=SmallIntegerField()
	instructions=CharField()

	class Meta:
		database = DATABASE

class SessionPoses(Model):
	session=ForeignKeyField(Session, backref='sessionposes', on_delete="CASCADE")
	asana=ForeignKeyField(Asana, backref='sessionposes',  on_delete="CASCADE")

	class Meta:
		database = DATABASE
def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Session, Asana, SessionPoses], safe=True)
	print("connected to db and created tables!")

	DATABASE.close()