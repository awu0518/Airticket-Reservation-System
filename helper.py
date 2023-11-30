def getAirports(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM airport")
    return cursor.fetchall()

def getAirlines(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM airline")
    return cursor.fetchall()

def getAirplanesForAirline(conn, airline):
    cursor = conn.cursor()
    cursor.execute("SELECT airplane_id FROM airplane WHERE airline_name=%s", airline)
    return cursor.fetchall()

def getFlightsForAirline(conn, airline):
    cursor = conn.cursor()
    query = "SELECT airline_name, T1.flight_num, T1.airport_city as depart_city, depart_date, depart_time, T2.airport_city as arrival_city, arrival_date, arrival_time, base_price, status FROM (SELECT airline_name, flight_num, airport_city, depart_date, depart_time, base_price, status FROM flight, airport WHERE depart_from = airport_code) as T1, (SELECT flight_num, airport_city, arrival_date, arrival_time FROM flight, airport where arrive_at = airport_code) as T2 WHERE T1.flight_num = T2.flight_num and airline_name = %s and T1.depart_date > CAST(CURRENT_DATE() as Date) ORDER BY depart_date"
    cursor.execute(query, airline)
    return cursor.fetchall()


def getAirlineFromStaff(conn, username):
    cursor = conn.cursor()
    query = 'SELECT * FROM airline_staff WHERE username=%s'
    cursor.execute(query, (username))

    staffData = cursor.fetchone()
    if staffData: return staffData['airline_name']
    else: return ""



