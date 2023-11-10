from flask import Flask
import pymysql.cursors

app = Flask(__name__)

conn = pymysql.connect(host='localhost',
                       port = 3306,
                       user='root',
                       password='root',
                       db='ticket_reservation_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor) 

@app.route('/')
def hello():
    return "Hello World"

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)





