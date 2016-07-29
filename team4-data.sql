drop schema if exists team4;
create schema team4;
use team4;
create table user(
	username varchar(255) primary key not null,
	password text not null,
	first_name text,
	last_name text,
	email text not null,
	is_admin int not null,
	blocked int not null
);

insert into user values ("ngainey","eagle1","Nick","Gainey","ngainey3@gatech.edu",1,0);
insert into user values ("jgreen","falcon8","John","Green","jgreen96@gatech.edu",1,0);
insert into user values ("tjoyce","iheartcs","Travis","Joyce","travisjoyce50@gatech.edu",0,1);
insert into user values ("rsengupta","thecurse","Ribhu","Sengupta","rsengupta8@gatech.edu",0,0);
insert into user values ("mkeezer","gucci","Matthew","Keezer","mkeezer3@gatech.edu",1,0);
insert into user values ("username","password","John","Doe","jdoe3@gatech.edu",0,0);

create table credit_card(
	ccnumber varchar(255) primary key not null,
	first_name text,
	last_name text,
	expiry text,
	cvv int,
	addr_id int not null references address(addr_id),
	username varchar(255) not null,
	foreign key (username) references user(username)
		on update cascade
		on delete cascade
);

insert into credit_card values (12345678,"Nick","Gainey","01/17",001,1,"ngainey");
insert into credit_card values (23456789,"John","Green","02/17",002,2,"jgreen");
insert into credit_card values (34567890,"Travis","Joyce","02/18",003,3,"tjoyce");
insert into credit_card values (45678901,"Ribhu","Sengupta","07/19",345,4,"rsengupta");
insert into credit_card values (56789012,"Matthew","Keezer","11/18",761,5,"mkeezer");
insert into credit_card values (67890123,"John","Doe","12/19",959,6,"username");


create table address(
	addr_id int primary key not null auto_increment,
	num int,
	street text,
	city text,
	state text,
	zip int,
	country text
);

insert into address values (1,12,"Schroeder Court","Carrollton","GA",30116,"USA");
insert into address values (2,23,"Korver Street","Suwanee","GA",30024,"USA");
insert into address values (3,34,"Bazemore Lane","Carrollton","GA",30117,"USA");
insert into address values (4,45,"Millsap Drive","Boston","MA",22108,"USA");
insert into address values (5,56,"Howard Boulevard","Savannah","GA",30332,"USA");
insert into address values (6,67,"Main Street","Seattle","WA", 86753,"USA");
insert into address values (7,1,"Rue de la Citadelle","Metz","Lorraine",57000,"USA");
insert into address values (8,1,"Parvis des Droits de l'Homme","Metz","Lorraine",57020,"USA");
insert into address values (9,1,"Place d'Armes","Metz","Lorraine",57000,"USA");
insert into address values (10,6,"Parvis Notre-Dame","Paris","Ile-de-France",75004,"France");
insert into address values (11,5,"Avenue Anatole","Paris","Ile-de-France",75007,"France");
insert into address values (12,35,"Rue du Chevalier","Paris","Ile-de-France",75018,"France");
insert into address values (13,1,"Piazza del Colosseo","Rome","Lazio",00184,"Italy");
insert into address values (14,1,"Piazza della Rotonda","Rome","Lazio",00186,"Italy");
insert into address values (15,1,"Piazza del Trevi","Rome","Lazio",00187,"Italy");	
insert into address values (16,18,"Rue de Dunkerque","Paris","Ile-de-France",75010,"France");
insert into address values (17,2,"Rue Marconi","Metz","Lorraine",57070,"France");

create table attraction(
	attr_id int primary key not null auto_increment,
	name text,
	description text,
	days_open text,
	opening_time text not null,
	closing_time text not null,
	cost int not null,
	reserve_compulsory int not null,
	addr_id int not null,
	foreign key (addr_id) references address(addr_id)
		on update cascade
		on delete cascade,
	trans_name text references public_transportation(trans_name)
);

insert into attraction values (1,"Basilica of Saint-Pierre-aux-Nonnains",
	"A pre-medieval church originally made as a Roman gymnasium in the 4th century AD. 
	It is one of the oldest churches in Europe.", "Sunday, Saturday", "10:00","18:00",
	0,0,7, "Provence");
