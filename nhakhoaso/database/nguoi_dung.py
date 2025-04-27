import sqlite3
import hashlib
import os

# Kết nối đến cơ sở dữ liệu
def get_db_connection():
    conn = sqlite3.connect('nhakhoaso.db')
    conn.row_factory = sqlite3.Row
    return conn

# Hàm mã hóa mật khẩu
def hash_password(password):
    # Sử dụng SHA-256 để mã hóa mật khẩu
    return hashlib.sha256(password.encode()).hexdigest()

# Kiểm tra đăng nhập
def check_login(ten_dang_nhap, mat_khau):
    conn = get_db_connection()
    hashed_password = hash_password(mat_khau)
    
    try:
        user = conn.execute(
            'SELECT * FROM NGUOIDUNG WHERE TenDangNhap = ? AND MatKhau = ?',
            (ten_dang_nhap, hashed_password)
        ).fetchone()
        
        conn.close()
        return user
    except Exception as e:
        print(f"Lỗi khi kiểm tra đăng nhập: {e}")
        conn.close()
        return None

# Tạo người dùng mới
def create_user(ten_dang_nhap, mat_khau, ho_ten):
    conn = get_db_connection()
    hashed_password = hash_password(mat_khau)
    
    try:
        conn.execute(
            'INSERT INTO NGUOIDUNG (TenDangNhap, MatKhau, HoTen) VALUES (?, ?, ?)',
            (ten_dang_nhap, hashed_password, ho_ten)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Tên đăng nhập đã tồn tại
        conn.close()
        return False
    except Exception as e:
        print(f"Lỗi khi tạo người dùng: {e}")
        conn.close()
        return False

# Lấy thông tin người dùng theo tên đăng nhập
def get_user_by_username(ten_dang_nhap):
    conn = get_db_connection()
    
    try:
        user = conn.execute(
            'SELECT * FROM NGUOIDUNG WHERE TenDangNhap = ?',
            (ten_dang_nhap,)
        ).fetchone()
        
        conn.close()
        return user
    except Exception as e:
        print(f"Lỗi khi lấy thông tin người dùng: {e}")
        conn.close()
        return None

# Tạo người dùng admin mặc định nếu chưa tồn tại
def create_default_admin():
    if not get_user_by_username('admin'):
        create_user('admin', 'admin123', 'Quản trị viên')
        print("Đã tạo tài khoản admin mặc định")