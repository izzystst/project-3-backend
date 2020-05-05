import models

from flask import Blueprint, request, jsonify


from playhouse.shortcuts import model_to_dict
from flask_login import LoginManager, current_user


import pprint
pp = pprint.PrettyPrinter(indent=4)


sessions = Blueprint('sessions', 'sessions')

# @sessions.route('/', methods=['GET'])
# def test_session():
# 	return "session resource works"
# create rouet
@sessions.route('/', methods=['POST'])
def create_session():
	
	payload= request.get_json()
	print('this is the payload')
	print(payload['asana'])
	new_session = models.Session.create(length=payload['length'], notes=payload['notes'], user=current_user.id)
	print(new_session)
	session_dict = model_to_dict(new_session)
	session_dict['user'].pop('password')
	print("this is the asana payload")
	print(payload['asana'][0])
	for asana in payload['asana']:
		new_poseSession = models.SessionPoses.create(asana=asana, session=session_dict['id'])
		print('this is the pose session create')
		pp.pprint(model_to_dict(new_poseSession))
		print(new_poseSession.session.id)
	return jsonify(
		data=session_dict, 
		message="succesffuly created a session",
		status=200
		), 200

@sessions.route('/', methods=['GET'])
def sessions_index():
	sessions = models.Session.select()
	print('this is the sessions')
	asanas_in_sessions = models.SessionPoses.select().order_by('session')
	asanas_in_session_dict = [model_to_dict(asanas_in_session) for asanas_in_session in asanas_in_sessions]
	# pp.pprint(sessions)
	total = []
	for session in sessions:
		session_dict = model_to_dict(session)
		asanas = []
		for session_pose in asanas_in_session_dict:
			if(session_pose['session']['id'] == session.id):

				asanas.append(session_pose['asana'])
				pp.pprint(session_pose)
				pp.pprint(session)

		session_dict['asanas'] = asanas
		total.append(session_dict)
		pp.pprint(session_dict) 
	
	print('this is the the total')
	# pp.pprint(total)
	print('this is total index 1')
	# pp.print(total[1])
	# sessions_dict = [model_to_dict(session) for session in sessions]
	# pp.pprint(sessions_dict)
	# print('this is the asana in the session')
	# pp.pprint(asanas_in_sessions)
	# print("these are the asanas in dict")
	# pp.pprint(asanas_in_session_dict)
	# sessions_dict.update(asanas_in_session_dict)
	# pp.pprint(session_dict)
	
	# for asana in asanas_in_session_dict:
	# 	print(asana)
	# 	# print(asana['session']['id'])
	# 	# if asana if matches curent id, push to id list, if not put the id list , in final list, as a list, empty list, checnage current id of the one that didnt match 
	# 	if(asana['session']['id'] == current_id):

	# 		id_list.append(asana)

	# 	else:
	# 		pp.pprint(id_list)
	# 		final_list.append(id_list)
		
	# 		# print('this is now the current id')
	# 		current_id = asana['id']
	# 		# print(current_id)
	# 		id_list = []



			# print("this is the asanas in session dict")
			# make final list a list dictionaries - probably not worth it  
		# ?sessions_dict[asanas] = final list
	# pp.pprint(asanas_in_session_dict)
	return jsonify(
		data=total,
		message="found all sessions and the poses in them",
		status=200
		),200


@sessions.route("/<id>", methods=['GET'])
def session_show(id):
	session = models.Session.get_by_id(id)
	session_dict = model_to_dict(session)


	asanas = models.SessionPoses.select().where(models.SessionPoses.session == id)
	# asanas.execute()
	print('these are the asanas')
	print(asanas)
	# asanas_dict = model_to_dict(asanas)
	# print(asanas_dict)
	asana_dict = [model_to_dict(asana) for asana in asanas]
	pp.pprint(asana_dict)

	# asanas_list=[]
	# for asana in asanas:
	# 	if asana["session"] == id:
	# 		print(asana)
	# 		asanas_list.append(asana)


	# print(asanas_list)
	print("this is asans after the loop")
	print(asanas)
	return jsonify(
		data={'session': session_dict, 'asanas': asana_dict },
		message=f"found session with id {id}",
		status=200
		), 200

@sessions.route('/<id>', methods=["POST"])
def update_session(id):
	payload= request.get_json()
	update_query= models.Session.update(
		length=payload['length'],
		notes=payload['notes']
		).where(models.Session.id==id)

	# for asana in payload['asana']:
	# 	update_pose_query=models.SessionPoses.update(
	# 		asana=asana
	# 	).where(models.SessionPoses.session.id==id)
	# 	sessionP_num_rows_modified = update_pose_query.execute()

	num_rows_modified = update_query.execute()
	updated_session = models.Session.get_by_id(id)
	update_session_dict = model_to_dict(updated_session)

	return jsonify(
		data=update_session_dict,
		message=f"update session with id {id}",
		status=200
		), 200
@sessions.route('/<id>', methods=['DELETE'])
def delete_session(id):
	delete_query = models.Session.delete().where(models.Session.id==id)
	num_rows_deleted = delete_query.execute()
	print(num_rows_deleted)
	return jsonify(
		data={},
		message=f"deleted session {num_rows_deleted} with id {id}",
		status=200
		),200