insert into	attraction values (2,"Centre Pompidou-Metz","Popular modern and 
	contempory art venue located in Metz. Since its birth in 2010 it has gained 
	widespread notority and is a major cultural venue of eastern France.", "Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday", "10:00","18:00",12,0,8,"Centre Pompidou");
insert into attraction values (3,"Metz Cathedral","Known by the locals as 
	Saint-Etienne de Metz, this historical cathedral seats the bishop of Metz. 
	Being one of the highest naves in the world the cathedral is nicknamed the 
	Good Lord's Lantern and displays the largest expanse of stained glass in 
	the world.", "Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday", "9:30","17:30",0,0,9,"Gare");
insert into	attraction values (4,"Sacre-Coeur","Roman Catholic church dedicated 
	to the Sacred Heart  of Jesus. Positioned at the highest point in Paris, this 
	cathedral is a must see for anyone visiting Paris.","Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday","8:30",
	"20:00",0,0,12,"Baguette");
insert into	attraction values (5,"Eiffel Tower","Iconic landmark overlooking the 
	Seine River, the Eiffel Tower brings to life the City of Lights. This 300 meter 
	tall tower is a global and cultural icon of France.","Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday","9:00","23:59",
	17,0,11,"La Defense");
insert into attraction values (6,"Notre Dame de Paris","A medieval catholic cathedral, 
	considered one of the finest examples of French gothic architecture and one of the 
	largest and most well known church buildings in the world.","Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday","8:00",
	"18:45",0,0,10,"Seine");
insert into attraction values (7,"Colosseum","Ancient wonder of the world located at 
	the center of the city, the Colosseum is a must see for any person visiting.",
	"Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday","8:30","15:30",12,0,13,"Forum");
insert into	attraction values (8,"Pantheon","Coming from the Greek meaning 'temple 
	of every god' the Pantheon is an iconic ancient Roman building with various 
	historical uses over the ages to be discovered inside","Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday","9:00",
	"19:30",0,0,14,"Fountains");
insert into attraction values (9,"Trevi Fountain", "Beautiful fountain known for its 
	romantic qualities. Also known as the wishing fountain, the Trevi Fountain is a 
	true gem of the city.","Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday","0:00","23:59",0,0,15,"Centre City");	
insert into attraction values (10,"GTL", "Discover the Georgia Tech Lorraine campus
	where some of the most intelligent minds in France are at work doing research 
	for one of the top engineering institutes in the world.",
	"Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday","12:00","18:00",20,1,17,"Graham Bell");	
insert into attraction values (11,"Paris City Bus Tour", "Take a double decker open top 
	bus through the streets of Paris with an English speaking tour guide. Learn all about 
	Paris and its different neighborhoods. Snacks and Drinks available on board. Lasts two hours",
	"Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday","08:00","20:00",20,1,16,"Gare Nord");

create table trip(
	conf_num int not null auto_increment,
	name text,
	start_date varchar(255) not null,
	end_date varchar(255) not null,
	booked int not null,
	city text not null,
	total_cost int,
	username varchar(255) not null,
	foreign key (username) references user(username)
		on update cascade
		on delete cascade,
	primary key (conf_num, username)
);


insert into trip values (1, "Meandering in Metz", "2016-08-06", "2016-08-06", 1, "Metz", 32, "ngainey");
insert into trip values (2, "Perusing Paris", "2016-07-30", "2016-07-30", 1, "Paris", 37, "rsengupta");
	

create table activity(
	activity_id int not null auto_increment,
	conf_num int not null,
	foreign key (conf_num) references trip(conf_num)
		on update cascade
		on delete cascade,
	primary key(activity_id, conf_num),
	cost int,
	attr_id int not null,
	foreign key (attr_id) references attraction(attr_id)
		on update cascade
		on delete cascade,
	start_datetime varchar(255) references time_slot(start_datetime),
	end_datetime varchar(255) references time_slot(end_datetime),
	reserve_num int,
	num_in_party int not null
);

insert into activity values (1,1,0,1,"2016-08-06T10:00:00","2016-08-06T11:30:00",null,2);
insert into activity values (2,1,12,2,"2016-08-06T12:30:00","2016-08-06T14:30:00",null,2);
insert into activity values (3,1,0,3,"2016-08-06T14:45:00","2016-08-06T15:30:00",null,2);
insert into activity values (4,2,0,6,"2016-07-30T09:00:00","2016-07-30T11:00:00",null,4);
insert into activity values (5,2,0,4,"2016-07-30T15:00:00","2016-07-30T16:00:00",null,4);
insert into activity values (6,2,17,5,"2016-07-30T16:00:00","2016-07-30T18:00:00",null,4);
insert into activity values (7,1,20,10,"2016-08-06T16:30:00","2016-08-06T18:00:00",1,2);
insert into activity values (8,2,20,11,"2016-07-30T12:00:00","2016-07-30T14:00:00",2,4);
	
create table time_slot(
	start_datetime varchar(255) not null,
	end_datetime varchar(255) not null,
	quantity int not null,
	attr_id int not null,
	foreign key (attr_id) references attraction(attr_id)
		on update cascade
		on delete cascade,
	primary key (start_datetime, attr_id)
);

insert into time_slot values ("2016-08-06 16:30:00", "2016-08-06 18:00:00", 20, 10);
insert into time_slot values ("2016-08-06 12:00:00", "2016-08-06 13:30:00", 25, 10);
insert into time_slot values ("2016-08-06 14:00:00", "2016-08-06 16:00:00", 10, 10);
insert into	time_slot values ("2016-07-30 12:00:00", "2016-07-30 14:00:00", 4, 11);
insert into	time_slot values ("2016-07-30 08:00:00", "2016-07-30 10:00:00", 4 ,11);
insert into time_slot values ("2016-07-30 16:00:00", "2016-07-30 10:00:00", 10, 11);


create table review(
	date_time varchar(255) not null,
	title text,
	body text,
	username varchar(255) not null,
	foreign key (username) references user(username)
		on update cascade
		on delete cascade,
	attr_id int not null,
	foreign key (attr_id) references attraction(attr_id)
		on update cascade
		on delete cascade,
	primary key (date_time, username, attr_id)
);

insert into	review values ("2014-07-01T10:23:16Z",
	"Colosseum","Colosseum was smaller than expected but still AWESOME!","rsengupta",7);
insert into	review values ("2015-12-23T08:12:02Z","Metz Cathedral",
	"The cathedral was my favorite thing about Metz.","jgreen",3);
insert into	review values ("2012-02-13T12:52:01Z","Eiffel Tower",
	"WOW, impressive for sure.","tjoyce",5);
insert into review values ("2016-05-07T20:12:06Z","Paris City Bus Tour",
	"Very extensive. A little overhyped I think though.","ngainey",11);

create table user_addr(
	username varchar(255) not null,
	foreign key (username) references user(username)
		on update cascade
		on delete cascade,
	addr_id int not null,
	foreign key (addr_id) references address(addr_id)
		on update cascade
		on delete cascade,
	primary key(username, addr_id)
);

insert into user_addr values ("ngainey",1);
insert into user_addr values ("jgreen",2);
insert into user_addr values ("tjoyce",3);
insert into user_addr values ("rsengupta",4);
insert into user_addr values ("mkeezer",5);
insert into user_addr values ("username",6);

create table public_transportation(
	trans_name varchar(255) primary key not null,
	addr_id int not null,
	foreign key (addr_id) references address(addr_id)
		on update cascade
		on delete cascade
);

insert into public_transportation values ("Provence",7);
insert into public_transportation values ("Centre Pompidou",8);
insert into public_transportation values ("Gare",9);
insert into public_transportation values ("Seine",10);
insert into public_transportation values ("La Defence",11);
insert into public_transportation values ("Baguette",12);
insert into public_transportation values ("Forum",13);
insert into public_transportation values ("Fountains",14);
insert into public_transportation values ("Centre City",15);
insert into public_transportation values ("Graham Bell",16);
insert into public_transportation values ("Gare Nord",17);