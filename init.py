from flask import Flask, render_template, request, session, redirect, url_for
from helper import *
from datetime import date
import pymysql.cursors
import hashlib

app = Flask(__name__)

conn = pymysql.connect(host='localhost',
                       port = 3306,
                       user='root',
                       password='',
                       db='ticket_reservation_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor) 

@app.route('/')
def root():
    cursor = conn.cursor()
    query = "SELECT airline_name, T1.flight_num, T1.airport_city as depart_city, depart_date, depart_time, T2.airport_city as arrival_city, arrival_date, arrival_time, base_price, status FROM (SELECT airline_name, flight_num, airport_city, depart_date, depart_time, base_price, status FROM flight, airport WHERE depart_from = airport_code) as T1, (SELECT flight_num, airport_city, arrival_date, arrival_time FROM flight, airport where arrive_at = airport_code) as T2 WHERE T1.flight_num = T2.flight_num and T1.depart_date >= CAST(CURRENT_DATE() as Date) ORDER BY depart_date"
    cursor.execute(query)
    flights = cursor.fetchall()
    return render_template("index.html", airlines = getAirlines(conn), 
                           airports = getAirports(conn), flights = flights, search=True)

@app.route('/searchFlights', methods=['GET', 'POST'])
def searchFlight():
    cursor = conn.cursor()

    depart_from = request.form['departure_airport']
    arrive_to = request.form['arrival_airport']
    depart_date = str(request.form['departure_date'])
    return_date = str(request.form['return_date'])

    query = "SELECT airline_name, T1.flight_num, T1.airport_city as depart_city, depart_date, depart_time, T2.airport_city as arrival_city, arrival_date, arrival_time, base_price, status FROM (SELECT airline_name, flight_num, airport_city, depart_date, depart_time, base_price, status FROM flight, airport WHERE depart_from = airport_code) as T1, (SELECT flight_num, airport_city, arrival_date, arrival_time FROM flight, airport where arrive_at = airport_code) as T2 WHERE T1.flight_num = T2.flight_num and T1.airport_city = %s and T2.airport_city = %s and depart_date = %s"
    cursor.execute(query, (depart_from, arrive_to, depart_date))
    depart_flights = cursor.fetchall()

    if return_date:
        query = "SELECT airline_name, T1.flight_num, T1.airport_city as depart_city, depart_date, depart_time, T2.airport_city as arrival_city, arrival_date, arrival_time, base_price, status FROM (SELECT airline_name, flight_num, airport_city, depart_date, depart_time, base_price, status FROM flight, airport WHERE depart_from = airport_code) as T1, (SELECT flight_num, airport_city, arrival_date, arrival_time FROM flight, airport where arrive_at = airport_code) as T2 WHERE T1.flight_num = T2.flight_num and T1.airport_city = %s and T2.airport_city = %s and depart_date = %s"
        cursor.execute(query, (arrive_to, depart_from, return_date))
        return_flights = cursor.fetchall()
        return render_template("index.html", airlines = getAirlines(conn), airports=getAirports(conn), 
                               flights=depart_flights, rflights = return_flights, search=False)
    else:
        return render_template("index.html", airlines = getAirlines(conn), 
                               airports=getAirports(conn), flights=depart_flights, search=False) 

@app.route('/checkStatus', methods=['GET', 'POST'])
def checkStatus():
    cursor = conn.cursor()

    airline_name = request.form['airline_name']
    flight_id = str(request.form['flight_id'])
    depart_date = str(request.form['departure_date'])

    query = "SELECT airline_name, T1.flight_num, T1.airport_city as depart_city, depart_date, depart_time, T2.airport_city as arrival_city, arrival_date, arrival_time, base_price, status FROM (SELECT airline_name, flight_num, airport_city, depart_date, depart_time, base_price, status FROM flight, airport WHERE depart_from = airport_code) as T1, (SELECT flight_num, airport_city, arrival_date, arrival_time FROM flight, airport where arrive_at = airport_code) as T2 WHERE T1.flight_num = T2.flight_num and T1.airline_name = %s and T1.flight_num = %s and depart_date = %s"
    cursor.execute(query, (airline_name, flight_id, depart_date))
    result = cursor.fetchone()

    return render_template("index.html", result = result, search=False)
    
@app.route('/login')
def login():
    return render_template("login/login.html")

@app.route('/register')
def register():
    return render_template("login/register.html")

@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def loginStaff():
    username = request.form['username']
    password = request.form['password']

    password = hashlib.md5(password.encode())
    password = password.hexdigest()

    cursor = conn.cursor()
    query = "SELECT * FROM airline_staff WHERE username = %s and password = %s"
    cursor.execute(query, (username, password))

    data = cursor.fetchone()
    
    if (data):
        session['username'] = username
        return redirect(url_for("staffHome"))
    else:
        return render_template("login/login.html", error = "Incorrect credentials")
    
@app.route('/custLoginAuth', methods=['GET', 'POST'])
def loginCustomer():
    username = request.form['username']
    password = request.form['password']

    password = hashlib.md5(password.encode())
    password = password.hexdigest()

    cursor = conn.cursor()
    query = "SELECT * FROM customer WHERE username = %s and password = %s"
    cursor.execute(query, (username, password))

    data = cursor.fetchone()
    
    if (data):
        session['username'] = username
        return redirect(url_for("custHome"))
    else:
        return render_template("login/login.html", error = "Incorrect credentials")

@app.route('/getCustReg')
def getCustReg():
    return render_template("/login/customerReg.html")

@app.route('/getStaffReg')
def getStaffReg():
    return render_template("/login/staffReg.html", airlines=getAirlines(conn))

@app.route('/customerRegistration', methods=['GET', 'POST'])
def customerRegistration():
    cursor = conn.cursor()
    email = request.form['email']

    query = "SELECT * FROM customer WHERE email = %s"
    cursor.execute(query, email)
    data = cursor.fetchone()

    if data is not None:
        return render_template("/login/customerReg.html", error="Account already associated with email, please login")
    
    password = request.form['password']
    password = hashlib.md5(password.encode())
    password = password.hexdigest()

    f_name = request.form['first_name']
    l_name = request.form['last_name']
    phone = str(request.form['phone_number'])
    dob = str(request.form['dob'])

    b_num = request.form['building_num']
    street = request.form['street']
    a_num = request.form['apartment_num']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip_code']

    p_num = request.form['passport_num']
    p_exp = str(request.form['passport_exp'])
    p_country = request.form['passport_country']
    
    query = "insert into Customer values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (email, password, f_name, l_name, b_num, street, a_num,
          city, state, zip, p_num, p_exp, p_country, dob))
    query = "insert into Phone_Number values (%s, %s)"
    cursor.execute(query, (email, phone))

    conn.commit()

    return redirect(url_for("login"))

