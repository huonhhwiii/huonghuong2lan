from .db import execute_query
import datetime
from .utils import get_next_id

def get_all_phieu_kham():
    """
    Lấy danh sách tất cả phiếu khám (chỉ các thông tin cơ bản)
    """
    try:
        query = """
        SELECT MaPK, NgayKham, ChanDoan, GhiChu, MaBN, MaBS, MaDV
        FROM PHIEUKHAM
        ORDER BY MaPK
        """
        result = execute_query(query, fetch=True)
        return result if result else []
    except Exception as e:
        print(f"Lỗi khi lấy danh sách phiếu khám: {e}")
        raise Exception(f"Không thể lấy danh sách phiếu khám: {str(e)}")

def get_phieu_kham_by_id(ma_pk):
    """
    Lấy thông tin phiếu khám theo mã (chỉ các thông tin cơ bản)
    """
    try:
        query = """
        SELECT MaPK, NgayKham, ChanDoan, GhiChu, MaBN, MaBS, MaDV
        FROM PHIEUKHAM
        WHERE MaPK = %s
        """
        result = execute_query(query, (ma_pk,), fetch=True)
        return result[0] if result else None
    except Exception as e:
        print(f"Lỗi khi lấy thông tin phiếu khám: {e}")
        raise Exception(f"Không thể lấy thông tin phiếu khám: {str(e)}")

def search_phieu_kham(tu_khoa, loai_tim_kiem='ma_phieu_kham'):
    """
    Tìm kiếm phiếu khám theo từ khóa và loại tìm kiếm (chỉ các thông tin cơ bản)
    
    Args:
        tu_khoa (str): Từ khóa tìm kiếm
        loai_tim_kiem (str): Loại tìm kiếm (ma_phieu_kham, ma_benh_nhan, ma_bac_si, chan_doan)
        
    Returns:
        list: Danh sách phiếu khám tìm thấy
    """
    try:
        if loai_tim_kiem == 'ma_phieu_kham':
            query = """
            SELECT MaPK, NgayKham, ChanDoan, GhiChu, MaBN, MaBS, MaDV
            FROM PHIEUKHAM
            WHERE MaPK LIKE %s
            """
        elif loai_tim_kiem == 'ma_benh_nhan':
            query = """
            SELECT MaPK, NgayKham, ChanDoan, GhiChu, MaBN, MaBS, MaDV
            FROM PHIEUKHAM
            WHERE MaBN LIKE %s
            """
        elif loai_tim_kiem == 'ma_bac_si':
            query = """
            SELECT MaPK, NgayKham, ChanDoan, GhiChu, MaBN, MaBS, MaDV
            FROM PHIEUKHAM
            WHERE MaBS LIKE %s
            """
        elif loai_tim_kiem == 'chan_doan':
            query = """
            SELECT MaPK, NgayKham, ChanDoan, GhiChu, MaBN, MaBS, MaDV
            FROM PHIEUKHAM
            WHERE ChanDoan LIKE %s COLLATE NOCASE
            """
        else:
            return []
            
        result = execute_query(query, (f'%{tu_khoa}%',), fetch=True)
        return result if result else []
    except Exception as e:
        print(f"Lỗi khi tìm kiếm phiếu khám: {e}")
        raise Exception(f"Không thể tìm kiếm phiếu khám: {str(e)}")

def create_phieu_kham(ma_bn, ma_bs, ma_dv, chan_doan=None, ghi_chu=None, ma_pk=None, ngay_kham=None):
    """
    Tạo mới phiếu khám
    
    Args:
        ma_bn (str): Mã bệnh nhân
        ma_bs (str): Mã bác sĩ
        ma_dv (str): Mã dịch vụ
        chan_doan (str, optional): Chẩn đoán
        ghi_chu (str, optional): Ghi chú
        ma_pk (str, optional): Mã phiếu khám (nếu không cung cấp sẽ tự động tạo)
        ngay_kham (str, optional): Ngày khám (định dạng YYYY-MM-DD HH:MM:SS)
        
    Returns:
        tuple: (ma_pk, success) - Mã phiếu khám và kết quả thành công hay không
    """
    # Nếu không có mã phiếu khám, tạo mã mới
    if not ma_pk:
        ma_pk = get_next_id("PHIEUKHAM", "MaPK", "PK", 5)
        
    # Nếu không có ngày khám, sử dụng ngày hiện tại
    if not ngay_kham:
        ngay_kham = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    query = """
    INSERT INTO PHIEUKHAM (MaPK, MaBN, MaBS, MaDV, NgayKham, ChanDoan, GhiChu)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        execute_query(query, (ma_pk, ma_bn, ma_bs, ma_dv, ngay_kham, chan_doan, ghi_chu))
        return ma_pk, True
    except Exception as e:
        print(f"Lỗi khi tạo phiếu khám: {e}")
        return None, False

def update_phieu_kham(ma_pk, ma_bn, ma_bs, ma_dv, chan_doan=None, ghi_chu=None, ngay_kham=None):
    """
    Cập nhật thông tin phiếu khám
    """
    query = """
    UPDATE PHIEUKHAM
    SET MaBN = %s, MaBS = %s, MaDV = %s, NgayKham = %s, ChanDoan = %s, GhiChu = %s
    WHERE MaPK = %s
    """
    
    try:
        execute_query(query, (ma_bn, ma_bs, ma_dv, ngay_kham, chan_doan, ghi_chu, ma_pk))
        return True
    except Exception as e:
        print(f"Lỗi khi cập nhật phiếu khám: {e}")
        return False

def delete_phieu_kham(ma_pk):
    """
    Xóa phiếu khám theo mã
    """
    query = "DELETE FROM PHIEUKHAM WHERE MaPK = %s"
    try:
        execute_query(query, (ma_pk,))
        return True
    except Exception as e:
        print(f"Lỗi khi xóa phiếu khám: {e}")
        return False