from flask import Flask
from utils import DBManager

app = Flask(__name__)
dbm = DBManager('root','')

@app.route("/")
def hello():
	return "hey Isaac"
@app.route("/path")
def function_to_run():
	return "gavin is a butt"
@app.route("/student_login")
def login_student(uname,pwd):
	success = dbm.authenticate(uname,pwd,'students')
	if success:
		return "You In student"
	else:
		return "You done fucked up"

@app.route("/professor_login")
def login_student(uname,pwd):
	success = dbm.authenticate(uname,pwd,'professors')
	if success:
		return "You In professor"
	else:
		return "You done fucked up"

@app.route("/admin_login")
def login_student(uname,pwd):
	success = dbm.authenticate(uname,pwd,'adminstrators')
	if success:
		return "You In admin"
	else:
		return "You done fucked up"

if __name__ == '__main__':
	app.run('localhost',port=9001)