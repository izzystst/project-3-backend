from flask import Flask, jsonify
from resources.users import users
import models
DEBUG=True
PORT=8000
app = Flask(__name__)

app.register_blueprint(users, url_prefix='/api/v1/users')

@app.route('/')
def hello():
	return 'hell world!'



if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)