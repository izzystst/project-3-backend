import os
from flask import Flask, jsonify, g
from resources.users import users
from resources.sessions import sessions
from resources.asanas import asanas
from resources.sessionposes import sessionposes
from flask_cors import CORS

from flask_login import LoginManager, current_user
import models
DEBUG=True
PORT=8000
app = Flask(__name__)

app.secret_key = "dumb secret"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	try:
		user= models.User.get_by_id(user_id)
		return user
	except models.DoesNotExist:
		return None


@login_manager.unauthorized_handler
def unautherized():
	return jsonify(
		data={"error":'user not logged in'},
		message="you must be logged in to access this",
		status=401
		), 401

CORS(sessions, origins=['http://localhost:3000'],supports_credentials=True)
CORS(users, origins=['http://localhost:3000'],supports_credentials=True)
CORS(asanas, origins=['http://localhost:3000'], supports_credentials=True)



app.register_blueprint(sessions, url_prefix='/api/v1/sessions')
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(asanas, url_prefix='/api/v1/asanas')
app.register_blueprint(sessionposes, url_prefix='/api/v1/sessionposes')
@app.before_request # use this decorator to cause a function to run before reqs
def before_request():
  """Connect to the db before each request"""
  # store the database as a global var in g
  print("you should see this before each request") # optional -- to illustrate that this code rus before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
  g.db = models.DATABASE
  g.db.connect()


@app.after_request # use this decorator to cause a function to run after reqs
def after_request(response):
  """Close the db connetion after each request"""
  print("you should see this after each request") # optional -- to illustrate that this code runs after each request
  g.db.close()
  return response # go ahead and send response back to client 
                  # (in our case this will be some JSON)
@app.route('/')
def hello():
	return 'hell world!'
if 'ON_HEROKU' in os.environ:
	print('\non heroku!')
	models.initialize()


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)