@app.route('/staffRegistration', methods=['GET', 'POST'])
def staffReg():
    cursor = conn.cursor()
    username = request.form['username']

    query = "SELECT * FROM airline_staff WHERE username = %s"
    cursor.execute(query, username)
    data = cursor.fetchone()

    if data is not None:
        return render_template("/login/staffReg.html", error="Account already associated with username, please login", airlines=getAirlines(conn))
    
    password = request.form['password']
    password = hashlib.md5(password.encode())
    password = password.hexdigest()

    airline = request.form['airline_name']
    email = request.form['email']
    f_name = request.form['first_name']
    l_name = request.form['last_name']
    phone = str(request.form['phone_number'])
    dob = str(request.form['dob'])

    query = "insert into airline_staff values (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (username, airline, password, f_name, l_name, dob))
    query = "insert into email values (%s, %s, %s)"
    cursor.execute(query, (username, airline, email))
    query = "insert into staff_phone_number values (%s, %s, %s)"
    cursor.execute(query, (username, airline, phone))

    conn.commit()

    return redirect(url_for("login"))

@app.route('/custHome')
def custHome():
    username = session['username']

    cursor = conn.cursor()
    query = 'SELECT * FROM Customer WHERE email=%s'
    cursor.execute(query, (username))

    return render_template('/customer/home.html', username=username, data=cursor.fetchone())

@app.route('/staffHome')
def staffHome():
    username = session['username']

    cursor = conn.cursor()
    query = 'SELECT * FROM airline_staff WHERE username=%s'
    cursor.execute(query, (username))

    staffData = cursor.fetchone()

    flights = getFlightsForAirline(conn, getAirlineFromStaff(conn, username))

    return render_template('/staff/home.html', username=username, data=staffData, flights=flights, airports=getAirports(conn), search=True)
    
@app.route('/staffSearchFlights', methods=['GET', 'POST'])
def staffSearchFlight():
    cursor = conn.cursor()

    username = session['username']

    start_date = request.form['start']
    end_date = request.form['end']
    depart = request.form['departure_airport']
    arrival = request.form['arrival_airport']

    query = "SELECT airline_name, T1.flight_num, T1.airport_city as depart_city, depart_date, depart_time, T2.airport_city as arrival_city, arrival_date, arrival_time, base_price, status FROM (SELECT airline_name, flight_num, airport_city, depart_date, depart_time, base_price, status FROM flight, airport WHERE depart_from = airport_code) as T1, (SELECT flight_num, airport_city, arrival_date, arrival_time FROM flight, airport where arrive_at = airport_code) as T2 WHERE T1.flight_num = T2.flight_num and airline_name = %s and T1.depart_date >= %s and T1.depart_date <= %s and T1.airport_city = %s and T2.airport_city = %s ORDER BY depart_date"
    cursor.execute(query, (getAirlineFromStaff(conn, username), start_date, end_date, depart, arrival))
    flights = cursor.fetchall()

    return render_template('/staff/home.html', flights=flights, airports=getAirports(conn), search=False)

