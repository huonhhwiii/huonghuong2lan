import sqlite3
import os
from config import DB_PATH

def init_database():
    """
    Khởi tạo cơ sở dữ liệu SQLite từ file SQL
    """
    try:
        # Đảm bảo thư mục tồn tại
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        # Kết nối đến SQLite (sẽ tạo file nếu chưa tồn tại)
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        # Đọc file SQL
        with open('database/init_db.sql', 'r') as file:
            sql_script = file.read()
        
        # Thực thi từng câu lệnh SQL
        cursor.executescript(sql_script)
        
        connection.commit()
        print("Cơ sở dữ liệu đã được khởi tạo thành công!")
        
        cursor.close()
        connection.close()
            
    except sqlite3.Error as e:
        print(f"Lỗi khi khởi tạo cơ sở dữ liệu: {e}")

if __name__ == "__main__":
    init_database()