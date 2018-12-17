from flask import Flask, request, render_template, session
from utils import DBManager

app = Flask(__name__,template_folder='')
app.secret_key = "rexrexrex"
dbm = DBManager('root','')

@app.route("/")
def hello():
	return render_template('index.html')
@app.route("/path")
def function_to_run():
	return 

@app.route("/student_login", methods=['POST'])
def student_login():
	uname = request.form['username']
	pwd = request.form['pass']
	uid = dbm.authenticate(uname,pwd,'students')
	if uid != None:
		session['uname'] = uname
		session['uid'] = uid 
		session['access'] = "student" 
		return "You In student " + session['uid']
	else:
		return "You done fucked up"

@app.route("/professor_login", methods=['POST'])
def professor_login(uname,pwd):
	uid = dbm.authenticate(uname,pwd,'professors')
	if uid != None:
		session['uname'] = uname
		session['uid'] = uid 
		session['access'] = "professor" 
		return "You In professor"
	else:
		return "You done fucked up"

@app.route("/admin_login", methods=['POST'])
def admin_login(uname,pwd):
	uid = dbm.authenticate(uname,pwd,'adminstrators')
	if uid != None:
		session['uname'] = uname
		session['uid'] = uid 
		session['access'] = "admin" 
		return "You In admin"
	else:
		return "You done fucked up"

if __name__ == '__main__':
	app.run('localhost',port=9001)