import random
from sqlalchemy import create_engine, func, not_, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import exc
from datetime import datetime
from passlib.hash import sha256_crypt
import string

class DBManager:
	def __init__(self,uname,pwd):
		Base = automap_base()

		engine = create_engine('mysql://{}:{}@localhost/ECE464_datahel'.format(uname,pwd))

		Base.prepare(engine, reflect=True)

		self.users = Base.classes.users
		self.students = Base.classes.students
		self.classes = Base.classes.classes
		self.professors = Base.classes.professors
		self.administrators = Base.classes.administrators
		self.teaching = Base.classes.teaching
		self.taking = Base.classes.taking
		self.planned = Base.classes.planned

		self.session = Session(engine)
		self.conn = engine.connect()

		random.seed(datetime.now())

	def new_user(self,ssn,name,address,DOB):
		k = None
		for _ in range(100):
			fname,lname = name.split(' ')
			uname = fname[0].lower()+lname[:7].lower()
			if k:
				uname += str(k)
				k += 1
			else:
				k = 1

			email = uname+'@cooper.edu'

			password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
			passhash = sha256_crypt.encrypt(password)

			# TODO: fix this so its not absolute garbage lol

			new_user = self.users(ssn=ssn, uname=uname, password=passhash,name=name,email=email,
									address=address,date_of_birth=DOB)

			self.session.add(new_user)

			try:
				self.session.commit()
				return new_user.uid,new_user.uname, new_user.email, password
			except exc.IntegrityError, e:
				self.session.rollback()
				if '\'ssn\'' in e.orig.args[1]:
					raise ValueError('Duplicate SSN!')
				elif '\'email\'' in e.orig.args[1]:
					continue
				else:
					break
		raise TimeoutError('Too many attempts')

	def new_student(self, ssn, name, address, DOB, major, grad, uid=None):
		if uid:
			new_student = self.students(sid=None, uid=uid, major=major, graduation=grad)
			self.session.add(new_student)
			self.session.commit()
			return
		uid, uname, email, password = self.new_user(ssn, name, address, DOB)
		new_student = self.students(sid=None, uid=uid, major=major, graduation=grad)
		self.session.add(new_student)
		self.session.commit()
		return uid, uname, email, password

	def new_professor(self,ssn, name, address, DOB, department, salary, uid=None):
		if uid:
			new_professor = self.professors(pid=None, uid=uid, department=department, salary=salary)
			self.session.add(new_professor)
			self.session.commit()
			return
		uid, uname, email, password = self.new_user(ssn, name, address, DOB)
		new_professor = self.professors(pid=None, uid=uid, department=department, salary=salary)
		self.session.add(new_professor)
		self.session.commit()
		return uid, uname, email, password		

	def new_administrator(self,ssn, name, address, DOB, uid=None):
		if uid:
			new_administrator = self.administrators(sid=None, uid=uid, department=department)
			self.session.add(new_professor)
			self.session.commit()
			return
		uid, uname, email, password = self.new_user(ssn, name, address, DOB)
		new_administrator = self.administrators(sid=None, uid=uid, department=department)
		self.session.add(new_administrator)
		self.session.commit()
		return uid, uname, email, password			

	def new_class(self,course_code, name, description, semester, meeting_times, department, credits, max_students):
		new_class = self.classes(name=name,semester=semester,meeting_times=meeting_times,department=department,credits=credits,max_students=max_students)
		self.session.add(new_class)
		self.session.commit()
		return new_class.cid

	def change_password(self, uid, old_pwd, new_pwd):
		user = self.session.query(self.users).filter(self.users.uid==uid).one()
		if sha256_crypt.verify(old_pwd, user.password):
			raise ValueError('Wrong password')
		user.password = sha256_crypt.encrypt(new_pwd)
		self.session.commit()

	def get_gpa(self,uid):
		# gpa_query = "SELECT SUM(t.grade*c.credits)/SUM(c.credits) FROM (taking t JOIN students s ON t.sid=s.uid AND t.grade IS NOT NULL AND s.uid=\"{}\") \
		# 			JOIN classes c ON t.cid=c.cid;".format(sid)
		gpa = self.session.query(func.sum(self.taking.grade*self.classes.credits)/func.sum(self.classes.credits)).select_from(self.taking).filter(self.taking.sid==uid,self.taking.grade.isnot(None)).join(self.classes).one()[0]
		return gpa

	def get_roster(self,cid):
		# roster_query = "SELECT s.name,s.email,s.major FROM taking t JOIN students s on t.sid=s.uid and t.cid=\"{}\";".format(cid)
		roster = self.session.query(self.users.name,self.users.email,self.students.major).select_from(self.users).join(self.students).join(self.taking).filter(self.taking.cid==cid).all()

		return roster

	def authenticate(self,uname,pwd,utype):
		if utype == 'students':
			utable = self.students
		elif utype == 'professors':
			utable = self.professors
		elif utype == 'administrators':
			utable = self.administrators
		else:
			raise ValueError('Invalid user type!')

		passhash = self.session.query(self.users.uid,self.users.password).select_from(self.users).join(utable).filter(self.users.uname==uname).one()
		
		if sha256_crypt.verify(pwd, passhash[1]):
			return passhash[0]
		return

	def enrol(self,uid,cid):
		seatstaken = self.session.query(func.count(self.taking.sid)).filter(self.taking.cid==cid).scalar()
		totalseats = self.session.query(self.classes.max_students).filter(self.classes.cid==cid).scalar()
		alreadytaken = self.session.query(func.count(self.taking.sid)).filter(self.taking.sid==uid).filter(self.taking.cid==cid).scalar()
		if totalseats - seatstaken > 0:
			if alreadytaken > 0:
				new_taking = self.taking(taid = None,sid=uid,cid=cid)
				self.session.add(new_taking)
				try:
					self.session.commit()
					return
				except MySQLdb.Error, e:
					return e.args
			else:
				raise ValueError("You cannot enroll in a class twice")
		else:
			raise ValueError("No more Seats Available: Not Enrolled")

	def drop(self,uid,cid):
		obj = self.session.query(self.taking).filter(self.taking.sid==uid).filter(self.taking.cid==cid).all()
		if len(obj) != 0:
			self.session.delete(obj[0])
			try:
				self.session.commit()
			except:
				raise ValueError("something went wrong: contact Isaac Alboucai at (555)-555-5555 to get it fixed")
		else:
			raise KeyError("The user/class pair does not exist")

	def plan(self,uid,cid):
		new_plan = self.planned(plid = None,sid=uid,cid=cid)
		self.session.add(new_plan)
		try:
			self.session.commit()
		except:
			raise ValueError("something went wrong: contact Isaac Alboucai at (555)-555-5555 to get it fixed")

	def unplan(self,uid,cid):
		obj = self.session.query(self.planned).filter(self.planned.sid==uid).filter(self.planned.cid==cid).all()
		if len(obj) != 0:
			self.session.delete(obj[0])
			try:
				self.session.commit()
			except:
				raise ValueError("something went wrong: contact Isaac Alboucai at (555)-555-5555 to get it fixed")
		else:
			raise KeyError("The user/class pair does not exist")

	def enrol_in_plan(self,uid):
		plans = self.session.query(self.planned.cid).filter(self.planned.sid==uid).all()
		for plan in plans:
			self.enrol(uid,plan[0])

	def get_plan_schedule(self,sid,semester):
		classes = self.session.query(self.classes.cid,self.classes.name,self.classes.semester,self.classes.meeting_times,
								self.classes.department,self.classes.credits,self.planned.sid).select_from(self.classes).join(self.planned).filter(
								self.taking.sid==sid and self.classes.semester==semester).all()
		cids = [cl[0] for cl in classes]
		profs = self.session.query(self.teaching.cid,self.teaching.pid,self.users.name).select_from(self.teaching).join(self.professors).join(
									self.users).filter(self.teaching.cid.in_(cids)).all()
		output = [list(cl)+[prof[2]] for prof in profs for cl in classes if cl[0] == prof[0]]
			
		return output	

	def change_salary(self,uid,new_salary):
		professor = self.session.query(self.professors).filter(self.professors.uid==uid).one()
		professor.salary = new_salary
		try:
			self.session.commit()
		except:
			raise NotImplementedError

	def get_schedule(self,sid,semester):
		classes = self.session.query(self.classes.cid,self.classes.course_code,self.classes.name,self.classes.description,self.classes.semester,self.classes.meeting_times,
								self.classes.department,self.classes.credits,self.taking.sid).select_from(self.classes).join(self.taking).filter(
								self.taking.sid==sid and self.classes.semester==semester).all()
		cids = [cl[0] for cl in classes]
		profs = self.session.query(self.teaching.cid,self.teaching.pid,self.users.name).select_from(self.teaching).join(self.professors).join(
									self.users).filter(self.teaching.cid.in_(cids)).all()
		output = [list(cl)+[prof[2]] for prof in profs for cl in classes if cl[0] == prof[0]]
			
		return output			

	def get_class_info(self,cid):
		cla = self.session.query(self.classes.cid,self.classes.name,self.classes.semester,self.classes.meeting_times,
								self.classes.department,self.classes.credits).filter(self.classes.cid==cid).one()
		return cla


	def get_grades(self,sid, semester=None):
		if semester == None:
			result = self.session.query(self.classes.cid,self.classes.course_code,self.classes.name,self.classes.semester,self.taking.grade,self.classes.credits).select_from(self.taking).join(
				self.classes).filter(self.taking.sid==sid).order_by(self.classes.semester,self.classes.cid).all()
		else:
			result = self.session.query(self.classes.cid,self.classes.course_code,self.classes.name,self.classes.semester,self.taking.grade,self.classes.credits).select_from(self.taking).join(
				self.classes).filter(self.taking.sid==sid).filter(self.classes.semester==semester).order_by(self.classes.semester,self.classes.cid).all()	
		return result


	def get_prof_info(self,uid):
		prof_info = self.session.query(self.users.name,self.users.ssn,self.users.email,self.users.address,self.users.date_of_birth,
										self.professors.department,self.professors.salary).select_from(self.users).join(self.professors).filter(
										self.users.uid==uid).all()
		return prof_info

	def get_student_info(self,uid):
		stud_info = self.session.query(self.users.name,self.users.ssn,self.users.email,self.users.address,self.users.date_of_birth,
										self.students.major,self.students.graduation).select_from(self.users).join(self.students).filter(
										self.users.uid==uid).all()
		return stud_info
		

	def get_admin_info(self,uid):
		admin_info = self.session.query(self.users.name,self.users.ssn,self.users.email,self.users.address,self.users.date_of_birth
										).select_from(self.users).join(self.administrators).filter(self.users.uid==uid).all()
		return admin_info
		

