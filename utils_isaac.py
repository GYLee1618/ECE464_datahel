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
		try:
			obj = self.session.query().filter(self.taking.sid==sid).filter(self.taking.cid==cid).one
			self.session.delete(obj)
			self.session.commit()
		except:
		

	def change_salary(self,uid, new_salary):
		raise NotImplementedError

	def get_schedule(self,sid,semester):
		raise NotImplementedError

	def get_grades(self,sid, semeter=None):
		raise NotImplementedError

	def get_class_info(self,cid):	
		raise NotImplementedError

	def get_prof_info(self,pid):
		raise NotImplementedError

	def get_student_info(self,sid):
		raise NotImplementedError

	def get_admin_info(self,uid):
		raise NotImplementedError