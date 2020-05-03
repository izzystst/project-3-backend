import models

from flask import Blueprint, request, jsonify


from playhouse.shortcuts import model_to_dict
from flask_login import LoginManager, current_user


import pprint
pp = pprint.PrettyPrinter(indent=4)

sessionposes = Blueprint('sessionposes', 'sessionposes')

# index for all session poses 
@sessionposes.route('/', methods=["GET"])
def session_poses():
	all_session_poses = models.SessionPoses.select()
	print("this is all the poses")
	pp.pprint(all_session_poses)
	all_session_poses_dict = [model_to_dict(all_session_pose) for all_session_pose in all_session_poses]
	print("this is the dict of all session poses")
	pp.pprint(all_session_poses_dict)
	return jsonify(
		data=all_session_poses_dict,
		message="these are all the sessionposes",
		status=200
		), 200
		