if __name__ == '__main__':
	dbm = DBManager('root','')
	schedule = dbm.get_schedule(1,"Fall 2018")
	#def new_class(self,course_code, name, description, semester, meeting_times, department, credits, max_students):
	dbm.new_class("ME395","Thermodynamics","Another Thermo Course","Spring 2019","Wed 2-5", "Mechanical Engineering",3.0,25)
	dbm.new_class("ME412","Autonomous Mobile Robots","ROBOTS!!!","Spring 2019","Thurs 6-9", "Mechanical Engineering",3.0,25)
	dbm.new_class("ECE161","Programming Languages","POINTERS!!","Spring 2019","Mon 2-5", "Electrical Engineering",3.0,25)
	dbm.new_class("ECE150","Digital Logic Design","NO SLEEP FOR YOU!!","Spring 2019","Tues 2-5", "Electrical Engineering",3.0,30)
	dbm.new_class("ECE335","Engineering Electromagnetics","Some Gabario!","Spring 2019","Thurs 8-11", "Electrical Engineering",3.0,25)
	dbm.new_class("ME395","Thermodynamics","Another Thermo Course","Spring 2017","Wed 2-5", "Mechanical Engineering",3.0,25)
	dbm.new_class("ME412","Autonomous Mobile Robots","ROBOTS!!!","Spring 2017","Thurs 6-9", "Mechanical Engineering",3.0,25)
	dbm.new_class("ECE161","Programming Languages","POINTERS!!","Spring 2017","Mon 2-5", "Electrical Engineering",3.0,25)
	dbm.new_class("ECE150","Digital Logic Design","NO SLEEP FOR YOU!!","Spring 2017","Tues 2-5", "Electrical Engineering",3.0,30)
	dbm.new_class("ECE335","Engineering Electromagnetics","Some Gabario!","Spring 2017","Thurs 8-11", "Electrical Engineering",3.0,25)

	import pdb
	pdb.set_trace()

