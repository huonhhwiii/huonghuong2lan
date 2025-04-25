import sqlite3
import os
import sys
import datetime

# Thêm thư mục gốc vào sys.path để import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH

def dict_factory(cursor, row):
    """
    Chuyển đổi kết quả truy vấn thành dictionary
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        value = row[idx]
        # Chuyển đổi datetime.date thành datetime.datetime
        if isinstance(value, str) and len(value) == 10 and value[4] == '-' and value[7] == '-':
            try:
                value = datetime.datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                pass
        d[col[0]] = value
    return d

def get_connection():
    """
    Tạo và trả về kết nối đến cơ sở dữ liệu SQLite
    """
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = dict_factory
        return connection
    except sqlite3.Error as e:
        print(f"Lỗi khi kết nối đến SQLite: {e}")
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
    # Thay thế %s bằng ? cho SQLite
    query = query.replace('%s', '?')
    
    connection = get_connection()
    result = None
    
    if connection:
        try:
            cursor = connection.cursor()
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
            
        except sqlite3.Error as e:
            print(f"Lỗi khi thực thi truy vấn: {e}")
        finally:
            connection.close()
                
    return result