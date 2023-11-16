from flask import Flask, render_template, request, session, redirect, url_for
from helper import *
import pymysql.cursors

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
    query = "SELECT airline_name, T1.flight_num, T1.airport_city as depart_city, depart_date, depart_time, T2.airport_city as arrival_city, arrival_date, arrival_time, base_price, status FROM (SELECT airline_name, flight_num, airport_city, depart_date, depart_time, base_price, status FROM flight, airport WHERE depart_from = airport_code) as T1, (SELECT flight_num, airport_city, arrival_date, arrival_time FROM flight, airport where arrive_at = airport_code) as T2 WHERE T1.flight_num = T2.flight_num ORDER BY depart_date"
    cursor.execute(query)
    flights = cursor.fetchall()
    return render_template("index.html", airports = getAirports(conn), flights = flights, search=True)

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
        return render_template("index.html", airports=getAirports(conn), flights=depart_flights, rflights = return_flights, search=False)
    else:
        return render_template("index.html", airports=getAirports(conn), flights=depart_flights, search=False) 

@app.route('/login')
def login():
    return render_template("login/login.html")

@app.route('/register')
def register():
    return render_template("login/register.html")

app.secret_key = 'some key that you will never guess'
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)





