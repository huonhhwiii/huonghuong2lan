sqlite3 /home/huong/nhakhoaso/database/nhakhoaso.db
from .db import execute_query
import datetime
from .utils import get_next_benh_nhan_id

def get_all_benh_nhan():
    """
    Lấy danh sách tất cả bệnh nhân
    """
    query = "SELECT * FROM BENHNHAN ORDER BY MaBN"
    return execute_query(query, fetch=True)

def get_benh_nhan_by_id(ma_bn):
    """
    Lấy thông tin bệnh nhân theo mã
    """
    query = "SELECT * FROM BENHNHAN WHERE MaBN = %s"
    result = execute_query(query, (ma_bn,), fetch=True)
    return result[0] if result else None

def search_benh_nhan(tu_khoa, loai_tim_kiem='ma_benh_nhan'):
    """
    Tìm kiếm bệnh nhân theo từ khóa và loại tìm kiếm
    
    Args:
        tu_khoa (str): Từ khóa tìm kiếm
        loai_tim_kiem (str): Loại tìm kiếm (ma_benh_nhan, so_dien_thoai, ho_ten)
        
    Returns:
        list: Danh sách bệnh nhân tìm thấy
    """
    if loai_tim_kiem == 'ma_benh_nhan':
        query = "SELECT * FROM BENHNHAN WHERE MaBN LIKE ?"
    elif loai_tim_kiem == 'so_dien_thoai':
        query = "SELECT * FROM BENHNHAN WHERE Sdt LIKE ?"
    elif loai_tim_kiem == 'ho_ten':
        # Sử dụng COLLATE NOCASE để tìm kiếm không phân biệt chữ hoa chữ thường
        query = "SELECT * FROM BENHNHAN WHERE HoTen LIKE ? COLLATE NOCASE"
    else:
        return []
        
    return execute_query(query, (f'%{tu_khoa}%',), fetch=True)

def create_benh_nhan(ho_ten, so_dien_thoai, gioi_tinh=None, ngay_sinh=None, ma_bn=None):
    """
    Tạo mới bệnh nhân
    
    Args:
        ho_ten (str): Họ tên bệnh nhân
        so_dien_thoai (str): Số điện thoại
        gioi_tinh (str, optional): Giới tính
        ngay_sinh (str, optional): Ngày sinh (định dạng YYYY-MM-DD)
        ma_bn (str, optional): Mã bệnh nhân (nếu không cung cấp sẽ tự động tạo)
        
    Returns:
        tuple: (ma_bn, success) - Mã bệnh nhân và kết quả thành công hay không
    """
    # Nếu không có mã bệnh nhân, tạo mã mới
    if not ma_bn:
        ma_bn = get_next_benh_nhan_id()
        
    query = """
    INSERT INTO BENHNHAN (MaBN, HoTen, NgaySinh, GioiTinh, Sdt)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    try:
        execute_query(query, (ma_bn, ho_ten, ngay_sinh, gioi_tinh, so_dien_thoai))
        return ma_bn, True
    except Exception as e:
        print(f"Lỗi khi tạo bệnh nhân: {e}")
        return None, False

def update_benh_nhan(ma_bn, ho_ten, so_dien_thoai, gioi_tinh=None, ngay_sinh=None):
    """
    Cập nhật thông tin bệnh nhân
    """
    query = """
    UPDATE BENHNHAN
    SET HoTen = %s, NgaySinh = %s, GioiTinh = %s, Sdt = %s
    WHERE MaBN = %s
    """
    
    try:
        execute_query(query, (ho_ten, ngay_sinh, gioi_tinh, so_dien_thoai, ma_bn))
        return True
    except Exception as e:
        print(f"Lỗi khi cập nhật bệnh nhân: {e}")
        return False

def delete_benh_nhan(ma_bn):
    """
    Xóa bệnh nhân theo mã
    """
    query = "DELETE FROM BENHNHAN WHERE MaBN = %s"
    execute_query(query, (ma_bn,))