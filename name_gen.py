import pandas as pd
import random
from datetime import datetime
import string
from uszipcode import SearchEngine, Zipcode

first_names = pd.read_csv("new-top-firstNames.csv")['name'].values
last_names = pd.read_csv("surnames.csv")['name'].values

search = SearchEngine(simple_zipcode=True)

zipcodes = search.by_population(lower=0, upper=999999999,sort_by=Zipcode.population, ascending=False, returns=1000)

def generate_names(first_names,last_names,n):
	names = []
	for i in range(n):
		rng_f = random.randint(0,len(first_names)-1)
		rng_l = random.randint(0,len(last_names)-1)
		names += ["{} {}".format(first_names[rng_f].title(),last_names[rng_l].title())]
	return names

names = generate_names(first_names,last_names,50)

sentries = list()
sids = set()
ssns = set()
emails = set()

majors = ['Electrical Engineering','Mechanical Engineering','Chemical Engineering',
			'Civil Engineering','General Engineering','Architecture','Art']

departments = ['Electrical Engineering','Mechanical Engineering','Chemical Engineering',
				'Civil Engineering','General Engineering','Architecture','Art','Physics',
				'Math','Hummanities']

days = [None,31,28,31,30,31,30,31,31,30,31,30,31]
ldays = [None,31,29,31,30,31,30,31,31,30,31,30,31]

for name in names:
	sid = random.randint(0,4095)
	while sid in sids:
		sid = random.randint(0,4095)
	sids.add(sid)

	ssn = "{:9d}".format(random.randint(0,999999999))
	while ssn in ssns:
		ssn = "{:9d}".format(random.randint(0,999999999))
	ssns.add(ssn)

	year = random.randint(1997,2000)
	month = random.randint(1,12)
	if year != 2000:
		day = random.randint(1,days[month])
	else:
		day = random.randint(1,ldays[month])

	dob = datetime.strptime("{}-{}-{}".format(year,month,day),"%Y-%m-%d")
	major = majors[random.randint(0,len(majors)-1)]

	i = 1
	fname,lname = name.lower().split(' ')
	email = "{}{}@cooper.edu".format(fname[0],lname[:7])
	uname = "{}{}".format(fname[0],lname[:7])
	while email in emails:
		email = "{}{}{}@cooper.edu".format(fname[0],lname[:7],i)
		uname = "{}{}{}".format(fname[0],lname[:7],i)
		i += 1
	emails.add(email)

	password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))

	a = random.randint(1,9999)
	b = last_names[random.randint(0,len(last_names)-1)].title()
	zipcode_info = zipcodes[random.randint(0,999)].values()
	zipcode = zipcode_info[0]
	city = zipcode_info[3]

	address = "{} {} St, {} {}".format(a,b,city,zipcode)

	sentries += [(sid,ssn,uname,password,name,email,address,dob,major)]

names = generate_names(first_names,last_names,5)

pentries = list()
pids = set()

for name in names:
	pid = random.randint(0,4095)
	while pid in pids:
		pid = random.randint(0,4095)
	pids.add(pid)

	ssn = "{:9d}".format(random.randint(0,999999999))
	while ssn in ssns:
		ssn = "{:9d}".format(random.randint(0,999999999))
	ssns.add(ssn)

	year = random.randint(1997,2000)
	month = random.randint(1,12)
	if year != 2000:
		day = random.randint(1,days[month])
	else:
		day = random.randint(1,ldays[month])

	dob = datetime.strptime("{}-{}-{}".format(year,month,day),"%Y-%m-%d")
	major = departments[random.randint(0,len(departments)-1)]

	i = 1
	fname,lname = name.lower().split(' ')
	email = "{}{}@cooper.edu".format(fname[0],lname[:7])
	uname = "{}{}".format(fname[0],lname[:7])
	while email in emails:
		email = "{}{}{}@cooper.edu".format(fname[0],lname[:7],i)
		uname = "{}{}{}".format(fname[0],lname[:7],i)
		i += 1
	emails.add(email)

	password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))

	a = random.randint(1,9999)
	b = last_names[random.randint(0,len(last_names)-1)].title()
	zipcode_info = zipcodes[random.randint(0,999)].values()
	zipcode = zipcode_info[0]
	city = zipcode_info[3]

	address = "{} {} St, {} {}".format(a,b,city,zipcode)

	salary = random.randint(800000,20000000)/100

	pentries += [(pid,ssn,uname,password,name,email,address,dob,major,salary)]

dept = ['MA','ECE','EID','HSS','HUM','SS','PH','BIO','CHE','CS','ESC','FA','HTA','ME']
semesters = ['Fall','Spring']

centries = dict()
cid = set()
codes = set()



with open('datahel.sql','w') as dh:
	for entry in sentries:
		dh.write("insert into students values {};\n".format(entry))
	for entry in pentries:
		dh.write("insert into professors values {};\n".format(entry))
