from flask import Flask
from utils import DBManager

app = Flask(__name__)

@app.route("/")
def hello():
	return "hey Isaac"

if __name__ == '__main__':
	app.run('localhost',port=9001)