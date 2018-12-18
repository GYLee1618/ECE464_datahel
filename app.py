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

def get_next_sem():
	now = datetime.now()
	if now.month >= 6:
		semester = 'Spring {}'.format(now.year+1)
	else:
		semester = 'Fall {}'.format(now.year)
	return semester


@app.route("/")
@app.route("/home")
def home():
	if 'access' in session:
		if session['access'] == "student":
			return render_template('student_home.html',schedule=dbm.get_schedule(session['uid'],get_current_sem()))
		elif session['access'] == "professor":
			return render_template('faculty_home.html',schedule=dbm.get_faculty_schedule(session['uid'],get_current_sem()))
		elif session['access'] == "admin":
			return render_template('admin_home.html')
		else:
			redirect("logout")
	else:
		return render_template('index.html')

@app.route("/account")	
def account():
	if 'uid' in session:
		if session['access'] == 'student':
			return render_template("account.html",error="")
		elif session['access'] == 'professor': 
			return render_template("professor_account.html",error="")
		elif session['access'] == 'admin': 
			return render_template("admin_account.html",error="")
		else:
			return redirect("/")
	else:
		return redirect("401")

@app.route("/change_pwd", methods=['POST'])
def change_pwd():
	if 'uid' in session:
		try:
			dbm.change_password(session['uid'],request.form['oldpass'],request.form['newpass'])
			if session['access'] == 'student':
				return render_template("account.html",error="Successfully Changed Password")
			elif session['access'] == 'professor': 
				return render_template("professor_account.html",error="Successfully Changed Password")
			elif session['access'] == 'admin': 
				return render_template("admin_account.html",error="Successfully Changed Password")
			else:
				return redirect("/")
		except ValueError:
			if session['access'] == 'student':
				return render_template("account.html",error="Wrong Password")
			elif session['access'] == 'professor': 
				return render_template("professor_account.html",error="Wrong Password")
			elif session['access'] == 'admin': 
				return render_template("admin_account.html",error="Wrong Password")
			else:
				return redirect("/")
	else:
		return redirect("401")

@app.route("/logout")
def logout():
	session.pop('uname',None)
	session.pop('uid',None)
	session.pop('access',None)
	return redirect("")

@app.route("/student")
def students():
	if 'uname' in session:
		if session['access'] == "student":
			return render_template('student_home.html',schedule=dbm.get_schedule(session['uid'],session['semester']))	
		else:
			return redirect("/")
	return render_template('index.html')

@app.route("/student_login", methods=['POST'])
def student_login():
	uname = request.form['username']
	pwd = request.form['pass']
	try:
		uid = dbm.authenticate(uname,pwd,'students')
		if uid != None:
			session['uname'] = uname
			session['uid'] = uid 
			session['access'] = "student" 
			session['semester'] = get_current_sem()
			return redirect("student")
		else:
			return redirect("logout")
	except:
		return redirect("logout")

@app.route("/grades")
def studentGrades():
	if 'uname' in session:
		if session['access'] == "student":
			return render_template('student_grades.html',grades=dbm.get_grades(session['uid']),gpa=dbm.get_gpa(session['uid']))
		if session['access'] == "professor":
			classes = dbm.get_faculty_schedule(session['uid'],get_current_sem())
			rosters = dict()
			for cl in classes:
				rosters[cl[1]] = dbm.get_roster(cl[0])

			return render_template('faculty_grades.html',rosters=rosters,classes=classes)
		else:
			return redirect("/")
	return render_template('index.html')

@app.route("/scheduling")
def studentSchedule():
	if 'uname' in session:
		if session['access'] == "student":
			return render_template('student_scheduling.html',plan=dbm.get_plan(session['uid'],get_next_sem()),schedule=dbm.get_classes(get_next_sem()))
		else:
			return redirect("/")
	return render_template('index.html')

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

@app.route("/add_plan", methods=['POST'])
def add_plan():
	cids = request.form.getlist('add_plan')
	planned_cids = list()
	class_info = list()
	if 'uid' in session:
		if session['access'] == 'student':
			try:
				for cid in cids:
					dbm.plan(session['uid'],cid)
					planned_cids += [cid]
			except(KeyError):
				pass
			except(ValueError):
				pass
			for cid in planned_cids:
				class_info += [dbm.get_class_info(cid)]
			return render_template("planned.html",class_info=class_info)
		else:
			return redirect("401")
	else:
		return redirect("/")

@app.route("/plan_enrol", methods=['POST'])
def enrol_plan():
	if 'uid' in session:
		if session['access'] == 'student':
			dbm.enrol_in_plan(session['uid'])
			return render_template("enrolled.html")
		else:
			redirect("401")
	else:
		redirect("home")


@app.route("/faculty")
def faculty():
	if 'uname' in session:
		if session['access'] == "professor":
			return render_template('faculty_home.html',schedule=dbm.get_faculty_schedule(session['uid'],get_current_sem()))
		else:
			return redirect("/")
	return render_template('professor_login.html')

