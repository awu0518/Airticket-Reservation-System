127.0.0.1/ticket_reservation_system/airplane/		http://localhost/phpmyadmin/index.php?route=/database/sql&db=ticket_reservation_system
   Showing rows 0 -  4 (5 total, Query took 0.0003 seconds.)
    SELECT airline_name, airplane_id, flight_num, depart_from, depart_date
    FROM flight 
    WHERE depart_date > CAST( CURRENT_DATE() AS Date );

    airline_name	airplane_id	flight_num	depart_from	depart_date
    Jet Blue	    12345	    1	        11430	    2023-11-08	
    Jet Blue	    12345	    3	        11430	    2023-11-20	
    Jet Blue	    43184	    5	        11430	    2023-11-12	
    Jet Blue	    89301	    4	        15231	    2023-11-08	
    Jet Blue	    12345	    2	        200120	    2023-11-08

   Showing rows 0 -  1 (2 total, Query took 0.0003 seconds.)
    SELECT airline_name, airplane_id, flight_num, depart_from, depart_date
    FROM flight 
    WHERE status='delayed';

    airline_name	airplane_id	flight_num	depart_from	depart_date
    Jet Blue	    12345	    2	        200120	    2023-11-08	
    Jet Blue	    89301	    4	        15231	    2023-11-08	

   Showing rows 0 -  2 (3 total, Query took 0.0003 seconds.)
    SELECT distinct first_name, last_name
    FROM ticket NATURAL JOIN customer;

    first_name	last_name
    Richard	    Vazquez	
    Garret	    Moss	
    Cassandra	Russell	

   Showing rows 0 -  2 (3 total, Query took 0.0003 seconds.)
    SELECT airplane_id
    FROM airplane
    WHERE airline_name="Jet Blue";

	airplane_id	
	12345	
    43184	
    89301	
