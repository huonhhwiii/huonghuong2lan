# Quản lý phiếu khám
from .db import execute_query
import datetime

def get_all_phieu_kham():
    """Lấy danh sách tất cả phiếu khám"""
    query = """
    SELECT pk.*, bn.HO_TEN as TEN_BENH_NHAN, bs.HO_TEN as TEN_BAC_SI, dv.TEN_DICH_VU
    FROM PHIEUKHAM pk
    JOIN BENHNHAN bn ON pk.MA_BENH_NHAN = bn.MA_BENH_NHAN
    JOIN BACSI bs ON pk.MA_BAC_SI = bs.MA_BAC_SI
    JOIN DICHVU dv ON pk.MA_DICH_VU = dv.MA_DICH_VU
    ORDER BY pk.NGAY_KHAM DESC
    """
    return execute_query(query, fetch=True)

def get_phieu_kham_by_id(ma_phieu_kham):
    """Lấy thông tin phiếu khám theo mã"""
    query = """
    SELECT pk.*, bn.HO_TEN as TEN_BENH_NHAN, bs.HO_TEN as TEN_BAC_SI, dv.TEN_DICH_VU, dv.GIA
    FROM PHIEUKHAM pk
    JOIN BENHNHAN bn ON pk.MA_BENH_NHAN = bn.MA_BENH_NHAN
    JOIN BACSI bs ON pk.MA_BAC_SI = bs.MA_BAC_SI
    JOIN DICHVU dv ON pk.MA_DICH_VU = dv.MA_DICH_VU
    WHERE pk.MA_PHIEU_KHAM = ?
    """
    result = execute_query(query, (ma_phieu_kham,), fetch=True)
    return result[0] if result else None

def search_phieu_kham(tu_khoa, loai_tim_kiem='ma_phieu_kham'):
    """Tìm kiếm phiếu khám theo từ khóa"""
    if loai_tim_kiem == 'ma_phieu_kham':
        query = """
        SELECT pk.*, bn.HO_TEN as TEN_BENH_NHAN, bs.HO_TEN as TEN_BAC_SI, dv.TEN_DICH_VU
        FROM PHIEUKHAM pk
        JOIN BENHNHAN bn ON pk.MA_BENH_NHAN = bn.MA_BENH_NHAN
        JOIN BACSI bs ON pk.MA_BAC_SI = bs.MA_BAC_SI
        JOIN DICHVU dv ON pk.MA_DICH_VU = dv.MA_DICH_VU
        WHERE pk.MA_PHIEU_KHAM LIKE ?
        ORDER BY pk.NGAY_KHAM DESC
        """
    elif loai_tim_kiem == 'ma_benh_nhan':
        query = """
        SELECT pk.*, bn.HO_TEN as TEN_BENH_NHAN, bs.HO_TEN as TEN_BAC_SI, dv.TEN_DICH_VU
        FROM PHIEUKHAM pk
        JOIN BENHNHAN bn ON pk.MA_BENH_NHAN = bn.MA_BENH_NHAN
        JOIN BACSI bs ON pk.MA_BAC_SI = bs.MA_BAC_SI
        JOIN DICHVU dv ON pk.MA_DICH_VU = dv.MA_DICH_VU
        WHERE pk.MA_BENH_NHAN LIKE ?
        ORDER BY pk.NGAY_KHAM DESC
        """
    elif loai_tim_kiem == 'ten_benh_nhan':
        query = """
        SELECT pk.*, bn.HO_TEN as TEN_BENH_NHAN, bs.HO_TEN as TEN_BAC_SI, dv.TEN_DICH_VU
        FROM PHIEUKHAM pk
        JOIN BENHNHAN bn ON pk.MA_BENH_NHAN = bn.MA_BENH_NHAN
        JOIN BACSI bs ON pk.MA_BAC_SI = bs.MA_BAC_SI
        JOIN DICHVU dv ON pk.MA_DICH_VU = dv.MA_DICH_VU
        WHERE bn.HO_TEN LIKE ?
        ORDER BY pk.NGAY_KHAM DESC
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
    INSERT INTO PHIEUKHAM (MA_PHIEU_KHAM, MA_BENH_NHAN, MA_BAC_SI, MA_DICH_VU, CHAN_DOAN, GHI_CHU, NGAY_KHAM)
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
    SET MA_BENH_NHAN = ?, MA_BAC_SI = ?, MA_DICH_VU = ?, CHAN_DOAN = ?, GHI_CHU = ?, NGAY_KHAM = ?
    WHERE MA_PHIEU_KHAM = ?
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
    check_query = "SELECT COUNT(*) as count FROM PHIEUKHAM WHERE MA_PHIEU_KHAM = ?"
    result = execute_query(check_query, (ma_phieu_kham,), fetch=True)
    
    if not result or result[0]['count'] == 0:
        print(f"Không tìm thấy phiếu khám với mã: {ma_phieu_kham}")
        return False
    
    # Thực hiện xóa phiếu khám
    query = "DELETE FROM PHIEUKHAM WHERE MA_PHIEU_KHAM = ?"
    
    try:
        execute_query(query, (ma_phieu_kham,))
        print(f"Đã xóa phiếu khám: {ma_phieu_kham}")
        return True
    except Exception as e:
        print(f"Lỗi khi xóa phiếu khám: {e}")
        return False