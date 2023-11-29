def getAirports(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT airport_city FROM airport")
    return cursor.fetchall()

def getAirlines(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM airline")
    return cursor.fetchall()


