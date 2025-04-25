# Quản lý phiếu khám
from .db import execute_query
import datetime

def get_all_phieu_kham():
    """Lấy danh sách tất cả phiếu khám"""
    query = """
    SELECT pk.*, bn.HoTen as TenBenhNhan, bs.HoTen as TenBacSi, dv.TenDV as TenDichVu
    FROM PHIEUKHAM pk
    JOIN BENHNHAN bn ON pk.MaBN = bn.MaBN
    JOIN BACSI bs ON pk.MaBS = bs.MaBS
    JOIN DICHVU dv ON pk.MaDV = dv.MaDV
    ORDER BY pk.NgayKham DESC
    """
    return execute_query(query, fetch=True)

def get_phieu_kham_by_id(ma_phieu_kham):
    """Lấy thông tin phiếu khám theo mã"""
    query = """
    SELECT pk.*, bn.HoTen as TenBenhNhan, bs.HoTen as TenBacSi, dv.TenDV as TenDichVu, dv.Gia
    FROM PHIEUKHAM pk
    JOIN BENHNHAN bn ON pk.MaBN = bn.MaBN
    JOIN BACSI bs ON pk.MaBS = bs.MaBS
    JOIN DICHVU dv ON pk.MaDV = dv.MaDV
    WHERE pk.MaPK = ?
    """
    result = execute_query(query, (ma_phieu_kham,), fetch=True)
    return result[0] if result else None

def search_phieu_kham(tu_khoa, loai_tim_kiem='ma_phieu_kham'):
    """Tìm kiếm phiếu khám theo từ khóa"""
    if loai_tim_kiem == 'ma_phieu_kham':
        query = """
        SELECT pk.*, bn.HoTen as TenBenhNhan, bs.HoTen as TenBacSi, dv.TenDV as TenDichVu
        FROM PHIEUKHAM pk
        JOIN BENHNHAN bn ON pk.MaBN = bn.MaBN
        JOIN BACSI bs ON pk.MaBS = bs.MaBS
        JOIN DICHVU dv ON pk.MaDV = dv.MaDV
        WHERE pk.MaPK LIKE ?
        ORDER BY pk.NgayKham DESC
        """
    elif loai_tim_kiem == 'ma_benh_nhan':
        query = """
        SELECT pk.*, bn.HoTen as TenBenhNhan, bs.HoTen as TenBacSi, dv.TenDV as TenDichVu
        FROM PHIEUKHAM pk
        JOIN BENHNHAN bn ON pk.MaBN = bn.MaBN
        JOIN BACSI bs ON pk.MaBS = bs.MaBS
        JOIN DICHVU dv ON pk.MaDV = dv.MaDV
        WHERE pk.MaBN LIKE ?
        ORDER BY pk.NgayKham DESC
        """
    elif loai_tim_kiem == 'ten_benh_nhan':
        query = """
        SELECT pk.*, bn.HoTen as TenBenhNhan, bs.HoTen as TenBacSi, dv.TenDV as TenDichVu
        FROM PHIEUKHAM pk
        JOIN BENHNHAN bn ON pk.MaBN = bn.MaBN
        JOIN BACSI bs ON pk.MaBS = bs.MaBS
        JOIN DICHVU dv ON pk.MaDV = dv.MaDV
        WHERE bn.HoTen LIKE ?
        ORDER BY pk.NgayKham DESC
        """
    else:
        raise ValueError("Loại tìm kiếm không hợp lệ")
    
    return execute_query(query, (f"%{tu_khoa}%",), fetch=True)

def create_phieu_kham(ma_benh_nhan, ma_bac_si, ma_dich_vu, chan_doan, ghi_chu, ma_phieu_kham=None, ngay_kham=None):
    """Tạo phiếu khám mới"""
    # Nếu không có mã phiếu khám, tạo mã mới
    if not ma_phieu_kham:
        from .utils import get_next_phieu_kham_id
        ma_phieu_kham = get_next_phieu_kham_id()
    
    # Nếu không có ngày khám, lấy ngày hiện tại
    if not ngay_kham:
        ngay_kham = datetime.datetime.now().strftime('%Y-%m-%d')
    
    query = """
    INSERT INTO PHIEUKHAM (MaPK, MaBN, MaBS, MaDV, ChanDoan, GhiChu, NgayKham)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    
    try:
        execute_query(query, (ma_phieu_kham, ma_benh_nhan, ma_bac_si, ma_dich_vu, chan_doan, ghi_chu, ngay_kham))
        return ma_phieu_kham, True
    except Exception as e:
        print(f"Lỗi khi tạo phiếu khám: {e}")
        return None, False

def update_phieu_kham(ma_phieu_kham, ma_benh_nhan, ma_bac_si, ma_dich_vu, chan_doan, ghi_chu, ngay_kham=None):
    """Cập nhật thông tin phiếu khám"""
    # Nếu không có ngày khám, lấy ngày hiện tại
    if not ngay_kham:
        ngay_kham = datetime.datetime.now().strftime('%Y-%m-%d')
    
    query = """
    UPDATE PHIEUKHAM
    SET MaBN = ?, MaBS = ?, MaDV = ?, ChanDoan = ?, GhiChu = ?, NgayKham = ?
    WHERE MaPK = ?
    """
    
    try:
        execute_query(query, (ma_benh_nhan, ma_bac_si, ma_dich_vu, chan_doan, ghi_chu, ngay_kham, ma_phieu_kham))
        return True
    except Exception as e:
        print(f"Lỗi khi cập nhật phiếu khám: {e}")
        return False

def delete_phieu_kham(ma_phieu_kham):
    """Xóa phiếu khám
    
    Args:
        ma_phieu_kham (str): Mã phiếu khám cần xóa
        
    Returns:
        bool: True nếu xóa thành công, False nếu có lỗi
    """
    # Kiểm tra xem phiếu khám có tồn tại không
    check_query = "SELECT COUNT(*) as count FROM PHIEUKHAM WHERE MaPK = ?"
    result = execute_query(check_query, (ma_phieu_kham,), fetch=True)
    
    if not result or result[0]['count'] == 0:
        print(f"Không tìm thấy phiếu khám với mã: {ma_phieu_kham}")
        return False
    
    # Thực hiện xóa phiếu khám
    query = "DELETE FROM PHIEUKHAM WHERE MaPK = ?"
    
    try:
        execute_query(query, (ma_phieu_kham,))
        print(f"Đã xóa phiếu khám: {ma_phieu_kham}")
        return True
    except Exception as e:
        print(f"Lỗi khi xóa phiếu khám: {e}")
        return False