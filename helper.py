def getAirports(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM airport")
    return cursor.fetchall()

def getAirlines(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM airline")
    return cursor.fetchall()

def getUniqueAirplanesForAirline(conn, airline):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM airplane WHERE airline_name=%s", airline)
    return cursor.fetchall()

def getAirplanesForAirline(conn, airline):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM airplane natural left outer join maintenance WHERE airline_name=%s", airline)
    return cursor.fetchall()

def getFlightsForAirline(conn, airline):
    cursor = conn.cursor()
    query = "SELECT airplane_id, airline_name, T1.flight_num, T1.airport_city as depart_city, depart_date, depart_time, T2.airport_city as arrival_city, arrival_date, arrival_time, base_price, status FROM (SELECT airplane_id, airline_name, flight_num, airport_city, depart_date, depart_time, base_price, status FROM flight, airport WHERE depart_from = airport_code) as T1, (SELECT flight_num, airport_city, arrival_date, arrival_time FROM flight, airport where arrive_at = airport_code) as T2 WHERE T1.flight_num = T2.flight_num and airline_name = %s and T1.depart_date > CAST(CURRENT_DATE() as Date) ORDER BY depart_date"
    cursor.execute(query, airline)
    return cursor.fetchall()


def getAirlineFromStaff(conn, username):
    cursor = conn.cursor()
    query = 'SELECT * FROM airline_staff WHERE username=%s'
    cursor.execute(query, (username))

    staffData = cursor.fetchone()
    if staffData: return staffData['airline_name']
    else: return ""

def getCustomers(conn, airline):
    cursor = conn.cursor()
    query = 'SELECT first_name, last_name, email, emails FROM customer NATURAL JOIN (SELECT cust_email as email, Count(cust_email) as emails FROM ticket WHERE airline_name = %s GROUP BY cust_email) as emails ORDER BY emails DESC'
    cursor.execute(query, airline)
    return cursor.fetchall()

def moreFlightInfo(conn, airline, flight_num):
    cursor = conn.cursor()
    query = 'SELECT airplane_id, depart_date, depart_time FROM flight WHERE airline_name = %s and flight_num = %s'
    cursor.execute(query, (airline, flight_num))

    flight_info = cursor.fetchone()
    return flight_info['airplane_id'], flight_info['depart_date'], flight_info['depart_time']

def flightInfoForReview(conn, ticket_id):
    cursor = conn.cursor()
    query = 'SELECT airline_name, airplane_id, flight_num, depart_date, depart_time FROM ticket WHERE ticket_id=%s'
    cursor.execute(query, ticket_id)
    
    flight_info = cursor.fetchone()
    return flight_info['airline_name'], flight_info['airplane_id'], flight_info['flight_num'], flight_info['depart_date'], flight_info['depart_time']



