from peewee import *
import datetime
from flask_login import UserMixin, current_user

DATABASE = SqliteDatabase('asanas.sqlite')

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
	length=BigIntegerField()
	notes=TextField()
	user=ForeignKeyField(User, backref='sessions')

	class Meta:
		database = DATABASE

class Asana(Model):
	name=CharField()
	difficulty=SmallIntegerField()
	instructions=CharField()

	class Meta:
		database = DATABASE

class SessionPoses(Model):
	session=ForeignKeyField(Session, backref='sessions')
	asana=ForeignKeyField(Asana, backref='asanas')

	class Meta:
		database = DATABASE
def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Session, Asana, SessionPoses], safe=True)
	print("connected to db and created tables!")

	DATABASE.close()