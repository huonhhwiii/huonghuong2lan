from .db import execute_query
from .utils import get_next_dich_vu_id

def get_all_dich_vu():
    """
    Lấy danh sách tất cả dịch vụ
    """
    query = """
    SELECT * FROM DICHVU
    ORDER BY MaDV
    """
    return execute_query(query, fetch=True)

def get_dich_vu_by_id(ma_dv):
    """
    Lấy thông tin dịch vụ theo mã
    """
    query = """
    SELECT * FROM DICHVU
    WHERE MaDV = %s
    """
    result = execute_query(query, (ma_dv,), fetch=True)
    return result[0] if result else None

def search_dich_vu(tu_khoa, loai_tim_kiem='ma_dv'):
    """
    Tìm kiếm dịch vụ theo từ khóa và loại tìm kiếm
    
    Args:
        tu_khoa (str): Từ khóa tìm kiếm
        loai_tim_kiem (str): Loại tìm kiếm (ma_dv, ten_dv, gia)
        
    Returns:
        list: Danh sách dịch vụ tìm thấy
    """
    if loai_tim_kiem == 'ma_dv':
        query = """
        SELECT * FROM DICHVU
        WHERE MaDV LIKE %s
        """
    elif loai_tim_kiem == 'ten_dv':
        query = """
        SELECT * FROM DICHVU
        WHERE TenDV LIKE %s
        """
    elif loai_tim_kiem == 'gia':
        # Tìm kiếm theo khoảng giá
        try:
            gia = float(tu_khoa)
            query = """
            SELECT * FROM DICHVU
            WHERE Gia = %s
            """
            return execute_query(query, (gia,), fetch=True)
        except ValueError:
            # Nếu không phải số, trả về danh sách rỗng
            return []
    else:
        return []
        
    return execute_query(query, (f'%{tu_khoa}%',), fetch=True)

def create_dich_vu(ten_dv, gia, ma_dv=None):
    """
    Tạo mới dịch vụ
    
    Args:
        ten_dv (str): Tên dịch vụ
        gia (float): Giá dịch vụ
        ma_dv (str, optional): Mã dịch vụ (nếu không cung cấp sẽ tự động tạo)
        
    Returns:
        tuple: (ma_dv, success) - Mã dịch vụ và kết quả thành công hay không
    """
    # Nếu không có mã dịch vụ, tạo mã mới
    if not ma_dv:
        ma_dv = get_next_dich_vu_id()
        
    query = """
    INSERT INTO DICHVU (MaDV, TenDV, Gia)
    VALUES (%s, %s, %s)
    """
    
    try:
        execute_query(query, (ma_dv, ten_dv, gia))
        return ma_dv, True
    except Exception as e:
        print(f"Lỗi khi tạo dịch vụ: {e}")
        return None, False

def update_dich_vu(ma_dv, ten_dv, gia):
    """
    Cập nhật thông tin dịch vụ
    """
    query = """
    UPDATE DICHVU
    SET TenDV = %s, Gia = %s
    WHERE MaDV = %s
    """
    
    try:
        execute_query(query, (ten_dv, gia, ma_dv))
        return True
    except Exception as e:
        print(f"Lỗi khi cập nhật dịch vụ: {e}")
        return False

def delete_dich_vu(ma_dv):
    """
    Xóa dịch vụ theo mã
    """
    # Kiểm tra xem dịch vụ có đang được sử dụng trong phiếu khám không
    check_query = """
    SELECT COUNT(*) as count FROM PHIEUKHAM
    WHERE MaDV = %s
    """
    result = execute_query(check_query, (ma_dv,), fetch=True)
    
    if result and result[0]['count'] > 0:
        return False, "Không thể xóa dịch vụ đang được sử dụng trong phiếu khám"
    
    query = "DELETE FROM DICHVU WHERE MaDV = %s"
    try:
        execute_query(query, (ma_dv,))
        return True, "Xóa dịch vụ thành công"
    except Exception as e:
        print(f"Lỗi khi xóa dịch vụ: {e}")
        return False, f"Lỗi: {str(e)}"