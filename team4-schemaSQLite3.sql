create table user(
	username varchar(255) primary key not null,
	password text not null,
	first_name text,
	last_name text,
	email text not null,
	is_admin integer not null,
	blocked integer not null
);
create table credit_card(
	ccnumber integer primary key not null,
	first_name text,
	last_name text,
	expiry text,
	cvv integer,
	addr_id integer not null references address(addr_id),
	username varchar(255) not null,
	foreign key (username) references user(username)
		on update cascade
		on delete cascade
);
create table address(
	addr_id integer primary key autoincrement,
	num integer,
	street text,
	city text,
	state text,
	zip integer,
	country text
);
create table attraction(
	attr_id integer primary key autoincrement,
	name text,
	description text,
	day_of_week text,
	opening_time text not null,
	closing_time text not null,
	cost integer not null,
	reserve_compulsory integer not null,
	addr_id integer not null,
	trans_name text,
	foreign key (addr_id) references address(addr_id)
		on update cascade
		on delete cascade,
	foreign key(trans_name) references public_transportation(trans_name)
);
create table public_transportation(
	trans_name varchar(255) primary key not null,
	addr_id integer not null,
	foreign key (addr_id) references address(addr_id)
		on update cascade
		on delete cascade
);
create table trip(
	conf_num integer not null,
	name text,
	start_date varchar(255) not null,
	end_date varchar(255) not null,
	booked integer not null,
	city text not null,
	total_cost integer,
	username varchar(255) not null,
	foreign key (username) references user(username)
		on update cascade
		on delete cascade,
	primary key (conf_num, username)
);
create table activity(
	activity_id integer,
	start_time varchar(255) not null,
	end_time varchar(255) not null,
	conf_num integer not null,
	cost integer,
	attr_id integer not null,
	start_datetime varchar(255),
	reserve_num integer,
	num_in_party integer not null,
	foreign key (conf_num) references trip(conf_num)
		on update cascade
		on delete cascade,
	foreign key (attr_id) references attraction(attr_id)
		on update cascade
		on delete cascade,
	foreign key(start_datetime) references time_slot(start_datetime),
	primary key(activity_id, conf_num)
);
create table time_slot(
	start_datetime varchar(255) not null,
	end_datetime varchar(255) not null,
	quantity integer not null,
	attr_id integer not null,
	foreign key (attr_id) references attraction(attr_id)
		on update cascade
		on delete cascade,
	primary key (start_datetime, attr_id)
);
create table review(
	date_time varchar(255) not null,
	title text,
	body text,
	username varchar(255) not null,
	attr_id integer not null,
	foreign key (username) references user(username)
		on update cascade
		on delete cascade,
	foreign key (attr_id) references attraction(attr_id)
		on update cascade
		on delete cascade,
	primary key (date_time, username, attr_id)
);
create table user_addr(
	username varchar(255) not null,
	addr_id integer not null,
	foreign key (username) references user(username)
		on update cascade
		on delete cascade,
	foreign key (addr_id) references address(addr_id)
		on update cascade
		on delete cascade,
	primary key(username, addr_id)
);
