from .db import execute_query
import datetime
from .utils import get_next_bac_si_id

def get_all_bac_si():
    """
    Lấy danh sách tất cả bác sĩ
    """
    try:
        query = "SELECT * FROM BACSI ORDER BY MaBS"
        result = execute_query(query, fetch=True)
        return result if result else []
    except Exception as e:
        print(f"Lỗi khi lấy danh sách bác sĩ: {e}")
        raise Exception(f"Không thể lấy danh sách bác sĩ: {str(e)}")

def get_bac_si_by_id(ma_bs):
    """
    Lấy thông tin bác sĩ theo mã
    """
    try:
        query = "SELECT * FROM BACSI WHERE MaBS = ?"
        result = execute_query(query, (ma_bs,), fetch=True)
        return result[0] if result else None
    except Exception as e:
        print(f"Lỗi khi lấy thông tin bác sĩ: {e}")
        raise Exception(f"Không thể lấy thông tin bác sĩ: {str(e)}")

def search_bac_si(tu_khoa, loai_tim_kiem='ma_bac_si'):
    """
    Tìm kiếm bác sĩ theo từ khóa và loại tìm kiếm
    
    Args:
        tu_khoa (str): Từ khóa tìm kiếm
        loai_tim_kiem (str): Loại tìm kiếm (ma_bac_si, so_dien_thoai, ho_ten)
        
    Returns:
        list: Danh sách bác sĩ tìm thấy
    """
    try:
        if loai_tim_kiem == 'ma_bac_si':
            query = "SELECT * FROM BACSI WHERE MaBS LIKE ?"
        elif loai_tim_kiem == 'so_dien_thoai':
            query = "SELECT * FROM BACSI WHERE Sdt LIKE ?"
        elif loai_tim_kiem == 'ho_ten':
            # Sử dụng COLLATE NOCASE để tìm kiếm không phân biệt chữ hoa chữ thường
            query = "SELECT * FROM BACSI WHERE HoTen LIKE ? COLLATE NOCASE"
        else:
            return []
            
        result = execute_query(query, (f'%{tu_khoa}%',), fetch=True)
        return result if result else []
    except Exception as e:
        print(f"Lỗi khi tìm kiếm bác sĩ: {e}")
        raise Exception(f"Không thể tìm kiếm bác sĩ: {str(e)}")

def create_bac_si(ho_ten, so_dien_thoai, ma_bs=None):
    """
    Tạo mới bác sĩ
    
    Args:
        ho_ten (str): Họ tên bác sĩ
        so_dien_thoai (str): Số điện thoại
        ma_bs (str, optional): Mã bác sĩ (nếu không cung cấp sẽ tự động tạo)
        
    Returns:
        tuple: (ma_bs, success) - Mã bác sĩ và kết quả thành công hay không
    """
    # Nếu không có mã bác sĩ, tạo mã mới
    if not ma_bs:
        ma_bs = get_next_bac_si_id()
        
    query = """
    INSERT INTO BACSI (MaBS, HoTen, Sdt)
    VALUES (?, ?, ?)
    """
    
    try:
        execute_query(query, (ma_bs, ho_ten, so_dien_thoai))
        return ma_bs, True
    except Exception as e:
        print(f"Lỗi khi tạo bác sĩ: {e}")
        return None, False

def update_bac_si(ma_bs, ho_ten, so_dien_thoai):
    """
    Cập nhật thông tin bác sĩ
    """
    query = """
    UPDATE BACSI
    SET HoTen = ?, Sdt = ?
    WHERE MaBS = ?
    """
    
    try:
        execute_query(query, (ho_ten, so_dien_thoai, ma_bs))
        return True
    except Exception as e:
        print(f"Lỗi khi cập nhật bác sĩ: {e}")
        return False

def delete_bac_si(ma_bs):
    """
    Xóa bác sĩ theo mã
    """
    query = "DELETE FROM BACSI WHERE MaBS = ?"
    execute_query(query, (ma_bs,))