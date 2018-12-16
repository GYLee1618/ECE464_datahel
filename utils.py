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

		self.students = Base.classes.students
		self.classes = Base.classes.classes
		self.professors = Base.classes.professors
		self.administrators = Base.classes.administrators
		self.teaching = Base.classes.teaching
		self.taking = Base.classes.taking

		self.session = Session(engine)
		self.conn = engine.connect()

		random.seed(datetime.now())


	def new_student(self,ssn, name, address, DOB, major):
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

			new_student = self.students(uid = None, ssn=ssn,uname=uname,password=password,name=name,
										email=email,address=address,date_of_birth=DOB,major=major)
			# import pdb
			# pdb.set_trace()

			self.session.add(new_student)
			try:
				self.session.commit()
				return
			except exc.IntegrityError, e:
				self.session.rollback()
				if '\'ssn\'' in e.orig.args[1]:
					raise ValueError('Duplicate SSN!')
				elif '\'email\'' in e.orig.args[1]:
					continue
				else:
					break
		raise ValueError('Could not complete')


	def new_professor(self,ssn, name, address, DOB, department, salary):
		k = None 
		for _ in range(100):
			fname,lname = name.split(' ')
			uname = fname[0].lower()+lname[:7].lower()
			if k:
				uname += str(k)
				k += 1
			else:
				k = 1

			s_emails = session.query(self.students.email).select_from(self.students)
			p_emails = session.query(self.professors.email).select_from(self.professors)
			a_emails = session.query(self.administrators.email).select_from(self.administrators)

			import pdb
			pdb.set_trace

			emails = s_emails+p_emails+a_emails

			email = uname+'@cooper.edu'

			password = 'burp'

			new_professor = self.professors(uid = None, ssn=ssn,uname=uname,password=password,name=name,
										email=email,address=address,date_of_birth=DOB,department=department,
										salary=salary)
			# import pdb
			# pdb.set_trace()

			self.session.add(new_professor)
			self.session.commit()
				return
			except exc.IntegrityError, e:
				self.session.rollback()
				if '\'ssn\'' in e.orig.args[1]:
					raise ValueError('Duplicate SSN!')
				elif '\'email\'' in e.orig.args[1]:
					continue
				else:
					break
		raise ValueError('Could not complete')

	def new_administrator(self,ssn, name, address, DOB):
		raise NotImplementedError

	def new_class(self,cid, semester, meeting_times, department, credits, max_students):
		raise NotImplementedError

	def change_password(self,uid, user_type, old_pwd, new_pwd):
		# TODO: exec query and update old pwd
		find_query = "SELECT u.password FROM \"{}\" u WHERE u.uid==\"{}\";".format(user_type,uid)

	def get_gpa(self,sid):
		gpa_query = "SELECT SUM(t.grade*c.credits)/SUM(c.credits) FROM (taking t JOIN students s ON t.sid=s.uid AND t.grade IS NOT NULL AND s.uid=\"{}\") \
					JOIN classes c ON t.cid=c.cid;".format(sid)

	def get_roster(self,cid):
		roster_query = "SELECT s.name,s.email,s.major FROM taking t JOIN students s on t.sid=s.uid and t.cid=\"{}\";".format(cid)


if __name__ == '__main__':
	dbm = DBManager('root','')
	dbm.new_student('1139284121','Isaac Alboucai','317 East 9th St, New York, NY 10003',datetime.strptime('10-12-1997','%m-%d-%Y'),'Electrical Engineering')
	dbm.new_student('1039284121','Isaac Alboucai','317 East 9th St, New York, NY 10003',datetime.strptime('10-12-1997','%m-%d-%Y'),'Electrical Engineering')
	dbm.new_student('1039284121','Isaac Alboucai','317 East 9th St, New York, NY 10003',datetime.strptime('10-12-1997','%m-%d-%Y'),'Electrical Engineering',3.50)
