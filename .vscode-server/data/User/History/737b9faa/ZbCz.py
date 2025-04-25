from .db import execute_query
import datetime
from .utils import get_next_lich_hen_id

def get_all_lich_hen():
    """
    Lấy danh sách tất cả lịch hẹn
    """
    query = """
    SELECT lh.*, bn.HoTen as TenBenhNhan
    FROM LICHHEN lh
    JOIN BENHNHAN bn ON lh.MaBN = bn.MaBN
    ORDER BY lh.NgayHen DESC
    """
    return execute_query(query, fetch=True)

def get_lich_hen_by_id(ma_lh):
    """
    Lấy thông tin lịch hẹn theo mã
    """
    query = """
    SELECT lh.*, bn.HoTen as TenBenhNhan
    FROM LICHHEN lh
    JOIN BENHNHAN bn ON lh.MaBN = bn.MaBN
    WHERE lh.MaLH = %s
    """
    result = execute_query(query, (ma_lh,), fetch=True)
    return result[0] if result else None

def search_lich_hen(tu_khoa, loai_tim_kiem='ma_lich_hen'):
    """
    Tìm kiếm lịch hẹn theo từ khóa và loại tìm kiếm
    
    Args:
        tu_khoa (str): Từ khóa tìm kiếm
        loai_tim_kiem (str): Loại tìm kiếm (ma_lich_hen, ma_benh_nhan, trang_thai)
        
    Returns:
        list: Danh sách lịch hẹn tìm thấy
    """
    if loai_tim_kiem == 'ma_lich_hen':
        query = """
        SELECT lh.*, bn.HoTen as TenBenhNhan
        FROM LICHHEN lh
        JOIN BENHNHAN bn ON lh.MaBN = bn.MaBN
        WHERE lh.MaLH LIKE %s
        """
    elif loai_tim_kiem == 'ma_benh_nhan':
        query = """
        SELECT lh.*, bn.HoTen as TenBenhNhan
        FROM LICHHEN lh
        JOIN BENHNHAN bn ON lh.MaBN = bn.MaBN
        WHERE lh.MaBN LIKE %s
        """
    elif loai_tim_kiem == 'trang_thai':
        query = """
        SELECT lh.*, bn.HoTen as TenBenhNhan
        FROM LICHHEN lh
        JOIN BENHNHAN bn ON lh.MaBN = bn.MaBN
        WHERE lh.TrangThai LIKE %s COLLATE NOCASE
        """
    else:
        return []
        
    return execute_query(query, (f'%{tu_khoa}%',), fetch=True)

def create_lich_hen(ma_bn, ngay_hen, trang_thai="Chưa khám", ma_lh=None):
    """
    Tạo mới lịch hẹn
    
    Args:
        ma_bn (str): Mã bệnh nhân
        ngay_hen (str): Ngày hẹn (định dạng YYYY-MM-DD HH:MM:SS)
        trang_thai (str, optional): Trạng thái lịch hẹn
        ma_lh (str, optional): Mã lịch hẹn (nếu không cung cấp sẽ tự động tạo)
        
    Returns:
        tuple: (ma_lh, success) - Mã lịch hẹn và kết quả thành công hay không
    """
    # Nếu không có mã lịch hẹn, tạo mã mới
    if not ma_lh:
        ma_lh = get_next_lich_hen_id()
        
    query = """
    INSERT INTO LICHHEN (MaLH, MaBN, NgayHen, TrangThai)
    VALUES (%s, %s, %s, %s)
    """
    
    try:
        execute_query(query, (ma_lh, ma_bn, ngay_hen, trang_thai))
        return ma_lh, True
    except Exception as e:
        print(f"Lỗi khi tạo lịch hẹn: {e}")
        return None, False

def update_lich_hen(ma_lh, ma_bn, ngay_hen, trang_thai):
    """
    Cập nhật thông tin lịch hẹn
    """
    query = """
    UPDATE LICHHEN
    SET MaBN = %s, NgayHen = %s, TrangThai = %s
    WHERE MaLH = %s
    """
    
    try:
        execute_query(query, (ma_bn, ngay_hen, trang_thai, ma_lh))
        return True
    except Exception as e:
        print(f"Lỗi khi cập nhật lịch hẹn: {e}")
        return False

def delete_lich_hen(ma_lh):
    """
    Xóa lịch hẹn theo mã
    """
    query = "DELETE FROM LICHHEN WHERE MaLH = %s"
    try:
        execute_query(query, (ma_lh,))
        return True
    except Exception as e:
        print(f"Lỗi khi xóa lịch hẹn: {e}")
        return False