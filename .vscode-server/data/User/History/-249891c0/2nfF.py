import mysql.connector

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
