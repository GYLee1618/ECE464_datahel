insert into classes values (464, 'ECE464', 'Databases', 'Learn about SQL and NoSQL Databases', 'Fall 2018', 'Tue 1800-2050','Electrical Engineering' , 3.0, 30);
insert into classes values (2231, 'PH351', 'Fluids', 'Learn about liquids and gasses', 'Fall 2018', 'Tue 0900-1150','Physics', 3.0, 20);
insert into classes values (227, 'ECE464', 'Databases', 'Learn about SQL and NoSQL Databases', 'Fall 2016', 'Wed 1600-1750, Thu 1200-1250','Electrical Engineering', 3.0, 30);

insert into teaching values (1, 3, 464);
insert into teaching values (2, 4, 2231);
insert into teaching values (3, 3, 227);

insert into taking values (1, 2, 464, 3);
insert into taking values (4, 1, 227, 2);
insert into taking values (2, 2, 2231, NULL);
insert into taking values (3, 1, 2231, NULL);
