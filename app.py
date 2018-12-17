from flask import Flask, request, render_template, session, redirect
from utils import DBManager

app = Flask(__name__)
app.secret_key = "rexrexrex"
dbm = DBManager('root','')

@app.route("/")
def home():
	if 'access' in session:
		if session['access'] == "student":
			return render_template('student_home.html')
		elif session['access'] == "professor":
			return render_template('faculty_home.html')
		elif session['access'] == "admin":
			return render_template('admin_home.html')
		else:
			redirect("logout")
	else:
		return render_template('index.html')

@app.route("/student")
def students():
	if 'uname' in session:
		if session['access'] == "student":
			return render_template('student_home.html')	
		else:
			return redirect("/")
	return render_template('index.html')

@app.route("/faculty")
def faculty():
	if 'uname' in session:
		if session['access'] == "professor":
			return render_template('faculty_home.html')
		else:
			return redirect("/")
	return render_template('professor_login.html')

@app.route("/admin")
def admin():
	if 'uname' in session:
		if session['access'] == "admin":
			return render_template('admin_home.html')
		else:
			return redirect("/")
	return render_template('admin_login.html')

@app.route("/student_login", methods=['POST'])
def student_login():
	uname = request.form['username']
	pwd = request.form['pass']
	uid = dbm.authenticate(uname,pwd,'students')
	if uid != None:
		session['uname'] = uname
		session['uid'] = uid 
		session['access'] = "student" 
		return redirect("student")
	else:
		return redirect("logout")

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

@app.route("/logout")
def logout():
	session.pop('uname',None)
	session.pop('uid',None)
	session.pop('access',None)
	return redirect("")

if __name__ == '__main__':
	app.run('localhost',port=9001)