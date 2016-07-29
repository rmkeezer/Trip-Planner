-- "Given a username or email address, is that user in the database?"

select * from user where username = "ngainey" or email = "ngainey3@gatech.edu";

-- "Given a username or email address, is that user an admin user?"

select is_admin from user where username = "rsengupta" or email = "rsengupta8@gatech.edu";

-- "Which attractions are open right now in Paris?"

select name from attraction join address using (addr_id) where days_open like concat("%", dayname(now()), "%") and  time(closing_time) > curtime() and time(opening_time) < curtime() and city = "Paris" ;

-- "Which attractions in Paris dont require reservations?"

select name from attraction natural join address where reserve_compulsory = 0 and city = "Paris";

-- "Which attractions in Metz are free?"

select name from attraction natural join address where cost = 0 and city = "Metz";

-- "Show the details for one attraction?"

select * from attraction limit 1;

-- "List all the reviews for an attraction."

select * from review where attr_id = 11;

-- "List all the reviews written by a particular user."

select * from review where username = 'jgreen';

-- "Show the details of one review."

select body from review limit 1;

-- "List the trips in the database for a particular user."

select name from trip where username = 'ngainey';

-- "For an attraction that requires reservations and already has some reservations for a time slot, how many spots remain for that time slot?"

select quantity - num_in_party as remaining from time_slot join activity using (attr_id) where (attr_id = 10);

-- "For one of the trips in the database that has two more more paid activities, what is the total cost of the trip?"

select sum(cost) from trip join activity using (conf_num) where conf_num = 2;

-- "For one of the public transportation locations in your database, which attractions are nearest to that location (list it as the nearest public transportation)?"

select name from attraction where trans_name = 'Gare Nord';


