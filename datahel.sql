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


insert into users values (1, '605349104', 'mhes', 'QI9d0qIceG', 'Margaret Hes', 'mhes@cooper.edu', '5402 Pankowski St, Houston, TX 77036', '19980829');
insert into students values (1, 1, 'Architecture', 2018);

insert into users values(2, '139840649', 'eangerho', '57NIoGgRXp', 'Elizabeth Angerhofer', 'eangerho@cooper.edu', '240 Vantuyle St, Pittsfield, MA 01201', '19990112');
insert into students values (2, 2, 'Electrical Engineering', 2019);

insert into users values (3, '704452583', 'jlyrek', '4qIvktm7mV', 'Eugene Sokolov', 'esokolov@cooper.edu', '7543 Koomen St, Augusta, GA 30906', '19990327');
insert into professors values (1, 3, 'Electrical Engineering', 132450.8);

insert into users values (4, '916460110', 'kfoxhall', 'tTprsmnXhf', 'Kyle Foxhall', 'kfoxhall@cooper.edu', '5034 Wiitanen St, Fullerton, CA 92833', '20000121');
insert into professors values (2, 4, 'Physics', 52543.89);

insert into classes values (464, 'ECE464', 'Fall 2018', 'Tue 1800-2050','Electrical Engineering' , 3.0, 30);
insert into classes values (2231, 'PH351', 'Fall 2018', 'Tue 0900-1150','Physics', 3.0, 20);
insert into classes values (227, 'ECE464', 'Fall 2016', 'Wed 1600-1750, Thu 1200-1250','Electrical Engineering', 3.0, 30);

insert into teaching values (1, 3, 464);
insert into teaching values (2, 4, 2231);
insert into teaching values (3, 3, 227);

insert into taking values (1, 2, 227, 3);
insert into taking values (2, 2, 2231, NULL);
insert into taking values (3, 1, 2231, NULL);

