
CREATE TABLE contestant(
	x integer not null, /*changed to not null because of weird error*/
	contestant_name text not null,
	uname text not null,
	pass text not null,
	admin integer
);

CREATE TABLE questions(
	cid integer not null,
	qnum integer not null,
	qtitle text not null,
	question text not null,
	input text not null,
	output text not null
);

CREATE TABLE response(
	rid integer not null, /*changed to not null because of weird error*/
	quest_id integer not null,
	exec_time integer not null,
	success integer not null,
	pep8 integer not null,
	pylint integer not null
);

CREATE TABLE participation(
	pid integer not null, /*changed to not null because of weird error*/
	contestant_id integer not null,
	contest_id integer not null,
	response_id integer not null
);

CREATE TABLE registration(
	constest_id int not null,
	contestant_id int not null
);

CREATE TABLE contest(
	cid varchar(20),
	date varchar(20),
	time varchar(20),
	maxusers int(100)
);

/*  replacing with contestant, noting that logins
	had a 20 char limit.
CREATE TABLE logins(
	uname varchar(20),
	pass varchar(20)
);
*/