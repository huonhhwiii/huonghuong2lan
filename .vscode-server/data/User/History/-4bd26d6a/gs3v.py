import mysql.connector

connect = mysql.connector.connect(
    host='localhost',
    user='root',
    password='huong24052005',
    database='QuanLyGiaSu'
)

cursor = connect.cursor()

cursor.execute("""
SELECT * FROM GIAODICH;""")
for row in results:
    print(row)
result = cursor.fetchall()
cursor.close()
connect.close()

