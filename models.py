from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('asanas.sqlite')

class User(UserMixin, Model):
	username=CharField(unique=True)
	email=CharField(unique=True)
	password=CharField(unique=True)
	zipcode=CharField()
	created_on= DateTimeField(default=datetime.date.today)

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User], safe=True)
	print("connected to db and created tables!")

	DATABASE.close()