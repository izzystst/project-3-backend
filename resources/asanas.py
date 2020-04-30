import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

asanas = Blueprint('asanas', 'asanas')

@asanas.route('/', methods=['POST'])
def create_asana():
	payload = request.get_json()

	new_asana = models.Asana.create(name=payload['name'], difficulty=payload['difficulty'], instructions=payload['instructions'])
	print(new_asana)
	print(new_asana.__dict__)

	asana_dict= model_to_dict(new_asana)

	return jsonify(
		data=asana_dict,
		message='congrats you added a new asana',
		status=201
		),201
# index route
@asanas.route('/', methods=["GET"])
def asanas_index():
	return "blah"


# show route
@asanas.route('<id>', methods=["GET"])
def show_asana(id):
	asana = models.Asana.get_by_id(id)

	asana_dict=model_to_dict(asana)

	return jsonify(
		data=asana_dict,
		message=f'found asana with id {id}',
		status=200), 200