from flask import Flask, jsonify
import models
DEBUG=True
PORT=8000
app = Flask(__name__)



@app.route('/')
def hello():
	return 'hell world!'



if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT)