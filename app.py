from flask import Flask, jsonify
from resources.users import users
from resources.sessions import sessions
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
		return models.User.get_by_id(user_id)
	except models.DoesNotExist:
		return None

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(sessions, url_prefix='/api/v1/sessions')
@app.route('/')
def hello():
	return 'hell world!'



if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)