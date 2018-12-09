CREATE TABLE students ( uid INT,
	ssn INT, 
	uname CHAR(30) NOT NULL,
	password CHAR(32) NOT NULL,
	name CHAR(30) NOT NULL,
	email CHAR(30),
	address CHAR(64),
	date_of_birth DATETIME,
	major CHAR(32),
	PRIMARY KEY (uid),
	UNIQUE (ssn),
	UNIQUE (email)
);

CREATE TABLE professors ( uid INT,
	ssn INT, 
	uname CHAR(30) NOT NULL,
	password CHAR(32) NOT NULL,
	name CHAR(30) NOT NULL,
	email CHAR(30),
	address CHAR(64),
	date_of_birth DATETIME,
	department CHAR(32),
	salary FLOAT,
	UNIQUE(ssn),
	UNIQUE(email),
	PRIMARY KEY (uid)
);

CREATE TABLE administrators ( uid INT,
	ssn INT, 
	uname CHAR(30) NOT NULL,
	password CHAR(32) NOT NULL,
	name CHAR(30) NOT NULL,
	email CHAR(30),
	address CHAR(64),
	Dob DATETIME,
	UNIQUE(ssn),
	UNIQUE(email),
	PRIMARY KEY (uid)
);

CREATE TABLE classes(cid INT,	
	semester CHAR(16),
	meeting_times CHAR(32),
	department CHAR(32),
	credits FLOAT,
	max_students INT,
	PRIMARY KEY (cid)
);

CREATE TABLE teaching ( teid INT,
	pid INT,
	cid INT,
	PRIMARY KEY (teid),
	FOREIGN KEY (pid) REFERENCES professors(uid),
	FOREIGN KEY (cid) REFERENCES classes(cid)
);

CREATE TABLE taking ( taid INT,
	sid INT,
	cid INT,
	grade FLOAT,
	PRIMARY KEY (taid),
	FOREIGN KEY (cid) REFERENCES classes(cid),
	FOREIGN KEY (sid) REFERENCES students(uid),
	CHECK (grade <= 4),
	CHECK (grade >= 0)
);


insert into students values (252, '605349104', 'mhes', 'QI9d0qIceG', 'Margaret Hes', 'mhes@cooper.edu', '5402 Pankowski St, Houston, TX 77036', '19980829', 'Architecture');
insert into students values (2564, '139840649', 'eangerho', '57NIoGgRXp', 'Elizabeth Angerhofer', 'eangerho@cooper.edu', '240 Vantuyle St, Pittsfield, MA 01201', '19990112', 'Electrical Engineering');
insert into students values (2010, '879595753', 'maug', 'R4Mzmm0wom', 'Michelle Aug', 'maug@cooper.edu', '9210 Living St, Frankfort, KY 40601', '19970322', 'Mechanical Engineering');
insert into students values (2386, '767224003', 'cmcgrath', 'aS1XRGAvmv', 'Christine Mcgrath', 'cmcgrath@cooper.edu', '9143 Hestand St, Yonkers, NY 10701', '19970604', 'General Engineering');
insert into students values (249, '411454262', 'avolstad', 'di5uwipSsL', 'Amy Volstad', 'avolstad@cooper.edu', '8505 Bennet St, Marysville, WA 98270', '19990313', 'Civil Engineering');
insert into students values (2750, '837999040', 'sbenik', 'MresNmh8O5', 'Sarah Benik', 'sbenik@cooper.edu', '7057 Wykoff St, Lehi, UT 84043', '19990124', 'Architecture');
insert into students values (695, '782611623', 'nplan', 'dHz8LPP6Dr', 'Nathan Plan', 'nplan@cooper.edu', '7856 Schaake St, Mesquite, TX 75150', '19970609', 'Mechanical Engineering');
insert into students values (1058, '767372672', 'jkrank', '8dIPYhXCUA', 'Justin Krank', 'jkrank@cooper.edu', '3589 Chopin St, Lakeville, MN 55044', '19971029', 'Civil Engineering');
insert into students values (625, '116678078', 'nrodecap', 'gZk3mO0XPf', 'Nicole Rodecap', 'nrodecap@cooper.edu', '565 Sakin St, Brooklyn, NY 11238', '19970524', 'General Engineering');
insert into students values (1268, '911305901', 'alundgre', '8MH8z3J7Oy', 'Angela Lundgren', 'alundgre@cooper.edu', '9232 Lacelle St, Simi Valley, CA 93063', '20000807', 'Art');
insert into students values (3441, '393036039', 'sbunte', 'RNSNXhcY6e', 'Samantha Bunte', 'sbunte@cooper.edu', '3296 Delille St, Albuquerque, NM 87114', '19991217', 'Art');
insert into students values (2366, '941859822', 'mdansky', 'T6I8iTPW11', 'Mary Dansky', 'mdansky@cooper.edu', '9026 Sandoval St, Indio, CA 92201', '19980811', 'Civil Engineering');
insert into students values (2019, '992461574', 'kmasotto', 'qLe4TbRkoJ', 'Kenneth Masotto', 'kmasotto@cooper.edu', '368 Kawlewski St, New York, NY 10033', '19990131', 'Architecture');
insert into students values (1134, '795080774', 'cnimer', 'ht3sidHTGg', 'Christine Nimer', 'cnimer@cooper.edu', '1439 Illes St, Winter Garden, FL 34787', '19990614', 'Art');
insert into students values (1207, '370551886', 'bschenbe', 'sRI2Xar1uq', 'Brenda Schenberg', 'bschenbe@cooper.edu', '4103 Strini St, Aurora, IL 60506', '20000124', 'Electrical Engineering');
insert into students values (1564, '571885944', 'mkuik', 'R4FJ3cZYzk', 'Michelle Kuik', 'mkuik@cooper.edu', '8308 Kilberg St, Lake Worth, FL 33463', '19990704', 'Art');
insert into students values (1061, '198156381', 'rprati', 'BImbTbhAIC', 'Rebecca Prati', 'rprati@cooper.edu', '7256 Kincade St, Buckeye, AZ 85326', '20000927', 'Chemical Engineering');
insert into students values (2967, '896406751', 'mcancell', 'W6pK9XofgY', 'Melissa Cancelli', 'mcancell@cooper.edu', '5543 Vacher St, Columbia, MO 65202', '20000404', 'Mechanical Engineering');
insert into students values (2748, '458257850', 'bveenker', 'qo9siGKDHK', 'Brandon Veenker', 'bveenker@cooper.edu', '344 Grinter St, Vista, CA 92084', '19990429', 'Chemical Engineering');
insert into students values (2411, '906533061', 'bpeckman', 'OmDADiLyQv', 'Benjamin Peckman', 'bpeckman@cooper.edu', '3796 Sallis St, Bothell, WA 98012', '20000901', 'General Engineering');