@app.route('/getCustomersFromFlight', methods=['GET', 'POST'])
def getCustomersFromFlight():
    flight = request.form['flight_num']

    cursor = conn.cursor()

    query = "SELECT * FROM ticket natural left outer join review WHERE flight_num = %s"
    cursor.execute(query, flight)
    data = cursor.fetchall()

    query = "SELECT avg(rating) as avg FROM ticket natural left outer join review WHERE flight_num = %s"
    cursor.execute(query, int(flight))
    avgRating = cursor.fetchone()

    return render_template('/staff/flightInfo.html', flight=flight, data=data, avgRating=avgRating)

@app.route('/flightManager')
def flightManager():
    username = session['username']
    airline = getAirlineFromStaff(conn, username)
    airplanes = getAirplanesForAirline(conn, airline)
    flights = getFlightsForAirline(conn, airline)
    airports = getAirports(conn)

    return render_template('/staff/flightManager.html', airplanes=airplanes, flights=flights, airports=airports)

@app.route('/flightStatusPage')
def flightStatusPage():
    airline = getAirlineFromStaff(conn, session['username'])
    flights = getFlightsForAirline(conn, airline)
    return render_template('/staff/flightManagerPages/changeFlightStatus.html', flights=flights)

@app.route('/changeStatus', methods=['GET', 'POST'])
def changeStatus():
    cursor = conn.cursor()
    flight_id = request.form['flight_id']
    status = request.form['status']

    query = "UPDATE flight SET status = %s WHERE flight_num = %s"
    cursor.execute(query, (status, flight_id))
    conn.commit()

    return redirect(url_for("flightManager"))

@app.route('/addFlightPage')
def addFlightPage():
    airline = getAirlineFromStaff(conn, session['username'])
    airports = getAirports(conn)
    airplanes = getAirplanesForAirline(conn, airline)
    return render_template('/staff/flightManagerPages/addFlight.html', airports=airports, airplanes=airplanes)

@app.route('/addAirportPage')
def addAirportPage():
    return render_template('/staff/flightManagerPages/addAirport.html')

@app.route('/addAirport', methods=['GET', 'POST'])
def addAirport():
    cursor = conn.cursor()
    airport_code = request.form['code']

    query = "SELECT airport_code FROM airport WHERE airport_code=%s"
    cursor.execute(query, airport_code)
    exist = cursor.fetchone()

    if exist:
        return render_template('/staff/flightManagerPages/addAirport.html', error="Airport Code Already Used")
    
    return redirect(url_for("flightManager"))

@app.route('/addAirplanePage')
def addAirplanePage():
    return render_template('/staff/flightManagerPages/addAirplane.html')

@app.route('/addAirplane', methods=['GET', 'POST'])
def addAirplane():
    cursor = conn.cursor()
    airplane_id = request.form['id']

    query = "SELECT airplane_id FROM airplane WHERE airplane_id=%s"
    cursor.execute(query, airplane_id)
    exist = cursor.fetchone()

    if exist:
        return render_template('/staff/flightManagerPages/addAirplane.html', error="Airplane ID Already Used")
    
    return redirect(url_for("flightManager"))


@app.route('/scheduleMaintenancePage')
def scheduleMaintanencePage():
    airline = getAirlineFromStaff(conn, session['username'])
    airplanes = getAirplanesForAirline(conn, airline)
    return render_template('/staff/flightManagerPages/scheduleMaintenance.html', airplanes=airplanes)

@app.route('/scheduleMaintenance', methods=['GET', 'POST'])
def scheduleMaintanence():
    cursor = conn.cursor()
    airline = getAirlineFromStaff(conn, session['username'])

    airplane_id = request.form['airplane_id']
    start_date = request.form['start_date']
    start_time = request.form['start_time']
    end_date = request.form['end_date']
    end_time = request.form['end_time']

    # add check for flights scheduled during maintenance time

    query = "insert into maintenance values (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (airline, airplane_id, start_date, start_time, end_date, end_time))
    conn.commit()

    return redirect(url_for("flightManager"))


@app.route('/customerInfo')
def customerInfo():
    username = session['username']
    customers = getCustomers(conn, getAirlineFromStaff(conn, username))

    return render_template('/staff/customers.html', customers=customers)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

app.secret_key = 'some key that you will never guess'
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)





