import mysql.connector
from mysql.connector import Error
import os
from config import DB_CONFIG

def init_database():
    """
    Khởi tạo cơ sở dữ liệu từ file SQL
    """
    try:
        # Kết nối đến MySQL Server (không chỉ định database)
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Đọc file SQL
            with open('database/init_db.sql', 'r') as file:
                sql_script = file.read()
            
            # Thực thi từng câu lệnh SQL
            for result in cursor.execute(sql_script, multi=True):
                pass
            
            print("Cơ sở dữ liệu đã được khởi tạo thành công!")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Lỗi khi khởi tạo cơ sở dữ liệu: {e}")

if __name__ == "__main__":
    init_database()