insert into professors values (825, '704452583', 'jlyrek', '4qIvktm7mV', 'James Lyrek', 'jlyrek@cooper.edu', '7543 Koomen St, Augusta, GA 30906', '19990327', 'Architecture', 132450.8);
insert into professors values (2460, '916460110', 'kfoxhall', 'tTprsmnXhf', 'Kyle Foxhall', 'kfoxhall@cooper.edu', '5034 Wiitanen St, Fullerton, CA 92833', '20000121', 'Physics', 52543.89);
insert into professors values (199, '515943776', 'jcicio', 'hT0PxXaYpH', 'Jose Cicio', 'jcicio@cooper.edu', '4934 Mikota St, Ashburn, VA 20147', '19981112', 'General Engineering', 93610.61);
insert into professors values (1526, '683576277', 'lhaythor', '0sprf84gkS', 'Linda Haythorn', 'lhaythor@cooper.edu', '8795 Iannetta St, Elizabethtown, KY 42701', '19980917', 'Civil Engineering', 156244.22);
insert into professors values (1351, '764586958', 'jyelen', 'gKK1Qe64r4', 'Jonathan Yelen', 'jyelen@cooper.edu', '2113 Bougher St, Hialeah, FL 33010', '19981001', 'Electrical Engineering', 191962.41);
insert into professors values (3354, '354349888', 'jenswort', 'CkKdAT0WeJ', 'Jordan Ensworth', 'jenswort@cooper.edu', '2259 Schmoekel St, Winston Salem, NC 27107', '19980204', 'Electrical Engineering', 141718.01);
insert into professors values (1225, '977071612', 'gguder', '8FjSTiwJ1i', 'Gary Guder', 'gguder@cooper.edu', '7307 Lamper St, Gardena, CA 90247', '20000507', 'Mechanical Engineering', 97038.07);
insert into professors values (2386, '622405950', 'skoceja', 'FcKoZWxEHn', 'Samuel Koceja', 'skoceja@cooper.edu', '5992 Vasek St, Monroe Township, NJ 08831', '19991224', 'General Engineering', 32200.67);
insert into professors values (2304, '379004848', 'jbaesman', 'SMsbuAco6w', 'Jacob Baesman', 'jbaesman@cooper.edu', '5143 Teta St, Desoto, TX 75115', '19990812', 'Art', 107848.68);
insert into professors values (322, '863250326', 'jmerline', 'wQxxp9SacN', 'Julie Merline', 'jmerline@cooper.edu', '4577 Hoepf St, New York, NY 10023', '19971112', 'Hummanities', 144626.83);

insert into classes values (540, 'ECE464', 'Fall 2018', 'Tue 1800-2050', 3.0, 30);
insert into classes values (2231, 'SS351', 'Fall 2018', 'Tue 0900-1150', 3.0, 20);
insert into classes values (227, 'ECE464', 'Fall 2016', 'Wed 1600-1750, Thu 1200-1250', 3.0, 30);
insert into classes values (1423, 'PH112', 'Spring 2019', 'Wed 0900-1050, Fri 1200-1350', 4.0, 20);
insert into classes values (2001, 'EID103', 'Spring 2019', 'Wed 1600-1750, Fri 1000-1150', 3.0, 20);
insert into classes values (1111, 'ARCH011', 'Spring 2019', 'Wed 1600-1750, Fri 1000-1150', 4.0, 30);
insert into classes values (1231, 'ECE471', 'Fall 2018', 'Thu 1800-2050', 3.0, 30);

insert into teaching values (201, 3354, 540);
insert into teaching values (3214, 322, 2231);
insert into teaching values (1922, 3354, 227);
insert into teaching values (802, 2460, 1423);
insert into teaching values (1401, 2386, 2001);
insert into teaching values (2789, 825, 1111);
insert into teaching values (1130, 1351, 1231);

insert into taking values (101, 2564, 540, 3);
insert into taking values (102, 2564, 1231, 4);
insert into taking values (103, 2564, 2231, 4);
insert into taking values (104, 252, 1111, NULL);
insert into taking values (105, 252, 2231, NULL);
insert into taking values (106, 2010, 1423, NULL);
insert into taking values (107, 2010, 2001, NULL);
insert into taking values (108, 2386, 2001, NULL);
insert into taking values (109, 2386, 1423, NULL);
insert into taking values (110, 249, 1423, NULL);
insert into taking values (111, 2750, 1111, NULL);
insert into taking values (112, 695, 2001, NULL);
insert into taking values (113, 1058, 1423, NULL);
insert into taking values (114, 1058, 2231, NULL);
