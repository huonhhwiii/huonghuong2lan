import mysql.connector
connect = mysql.connector.connect(
    host='localhost',
    user='root',
    password='huong24052005',
    database='QuanLyGiaSu'
)
cursor = connect.cursor()
cursor.execute("SELECT * FROM GIASU;")
results = cursor.fetchall()
if cursor:
   print("yes")
else:
   print("done")

