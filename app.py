from flask import Flask, request, render_template, session, redirect
from utils import DBManager
from datetime import datetime

app = Flask(__name__)
app.secret_key = "rexrexrex"
dbm = DBManager('root','')

def get_current_sem():
	now = datetime.now()
	if now.month >= 6:
		semester = 'Fall {}'.format(now.year)
	else:
		semester = 'Spring {}'.format(now.year)
	return semester


@app.route("/")
def home():
	if 'access' in session:
		if session['access'] == "student":
			return render_template('student_home.html',schedule=dbm.get_schedule(session['uid'],session['semester']))
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
			return render_template('student_home.html',schedule=dbm.get_schedule(session['uid'],session['semester']))	
		else:
			return redirect("/")
	return render_template('index.html')

@app.route("/grades")
def studentGrades():
	if 'uname' in session:
		if session['access'] == "student":
			return render_template('student_grades.html',grades=dbm.get_grades(session['uid']))
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
		session['semester'] = get_current_sem()
		return redirect("student")
	else:
		return redirect("logout")

@app.route("/professor_login", methods=['POST'])
def professor_login():
	uname = request.form['username']
	pwd = request.form['pass']
	uid = dbm.authenticate(uname,pwd,'professors')
	if uid != None:
		session['uname'] = uname
		session['uid'] = uid 
		session['access'] = "professor" 
		return "You In professor"
	else:
		return "You done fucked up"

@app.route("/admin_login", methods=['POST'])
def admin_login():
	uname = request.form['username']
	pwd = request.form['pass']
	uid = dbm.authenticate(uname,pwd,'adminstrators')
	if uid != None:
		session['uname'] = uname
		session['uid'] = uid 
		session['access'] = "admin" 
		return "You In admin"
	else:
		return "You done fucked up"

@app.route("/drop", methods=['POST'])
def drop_class():
	cids = request.form.getlist('drop')
	dropped_cids = list()
	class_info = list()
	if 'uid' in session:
		if session['access'] == 'student':
			try:
				for cid in cids:
					dbm.drop(session['uid'],cid)
					dropped_cids += [cid]
			except(KeyError):
				pass
			except(ValueError):
				pass
			for cid in dropped_cids:
				class_info += [dbm.get_class_info(cid)]
			return render_template("dropped.html",class_info=class_info)
		else:
			return redirect("401")
	else:
		return redirect("/")
	

@app.route("/logout")
def logout():
	session.pop('uname',None)
	session.pop('uid',None)
	session.pop('access',None)
	return redirect("")

if __name__ == '__main__':
	app.run('localhost',port=9001)