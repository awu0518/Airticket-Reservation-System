from flask import Flask, render_template, request
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
    cursor.execute("SELECT airport_name FROM airport")
    airports = cursor.fetchall()
    cursor.execute("SELECT * FROM flight, airport WHERE flight.depart_from = airport.airport_code ORDER BY depart_date")
    flights = cursor.fetchall()
    return render_template("index.html", airports = airports, flights = flights)

@app.route('/searchFlights', methods=['GET', 'POST'])
def searchFlight():
    depart_from = request.form['departure_airport']
    arrive_to = request.form['arrival_airport']
    print(depart_from)
    print(arrive_to)
    
    return render_template("index.html")


app.secret_key = 'some key that you will never guess'
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)