@app.route("/professor_login", methods=['POST'])
def professor_login():
	uname = request.form['username']
	pwd = request.form['pass']
	try:
		uid = dbm.authenticate(uname,pwd,'professors')
		if uid != None:
			session['uname'] = uname
			session['uid'] = uid 
			session['access'] = "professor" 
			return redirect("faculty")
		else:
			return redirect("logout")
	except:
		return redirect("logout")

@app.route("/submit_grades/<int:cid>", methods=['POST'])
def submit_grades(cid):
	if 'uid' in session:
		if session['access'] == 'professor':
			for key in request.form:
				dbm.change_grade(int(key),cid,request.form[key])
			return redirect("/grades")
		else:
			redirect("401")
	else:
		redirect("home")


@app.route("/admin")
def admin():
	if 'uname' in session:
		if session['access'] == "admin":
			return render_template('admin_home.html')
		else:
			return redirect("/")
	return render_template('admin_login.html')

@app.route("/admin_login", methods=['POST'])
def admin_login():
	uname = request.form['username']
	pwd = request.form['pass']
	try:
		uid = dbm.authenticate(uname,pwd,'administrators')
		if uid != None:
			session['uname'] = uname
			session['uid'] = uid 
			session['access'] = "admin" 
			return redirect("home")
		else:
			return redirect("home")
	except:
		return redirect("home")

@app.route("/add_student")
def add_student():
	if 'access' in session:
		if session['access'] == 'admin':
			return render_template("add_student.html")
		else:
			return redirect("401")
	else:
		return redirect("home")


@app.route("/create_student", methods=['post'])
def create_student():
	name = request.form['name']
	ssn = request.form['ssn']
	try:
		dob = datetime.strptime(request.form['dob'],'%m-%d-%Y')
		dob = datetime.strftime(dob,'%Y%m%d')
	except:
		return redirect("add_student")
	address = request.form['address']
	major = request.form['major']
	try:
		grad = int(request.form['grad'])
	except:
		return redirect("add_student")
	if 'access' in session:
		if session['access'] == 'admin':
			info = dbm.new_student(ssn,name,address,dob,major,grad)
			return render_template("add_student_landing.html",info=info)
		else:
			return redirect("401")
	else:
		return redirect("home")

@app.route("/add_prof")
def add_professor():
	if 'access' in session:
		if session['access'] == 'admin':
			return render_template("add_prof.html")
		else:
			return redirect("401")
	else:
		return redirect("home")


@app.route("/create_prof", methods=['post'])
def create_professor():
	name = request.form['name']
	ssn = request.form['ssn']
	try:
		dob = datetime.strptime(request.form['dob'],'%m-%d-%Y')
		dob = datetime.strftime(dob,'%Y%m%d')
	except:
		return redirect("add_professor")
	address = request.form['address']
	department = request.form['department']
	try:
		salary = float(request.form['salary'])
	except:
		return redirect("add_professor")
	if 'access' in session:
		if session['access'] == 'admin':
			info = dbm.new_professor(ssn,name,address,dob,department,salary)
			return render_template("add_prof_landing.html",info=info)
		else:
			return redirect("401")
	else:
		return redirect("home")

@app.route("/add_admin")
def add_admin():
	if 'access' in session:
		if session['access'] == 'admin':
			return render_template("add_admin.html")
		else:
			return redirect("401")
	else:
		return redirect("home")


@app.route("/create_admin", methods=['post'])
def create_admin():
	name = request.form['name']
	ssn = request.form['ssn']
	try:
		dob = datetime.strptime(request.form['dob'],'%m-%d-%Y')
		dob = datetime.strftime(dob,'%Y%m%d')
	except:
		return redirect("add_admin")
	address = request.form['address']
	if 'access' in session:
		if session['access'] == 'admin':
			info = dbm.new_administrator(ssn,name,address,dob)
			return render_template("add_admin_landing.html",info=info)
		else:
			return redirect("401")
	else:
		return redirect("home")

@app.route("/add_classes")
def add_class():
	if 'access' in session:
		if session['access'] == 'admin':
			return render_template("add_class.html")
		else:
			return redirect("401")
	else:
		return redirect("home")


@app.route("/create_classes", methods=['post'])
def create_class():
	course_code = request.form['course_code']
	name = request.form['name']
	desc = request.form['description']
	semester = request.form['semester']
	semyear = request.form['year']
	semester = "{} {}".format(semester,semyear)
	meeting_times = request.form['meeting_times']
	dept = request.form['department']
	credits = request.form['credits']
	try:
		credits = int(credits)
	except:
		return redirect("add_class")

	max_students = request.form['max_students']
	try:
		max_students = int(max_students)
	except:
		return redirect("add_class")
	prof = request.form['prof']


	if 'access' in session:
		if session['access'] == 'admin':
			info = dbm.new_class(course_code,name,desc,semester,meeting_times,department,credits,max_students)
			teaching = dbm.change_teaching_u(info,prof)
			return render_template("add_class_landing.html",info=info)
		else:
			return redirect("401")
	else:
		return redirect("home")









if __name__ == '__main__':
	app.run('localhost',port=9001)