import mysql.connector
from mysql.connector import Error
import os
import sys

# Thêm thư mục gốc vào sys.path để import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG

def get_connection():
    """
    Tạo và trả về kết nối đến cơ sở dữ liệu MySQL
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Lỗi khi kết nối đến MySQL: {e}")
    return None

def execute_query(query, params=None, fetch=False):
    """
    Thực thi truy vấn SQL và trả về kết quả nếu cần
    
    Args:
        query (str): Câu truy vấn SQL
        params (tuple, optional): Tham số cho câu truy vấn
        fetch (bool, optional): Có lấy kết quả hay không
        
    Returns:
        list/None: Kết quả truy vấn hoặc None nếu không cần lấy kết quả
    """
    connection = get_connection()
    result = None
    
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if fetch:
                result = cursor.fetchall()
            else:
                connection.commit()
                result = cursor.lastrowid
                
            cursor.close()
            
        except Error as e:
            print(f"Lỗi khi thực thi truy vấn: {e}")
        finally:
            if connection.is_connected():
                connection.close()
                
    return result