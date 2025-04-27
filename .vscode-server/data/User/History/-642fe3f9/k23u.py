import sqlite3
import hashlib
import sys

def get_db_connection():
    conn = sqlite3.connect('nhakhoaso/nhakhoaso.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(ten_dang_nhap, mat_khau, ho_ten):
    conn = get_db_connection()
    hashed_password = hash_password(mat_khau)
    
    try:
        # Kiểm tra xem bảng NGUOIDUNG đã tồn tại chưa
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='NGUOIDUNG'")
        if not cursor.fetchone():
            print("Bảng NGUOIDUNG chưa tồn tại. Đang tạo bảng...")
            conn.execute('CREATE TABLE NGUOIDUNG (TenDangNhap TEXT PRIMARY KEY, MatKhau TEXT, HoTen TEXT)')
            conn.commit()
            print("Đã tạo bảng NGUOIDUNG thành công!")
        
        # Kiểm tra xem tên đăng nhập đã tồn tại chưa
        existing_user = conn.execute(
            'SELECT * FROM NGUOIDUNG WHERE TenDangNhap = ?',
            (ten_dang_nhap,)
        ).fetchone()
        
        if existing_user:
            print(f"Lỗi: Tên đăng nhập '{ten_dang_nhap}' đã tồn tại!")
            conn.close()
            return False
        
        # Thêm người dùng mới
        conn.execute(
            'INSERT INTO NGUOIDUNG (TenDangNhap, MatKhau, HoTen) VALUES (?, ?, ?)',
            (ten_dang_nhap, hashed_password, ho_ten)
        )
        conn.commit()
        print(f"Đã tạo tài khoản thành công cho '{ho_ten}' với tên đăng nhập '{ten_dang_nhap}'")
        conn.close()
        return True
    except Exception as e:
        print(f"Lỗi khi tạo người dùng: {e}")
        conn.close()
        return False

def list_users():
    conn = get_db_connection()
    try:
        users = conn.execute('SELECT TenDangNhap, HoTen FROM NGUOIDUNG').fetchall()
        print("\nDanh sách người dùng hiện tại:")
        print("-----------------------------")
        for user in users:
            print(f"Tên đăng nhập: {user['TenDangNhap']}, Họ tên: {user['HoTen']}")
        print("-----------------------------")
        conn.close()
    except Exception as e:
        print(f"Lỗi khi lấy danh sách người dùng: {e}")
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Sử dụng: python3 create_user.py <tên_đăng_nhập> <mật_khẩu> <họ_tên>")
        print("Ví dụ: python3 create_user.py nhanvien1 password123 'Nguyễn Văn A'")
        sys.exit(1)
    
    ten_dang_nhap = sys.argv[1]
    mat_khau = sys.argv[2]
    ho_ten = sys.argv[3]
    
    create_user(ten_dang_nhap, mat_khau, ho_ten)
    list_users()