create table Airline (
    airline_name        varchar(20) not null,

    primary key(airline_name)
);

create table Airplane (
    airline_name        varchar(20) not null,
    airplane_id         int(5) unsigned not null,
    num_seats           int(3) unsigned not null,
    manufact_comp       varchar(20) not null,
    model_num           int(3) unsigned not null,
    manufact_date       date not null,

    primary key(airline_name, airplane_id),
    foreign key(airline_name) references Airline(airline_name)
);

create table Maintenance (
    airline_name        varchar(20) not null,
    airplane_id         int(5) unsigned not null,
    start_date          date not null,
    start_time          time not null,
    end_date            date not null,
    end_time            time not null,

    primary key(airplane_id, start_date, start_time),
    foreign key(airline_name, airplane_id) references Airplane(airline_name, airplane_id)
);

create table Airport (
    airport_code        int(5) unsigned not null,
    airport_name        varchar(20) not null,
    airport_city        varchar(20) not null,
    airport_country     varchar(20) not null,
    num_of_terminals    int(3) unsigned not null,
    airport_type        varchar(15) not null check (airport_type in ('domestic', 'international', 'both')),

    primary key(airport_code)
);

create table Flight (
    airline_name        varchar(20) not null,
    airplane_id         int(5) unsigned not null,
    flight_num          int(5) unsigned not null,
    depart_from         int(5) unsigned not null,
    depart_date         date not null,
    depart_time         time not null,
    arrive_at           int(5) unsigned not null,
    arrival_date        date not null,
    arrival_time        time not null,
    base_price          double(10, 2) unsigned not null,
    status              varchar(10) not null check (status in ('delayed', 'ontime', 'canceled')),
    roundtrip           boolean,

    primary key(airline_name, airplane_id, flight_num, depart_date, depart_time),
    foreign key(airline_name, airplane_id) references Airplane(airline_name, airplane_id),
    foreign key(depart_from) references Airport(airport_code),
    foreign key(arrive_at) references Airport(airport_code)
);

create table Customer (
    email               varchar(20) not null,
    password            varchar(20) not null,
    first_name          varchar(20) not null,
    last_name           varchar(20) not null,
    building_num        int(5) unsigned not null,
    street              varchar(20) not null,
    apart_num           int(5) unsigned not null,
    city                varchar(20) not null,
    state               varchar(20) not null,
    zip_code            int(5) unsigned not null,
    phone_number        int(10) unsigned not null,
    passport_num        int(10) unsigned not null,
    passport_exp        date not null,
    passport_country    varchar(20) not null,
    date_of_birth       date not null

    primary key(email)
);

create table Phone_Number (
    email               varchar(20) not null,
    phone_number        int(10) unsigned not null,

    primary key(email, phone_number),
    foreign key(email) references Customer(email)
);

create table Ticket (
    airline_name        varchar(20) not null,
    airplane_id         int(5) unsigned not null,
    flight_num          int(5) unsigned not null,
    ticket_id           int(5) unsigned not null,
    depart_date         date not null,
    depart_time         time not null,
    card_type           varchar(6) check (card_type in ('credit', 'debit')),
    card_number         int(20) unsigned not null,
    card_name           varchar(20) not null,
    expiration_date     date not null,
    cust_first_name     varchar(20) not null,
    cust_last_name      varchar(20) not null,
    cust_email          varchar(20) not null,
    date_of_birth       date not null,
    purchase_date       date not null,
    purchase_time       time not null,

    primary key(ticket_id),
    foreign key(airline_name, airplane_id, flight_num, depart_date, depart_time) references Flight(airline_name, airplane_id, flight_num, depart_date, depart_time),
    foreign key(cust_email) references Customer(email)
);

create table Review (
    airline_name        varchar(20) not null,
    airplane_id         int(5) unsigned not null,
    flight_num          int(5) unsigned not null,
    rating              int(1) not null check (rating > 0 and rating < 6),
    depart_date         date not null,
    depart_time         time not null,
    comments            varchar(600),
    email               varchar(20) not null,

    primary key(email, airline_name, airplane_id, flight_num, depart_date, depart_time),
    foreign key(airline_name, airplane_id, flight_num, depart_date, depart_time) references Ticket(airline_name, airplane_id, flight_num, depart_date, depart_time),
    foreign key(email) references Customer(email)
);

create table Airline_Staff (
    username            varchar(20) not null,
    airline_name        varchar(20) not null,
    password            varchar(20) not null,
    first_name          varchar(20) not null,
    last_name           varchar(20) not null,
    date_of_birth       date not null,

    primary key(username, airline_name),
    foreign key(airline_name) references Airline(airline_name)
);

create table Email (
    username            varchar(20) not null,
    airline_name        varchar(20) not null,
    email               varchar(20) not null,

    primary key(username, airline_name, email),
    foreign key(username, airline_name) references Airline_Staff(username, airline_name)
);

create table Staff_Phone_Number (
    username            varchar(20) not null,
    airline_name        varchar(20) not null,
    phone_number        int(10) not null,

    primary key(username, airline_name, phone_number),
    foreign key(username, airline_name) references Airline_Staff(username, airline_name)
);


