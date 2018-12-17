CREATE TABLE users(uid int NOT NULL AUTO_INCREMENT,
	ssn INT, 
	uname CHAR(30) NOT NULL,
	password CHAR(128) NOT NULL,
	name CHAR(30) NOT NULL,
	email CHAR(30),
	address CHAR(64),
	date_of_birth DATETIME,
	PRIMARY KEY (uid),
	UNIQUE (ssn),
	UNIQUE (email)
);

CREATE TABLE students ( sid INT NOT NULL AUTO_INCREMENT,
	uid INT,
	major CHAR(32),
	graduation INT,
	FOREIGN KEY (uid) REFERENCES users(uid),
	PRIMARY KEY(sid)
);

CREATE TABLE professors ( pid INT NOT NULL AUTO_INCREMENT,
	uid INT,
	department CHAR(32),
	salary FLOAT,
	FOREIGN KEY (uid) REFERENCES users(uid),
	PRIMARY KEY (pid)
);

CREATE TABLE administrators ( aid INT NOT NULL AUTO_INCREMENT,
	uid INT,
	FOREIGN KEY (uid) REFERENCES users(uid),
	PRIMARY KEY (aid)
);

CREATE TABLE classes(cid INT NOT NULL AUTO_INCREMENT,
	course_code CHAR(16),
	name CHAR(32),	
	description TEXT,
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
	FOREIGN KEY (pid) REFERENCES professors(uid),
	FOREIGN KEY (cid) REFERENCES classes(cid)
);

CREATE TABLE taking ( taid INT NOT NULL AUTO_INCREMENT,
	sid INT,
	cid INT,
	grade FLOAT,
	PRIMARY KEY (taid),
	FOREIGN KEY (cid) REFERENCES classes(cid),
	FOREIGN KEY (sid) REFERENCES students(uid),
	CHECK (grade <= 4),
	CHECK (grade >= 0)
);

CREATE TABLE planned ( plid INT NOT NULL AUTO_INCREMENT,
	sid INT,
	cid INT,
	grade FLOAT,
	PRIMARY KEY (plid),
	FOREIGN KEY (cid) REFERENCES classes(cid),
	FOREIGN KEY (sid) REFERENCES students(uid)
);


-- insert into users values (1, '605349104', 'mhes', 'QI9d0qIceG', 'Margaret Hes', 'mhes@cooper.edu', '5402 Pankowski St, Houston, TX 77036', '19980829');
-- insert into students values (1, 1, 'Architecture', 2018);

-- insert into users values(2, '139840649', 'eangerho', '57NIoGgRXp', 'Elizabeth Angerhofer', 'eangerho@cooper.edu', '240 Vantuyle St, Pittsfield, MA 01201', '19990112');
-- insert into students values (2, 2, 'Electrical Engineering', 2019);

-- insert into users values (3, '704452583', 'esokolov', '4qIvktm7mV', 'Eugene Sokolov', 'esokolov@cooper.edu', '7543 Koomen St, Augusta, GA 30906', '19990327');
-- insert into professors values (1, 3, 'Electrical Engineering', 132450.8);

-- insert into users values (4, '916460110', 'kfoxhall', 'tTprsmnXhf', 'Kyle Foxhall', 'kfoxhall@cooper.edu', '5034 Wiitanen St, Fullerton, CA 92833', '20000121');
-- insert into professors values (2, 4, 'Physics', 52543.89);

