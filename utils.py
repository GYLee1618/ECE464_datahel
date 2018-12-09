import random
from datetime import datetime

def new_student(ssn, name, address, DOB, major):
	# TODO: exec queries

	sid = random.randint(0,4095)
	
	names = name.lower().split(' ')
	uname = "{}{}".format(names[0][0],names[-1][:7])
	email = "{}@cooper.edu".format(uname)

	password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
	# hash and salt after this

	insert_query = "INSERT INTO students VALUES {};".format((sid,ssn,uname,password,name,email,address,datetime.strftime(dob,"%Y%m%d"),major))
	# TODO: if error, find out why error and retry if error is ssn or uname clash
	# while sid in sid_list:
	# 	sid = random.randint(0,4095)
	# i = 1
	# while uname in uname_list:
	# 	uname = "{}{}{}".format(names[0][0],names[-1][:7],i)
	# 	i += 1
	# email = "{}@cooper.edu".format(uname)
	# exec insert_query

def change_password(uid, user_type="students", old_pwd, new_pwd):
	# TODO: exec query and update old pwd
	find_query = "SELECT u.password FROM \"{}\" u WHERE u.uid==\"{}\";".format(user_type,uid)


def get_gpa(sid):
	gpa_query = "SELECT SUM(t.grade*c.credits)/SUM(c.credits) FROM (taking t JOIN students s ON t.sid=s.uid AND t.grade IS NOT NULL AND s.uid=\"{}\") \
				JOIN classes c ON t.cid=c.cid;".format(sid)

def get_roster(cid):
	roster_query = "SELECT s.name,s.email,s.major FROM taking t JOIN students s on t.sid=s.uid and t.cid=\"{}\";".format(cid)


