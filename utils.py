import random
from sqlalchemy import create_engine, func, not_, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import exc
from datetime import datetime

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

			password = 'burp'
			# TODO: fix this so its not absolute garbage lol

			new_user = self.users(ssn=ssn, uname=uname, password=password,name=name,email=email,
									address=address,date_of_birth=DOB)

			self.session.add(new_user)

			try:
				self.session.commit()
				return new_user.uid,new_user.uname, new_user.email, new_user.password
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
			new_professor = self.professors(sid=None, uid=uid, department=department, salary=salary)
			self.session.add(new_professor)
			self.session.commit()
			return
		uid, uname, email, password = self.new_user(ssn, name, address, DOB)
		new_professor = self.professors(sid=None, uid=uid, department=department, salary=salary)
		self.session.add(new_professor)
		self.session.commit()
		return uname, email, password		

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
		return uname, email, password			

	def new_class(self, semester, meeting_times, department, credits, max_students):
		new_class = self.classes(semester=semester,meeting_times=meeting_times,department=department,credits=credits,max_students=max_students)
		self.session.add(new_class)
		self.session.commit()
		return new_class.cid

	def change_password(self, uid, old_pwd, new_pwd):
		user = self.session.query(self.users).filter(self.users.uid==uid).one()
		if user.password != old_pwd:
			raise ValueError('Wrong password')
		user.password = new_pwd
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

		return self.session.query(self.users).select_from(self.users).join(utable).filter(self.users.uname==uname).filter(self.users.password==pwd).scalar() is not None 

	def enrol(self,uid,cid):
		import pdb
		pdb.set_trace()
		seatstaken = self.session.query(func.count(self.taking.sid)).filter(self.taking.cid==cid).scalar()
		totalseats = self.session.query(self.classes.max_students).filter(self.classes.cid==cid).scalar()
		if totalseats - seatstaken > 0:
			new_taking = self.taking(taid = None,sid=uid,cid=cid)
			self.session.add(new_taking)
			try:
				self.session.commit()
				return
			except MySQLdb.Error, e:
				return e.args
		else:
			raise ValueError("No more Seats Available: Not Enrolled")

	def drop(self,uid,cid):
		obj = self.session.query(self.taking).filter(self.taking.sid==uid).filter(self.taking.cid==cid).one()
		self.session.delete(obj)
		try:
			self.session.commit()
		except:
			raise NotImplementedError

	def change_salary(self,uid,new_salary):
		professor = self.session.query(self.professors).filter(self.professors.uid==uid)
		professor.salary = new_salary
		try:
			self.session.commit()
		except:
			raise NotImplementedError

	def get_schedule(self,sid,semester):
		classes = self.session.query(self.classes.cid,self.classes.name,self.classes.semester,self.classes.meeting_times,
								self.classes.department,self.classes.credits).select_from(self.classes).join(self.taking).filter(
								self.taking.sid==sid).filter(self.taking.semester==semester)
		return classes
			

	def get_class_info(self,cid):
		cla = self.session.query(self.classes.cid,self.classes.name,self.classes.semester,self.classes.meeting_times,
								self.classes.department,self.classes.credits).filter(self.classes.cid==cid).one()
		return cla


	def get_grades(self,sid, semeter=None):
		grades = []
		if semester != None:
			result = self.session.query(self.classes.cid,self.classes.name,self.classes.semester,self.taking.grade).select_from(self.taking).join(
				self.classes).filter(self.taking.sid==sid)
		else:
			result = self.session.query(self.classes.cid,self.classes.name,self.classes.semester,self.taking.grade).select_from(self.taking).join(
				self.classes).filter(self.taking.sid==sid).filter(self.classes.semester==semester)
		return result


	def get_prof_info(self,uid):
		prof_info = self.session.query(self.users.name,self.users.ssn,self.users.email,self.users.address,self.users.date_of_birth,
										self.professors.department,self.professors.salary).select_from(self.users).join(self.professors).filter(
										self.users.uid==uid)
		return prof_info

	def get_student_info(self,uid):
		stud_info = self.session.query(self.users.name,self.users.ssn,self.users.email,self.users.address,self.users.date_of_birth,
										self.students.major,self.students.graduation).select_from(self.users).join(self.students).filter(
										self.users.uid==uid)
		return stud_info
		

	def get_admin_info(self,uid):
		admin_info = self.session.query(self.users.name,self.users.ssn,self.users.email,self.users.address,self.users.date_of_birth
										).select_from(self.users).join(self.administrators).filter(self.users.uid==uid)
		return admin_info
		

if __name__ == '__main__':
	dbm = DBManager('root','')
	sok = dbm.get_prof_info(3)
	print sok
	dbm.change_salary(3,250000.2)
	sok = dbm.get_prof_info(3)
	print sok 
	classes = dbm.get_schedule(1,"Fall 2018")
	print classes
	c1 = dbm.get_class_info(464)
	print c1
	grades = dbm.get_grades(1,"Fall 2018")
	print grades

	stud = dbm.get_student_info(1)
	print stud

	import pdb
	pdb.set_trace()

