import random
from sqlalchemy import create_engine, func, not_, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from datetime import datetime

def setup(uname,pwd):
	Base = automap_base()

	engine = create_engine('mysql://{}:{}@localhost/ECE464_datahel'.format(uname,pwd))

	Base.prepare(engine, reflect=True)

	students = Base.classes.students
	classes = Base.classes.classes
	professors = Base.classes.professors
	administrators = Base.classes.administrators
	teaching = Base.classes.teaching
	taking = Base.classes.taking

	session=Session(engine)
	conn = engine.connect()

	return session,students,classes,professors,administrators,teaching,taking

def new_student(ssn, name, address, DOB, major):
	# TODO: exec queries

	sid = random.randint(0,4095)
	
	names = name.lower().split(' ')
	uname = "{}{}".format(names[0][0],names[-1][:7])
	email = "{}@cooper.edu".format(uname)

	password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
	# hash and salt after this

	
	# TODO: if error, find out why error and retry if error is ssn or uname clash
	# while sid in sid_list:
	# 	sid = random.randint(0,4095)
	# i = 1
	# while uname in uname_list:
	# 	uname = "{}{}{}".format(names[0][0],names[-1][:7],i)
	# 	i += 1
	# email = "{}@cooper.edu".format(uname)
	# exec insert_query

def new_professor(ssn, name, address, DOB, department, salary):
	raise NotImplementedError

def new_administrator(ssn, name, address, DOB):
	raise NotImplementedError

def new_class(cid, semester, meeting_times, department, credits, max_students)
	raise NotImplementedError

def change_password(uid, user_type, old_pwd, new_pwd):
	# TODO: exec query and update old pwd
	find_query = "SELECT u.password FROM \"{}\" u WHERE u.uid==\"{}\";".format(user_type,uid)

def get_gpa(sid):
	gpa_query = "SELECT SUM(t.grade*c.credits)/SUM(c.credits) FROM (taking t JOIN students s ON t.sid=s.uid AND t.grade IS NOT NULL AND s.uid=\"{}\") \
				JOIN classes c ON t.cid=c.cid;".format(sid)

def get_roster(cid):
	roster_query = "SELECT s.name,s.email,s.major FROM taking t JOIN students s on t.sid=s.uid and t.cid=\"{}\";".format(cid)

def enrol(sid,cid):
	raise NotImplementedError

def drop(sid,cid):
	raise NotImplementedError

def change_salary(uid, new_salary):
	raise NotImplementedError

def get_schedule(sid,semester):
	raise NotImplementedError

def get_grades(sid, semeter=None):
	raise NotImplementedError

def get_class_info(cid)
:	raise NotImplementedError

def get_prof_info(pid):
	raise NotImplementedError

def get_student_info(sid):
	raise NotImplementedError

def get_admin_info(uid):
	raise NotImplementedError

