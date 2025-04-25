from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_giasu_data():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='huong24052005',
        database='QuanLyGiaSu'
    )
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True for easier Jinja use
    cursor.execute("SELECT * FROM GIASU")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@app.route('/')
def index():
    giasu_list = get_giasu_data()
    return render_template('qlgs.html', giasu=giasu_list)

if __name__ == '__main__':
    app.run(debug=True)
