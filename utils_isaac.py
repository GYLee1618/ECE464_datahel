	def enrol(self,sid,cid):
		seatstaken = self.session.query(func.count(self.taking.sid)).filter(self.taking.cid==cid)
		totalseats = self.session.query(self.classes.max_students).filter(self.taking.cid==cid)
		if totalseats - seatstaken > 0:
			new_taking = self.taking(taid = None,sid=sid,cid=cid)
			self.session.add(new_taking)
			try:
				self.session.commit()
				return
			except MySQLdb.Error, e:
        		return e.args
		else:
			raise ValueError("No more Seats Available: Not Enrolled")

	def drop(self,sid,cid):
		obj = self.session.query(self.taking).filter(self.taking.sid==sid).filter(self.taking.cid==cid).one()
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
								self.classes.department,self.classes.credits).select_from(self.classes).join(self.taking)
								.filter(self.taking.sid==sid).filter(self.taking.semester==semester)
		return classes
			

	def get_class_info(self,cid):
		cla = self.session.query(self.classes.cid,self.classes.name,self.classes.semester,self.classes.meeting_times,
								self.classes.department,self.classes.credits)
								.filter(self.classes.cid==cid).one()
		return cla


	def get_grades(self,sid, semeter=None):
		grades = []
		if semester != None:
			result = self.session.query(self.classes.cid,self.classes.name,self.classes.semester,self.taking.grade).select_from(self.taking)
					.join(self.classes).filter(self.taking.sid==sid)
		else:
			result = self.session.query(self.classes.cid,self.classes.name,self.classes.semester,self.taking.grade).select_from(self.taking)
					.join(self.classes).filter(self.taking.sid==sid).filter(self.classes.semester==semester)
		return result


	def get_prof_info(self,uid):
		prof_info = self.session.query(self.users.name,self.users.ssn,self.users.email,self.users.address,self.users.dob
										self.professors.dept,self.professors.salary).select_from(self.users).join(self.professors)
										.filter(self.users.uid==uid)
		return prof_info

	def get_student_info(self,uid):
		stud_info = self.session.query(self.users.name,self.users.ssn,self.users.email,self.users.address,self.users.dob
										self.students.major,self.students.graduation).select_from(self.users).join(self.students)
										.filter(self.users.uid==uid)
		return stud_info
		

	def get_admin_info(self,uid):
		admin_info = self.session.query(self.users.name,self.users.ssn,self.users.email,self.users.address,self.users.dob
										).select_from(self.users).join(self.administrators)
										.filter(self.users.uid==uid)
		return admin_info
		


















