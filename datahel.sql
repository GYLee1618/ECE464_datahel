CREATE TABLE users(uid int NOT NULL AUTO_INCREMENT,
	ssn INT, 
	uname CHAR(30) NOT NULL,
	password CHAR(32) NOT NULL,
	name CHAR(30) NOT NULL,
	email CHAR(30),
	address CHAR(64),
	date_of_birth DATETIME,
	PRIMARY KEY (uid),
	UNIQUE (ssn),
	UNIQUE (email))

CREATE TABLE students ( sid INT NOT NULL AUTO_INCREMENT,
	uid INT,
	major CHAR(32),
	graduation CHAR(32),
	FOREIGN KEY (uid) REFERENCES users,
	PRIMARY KEY(sid)
);

CREATE TABLE professors ( pid INT NOT NULL AUTO_INCREMENT,
	uid INT,
	department CHAR(32),
	salary FLOAT,
	FOREIGN KEY (uid) REFERENCES users,
	PRIMARY KEY (pid)
);

CREATE TABLE administrators ( aid INT NOT NULL AUTO_INCREMENT,
	uid INT,
	FOREIGN KEY (uid) REFERENCES users,
	PRIMARY KEY (aid)
);

CREATE TABLE classes(cid INT NOT NULL,
	name CHAR(16),	
	semester CHAR(16),
	meeting_times CHAR(32),
	department CHAR(32),
	credits FLOAT,
	max_students INT,
	PRIMARY KEY (cid)
);

CREATE TABLE teaching ( teid INT  NOT NULL AUTO_INCREMENT,
	pid INT,
	cid INT,
	PRIMARY KEY (teid),
	FOREIGN KEY (pid) REFERENCES professors(pid),
	FOREIGN KEY (cid) REFERENCES classes(cid)
);

CREATE TABLE taking ( taid INT NOT NULL AUTO_INCREMENT,
	sid INT,
	cid INT,
	grade FLOAT,
	PRIMARY KEY (taid),
	FOREIGN KEY (cid) REFERENCES classes(cid),
	FOREIGN KEY (sid) REFERENCES students(sid),
	CHECK (grade <= 4),
	CHECK (grade >= 0)
);


insert into users values (0, '605349104', 'mhes', 'QI9d0qIceG', 'Margaret Hes', 'mhes@cooper.edu', '5402 Pankowski St, Houston, TX 77036', '19980829');
insert into students values (0, 0, 'Architecture', )

insert into students values (252, '605349104', 'mhes', 'QI9d0qIceG', 'Margaret Hes', 'mhes@cooper.edu', '5402 Pankowski St, Houston, TX 77036', '19980829', 'Architecture');
insert into students values (2564, '139840649', 'eangerho', '57NIoGgRXp', 'Elizabeth Angerhofer', 'eangerho@cooper.edu', '240 Vantuyle St, Pittsfield, MA 01201', '19990112', 'Electrical Engineering');

insert into professors values (825, '704452583', 'jlyrek', '4qIvktm7mV', 'James Lyrek', 'jlyrek@cooper.edu', '7543 Koomen St, Augusta, GA 30906', '19990327', 'Architecture', 132450.8);
insert into professors values (2460, '916460110', 'kfoxhall', 'tTprsmnXhf', 'Kyle Foxhall', 'kfoxhall@cooper.edu', '5034 Wiitanen St, Fullerton, CA 92833', '20000121', 'Physics', 52543.89);
insert into professors values (199, '515943776', 'jcicio', 'hT0PxXaYpH', 'Jose Cicio', 'jcicio@cooper.edu', '4934 Mikota St, Ashburn, VA 20147', '19981112', 'General Engineering', 93610.61);
insert into professors values (1526, '683576277', 'lhaythor', '0sprf84gkS', 'Linda Haythorn', 'lhaythor@cooper.edu', '8795 Iannetta St, Elizabethtown, KY 42701', '19980917', 'Civil Engineering', 156244.22);
insert into professors values (1351, '764586958', 'jyelen', 'gKK1Qe64r4', 'Jonathan Yelen', 'jyelen@cooper.edu', '2113 Bougher St, Hialeah, FL 33010', '19981001', 'Electrical Engineering', 191962.41);
insert into professors values (3354, '354349888', 'jenswort', 'CkKdAT0WeJ', 'Eugene Sokolov', 'jenswort@cooper.edu', '2259 Schmoekel St, Winston Salem, NC 27107', '19980204', 'Electrical Engineering', 141718.01);
insert into professors values (1225, '977071612', 'gguder', '8FjSTiwJ1i', 'Gary Guder', 'gguder@cooper.edu', '7307 Lamper St, Gardena, CA 90247', '20000507', 'Mechanical Engineering', 97038.07);
insert into professors values (2386, '622405950', 'skoceja', 'FcKoZWxEHn', 'Samuel Koceja', 'skoceja@cooper.edu', '5992 Vasek St, Monroe Township, NJ 08831', '19991224', 'General Engineering', 32200.67);
insert into professors values (2304, '379004848', 'jbaesman', 'SMsbuAco6w', 'Jacob Baesman', 'jbaesman@cooper.edu', '5143 Teta St, Desoto, TX 75115', '19990812', 'Art', 107848.68);
insert into professors values (322, '863250326', 'jmerline', 'wQxxp9SacN', 'Julie Merline', 'jmerline@cooper.edu', '4577 Hoepf St, New York, NY 10023', '19971112', 'Hummanities', 144626.83);

insert into classes values (540, 'ECE464', 'Fall 2018', 'Tue 1800-2050','Electrical Engineering' , 3.0, 30);
insert into classes values (2231, 'SS351', 'Fall 2018', 'Tue 0900-1150','Hummanities', 3.0, 20);
insert into classes values (227, 'ECE464', 'Fall 2016', 'Wed 1600-1750, Thu 1200-1250','Electrical Engineering', 3.0, 30);
insert into classes values (1423, 'PH112', 'Spring 2019', 'Wed 0900-1050, Fri 1200-1350','Physics', 4.0, 20);
insert into classes values (2001, 'EID103', 'Spring 2019', 'Wed 1600-1750, Fri 1000-1150','General Engineering', 3.0, 20);
insert into classes values (1111, 'ARCH011', 'Spring 2019', 'Wed 1600-1750, Fri 1000-1150','Architecture', 4.0, 30);
insert into classes values (1231, 'ECE471', 'Fall 2018', 'Thu 1800-2050','Electrical Engineering', 3.0, 30);

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
