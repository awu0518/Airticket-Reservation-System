def getAirports(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT airport_city FROM airport")
    return cursor.fetchall()

