insert into Airline values
    ('Jet Blue');

insert into Airport values
    (11430, "JFK", "New York City", "United States", 5, "Both"),
    (200120, "PVG", "Shanghai", "China", 2, "Both"),
    (15231, "PIT", "Pittsburgh", "United States", 3, "Both");

insert into Customer values
    ('cust01@gmail.com', 'cust01pass', 'Richard', 'Vazquez', 10, 'Random Srt', 1, "New York", "NY", 10013, 1111111111, 123456789, "2025-01-01", "United States", "1995-01-01"),
    ('cust02@gmail.com', 'cust02pass', 'Garret', 'Moss', 201, 'Test Srt', 2, "Pittsburgh", "PA", 15215, 2222222222, 234567891, "2024-10-15", "United States", "1990-03-15"),
    ('cust03@gmail.com', 'cust03pass', 'Cassandra', 'Russell', 4, 'Randomer Srt', 3, "New York", "NY", 10015, 3333333333, 345678912, "2027-04-30", "United States", "2000-08-28");

insert into Phone_Number values
    ('cust01@gmail.com', 1111111111),
    ('cust02@gmail.com', 2222222222),
    ('cust02@gmail.com', 3333333333),
    ('cust03@gmail.com', 4444444444),
    ('cust03@gmail.com', 5555555555);

insert into Airplane values
    ("Jet Blue", 12345, 100, "Plane Builders", 500, "2018-07-03"),
    ("Jet Blue", 89301, 80, "Plane Builders", 501, "2019-11-14"),
    ("Jet Blue", 43184, 120, "Plane Builders", 495, "2015-12-18");

insert into Airline_Staff values
    ("staff1", "Jet Blue", "staff01pass", "Cruz", "Donovan", "1990-06-25");

insert into Email values
    ("staff1", "Jet Blue", "staff01@jetblue.com");

insert into Staff_Phone_Number values
    ("staff1", "Jet Blue", 6666666666);

insert into Flight values
    ("Jet Blue", 12345, 1, 11430, "2023-11-08", "12:00:00", 200120, "2023-11-10", "09:00:00", 1300, "ontime", False),
    ("Jet Blue", 12345, 2, 200120, "2023-11-08", "18:00:00", 11430, "2023-11-10", "09:00:00", 1400, "delayed", True),
    ("Jet Blue", 12345, 3, 11430, "2023-11-20", "09:00:00", 200120, "2023-11-22", "11:00:00", 1250, "canceled", False),
    ("Jet Blue", 89301, 4, 15231, "2023-11-08", "10:00:00", 11430, "2023-11-08", "11:30:00", 150, "delayed", True),
    ("Jet Blue", 43184, 5, 11430, "2023-11-12", "12:00:00", 15231, "2023-11-11", "14:30:00", 140, "ontime", False);

insert into Ticket values
    ("Jet Blue", 12345, 1, 1, "2023-11-08", "12:00:00", "credit", 123456, "Richard Vazquez", "2024-09-03", "Richard", "Vazquez", "cust01@gmail.com", "1995-01-01", "2023-11-06", "10:15:12"),
    ("Jet Blue", 12345, 2, 15, "2023-11-08", "18:00:00", "debit", 490419, "Garret Moss", "2023-12-03", "Garret", "Moss", "cust02@gmail.com", "1990-03-15", "2023-11-05", "14:15:27"),
    ("Jet Blue", 12345, 2, 16, "2023-11-08", "18:00:00", "debit", 490419, "Garret Moss", "2023-12-03", "Elizabeth", "Moss", "cust02@gmail.com", "1989-01-15", "2023-11-05", "14:16:00"),
    ("Jet Blue", 89301, 4, 201, "2023-11-08", "10:00:00", "credit", 948103, "Cassandra Russel", "2026-02-14", "Cassandra", "Russel", "cust03@gmail.com", "2000-08-28", "2023-10-29", "20:30:49"),
    ("Jet Blue", 43184, 5, 203, "2023-11-12", "12:00:00", "credit", 948103, "Cassandra Russel", "2024-02-14", "Cassandra", "Russel", "cust03@gmail.com", "2000-08-28", "2023-10-29", "20:32:12");