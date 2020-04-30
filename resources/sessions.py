import models

from flask import Blueprint, request, jsonify


from playhouse.shortcuts import model_to_dict




sessions = Blueprint('sessions', 'sessions')

@sessions.route('/', methods=['GET'])
def test_session():
	return "session resource works"
# create rouet
# @sessions.route('/', methods=['POST'])
# def creat_session():
