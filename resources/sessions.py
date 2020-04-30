import models

from flask import Blueprint, request, jsonify


from playhouse.shortcuts import model_to_dict
from flask_login import LoginManager, current_user




sessions = Blueprint('sessions', 'sessions')

# @sessions.route('/', methods=['GET'])
# def test_session():
# 	return "session resource works"
# create rouet
@sessions.route('/', methods=['POST'])
def create_session():
	payload= request.get_json()
	new_session = models.Session.create(length=payload['length'], notes=payload['notes'], user=current_user.id)
	print(new_session)
	session_dict = model_to_dict(new_session)
	session_dict['user'].pop('password')
	
	return jsonify(
		data=session_dict,
		message="succesffuly created a session",
		status=200
		), 200

@sessions.route('/', methods=['GET'])
def sessions_index():
	sessions = models.Session.select()
	sessions_dict = [model_to_dict(session) for session in sessions]
	print(sessions_dict)
	return jsonify(
		data=sessions_dict,
		message="found all sessions",
		status=200
		),200
	# 	date=DateTimeField(default=datetime.date.today)
	# length=BigIntegerField()
	# notes=TextField()
	# user=ForeignKeyField(User, backref='sessions', defaul)
@sessions.route("/<id>", methods=['GET'])
def session_show(id):
	session = models.Session.get_by_id(id)
	session_dict = model_to_dict(session)
	return jsonify(
		data=session_dict,
		message=f"found session with id {id}",
		status=200
		), 200