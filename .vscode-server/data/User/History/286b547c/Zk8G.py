from .db import execute_query
from .utils import get_next_dich_vu_id

def get_all_dich_vu():
    """
    Lấy danh sách tất cả dịch vụ
    """
    try:
        query = """
        SELECT * FROM DICHVU
        ORDER BY MaDV
        """
        result = execute_query(query, fetch=True)
        # Đảm bảo giá trị Gia là số
        for item in result:
            if item['Gia'] is None:
                item['Gia'] = 0
            elif isinstance(item['Gia'], str):
                try:
                    item['Gia'] = float(item['Gia'])
                except ValueError:
                    item['Gia'] = 0
        return result
    except Exception as e:
        print(f"Lỗi trong hàm get_all_dich_vu: {str(e)}")
        raise

def get_dich_vu_by_id(ma_dv):
    """
    Lấy thông tin dịch vụ theo mã
    """
    try:
        query = """
        SELECT * FROM DICHVU
        WHERE MaDV = %s
        """
        result = execute_query(query, (ma_dv,), fetch=True)
        
        if result and len(result) > 0:
            dich_vu = result[0]
            # Đảm bảo giá trị Gia là số
            if dich_vu['Gia'] is None:
                dich_vu['Gia'] = 0
            elif isinstance(dich_vu['Gia'], str):
                try:
                    dich_vu['Gia'] = float(dich_vu['Gia'])
                except ValueError:
                    dich_vu['Gia'] = 0
            return dich_vu
        return None
    except Exception as e:
        print(f"Lỗi trong hàm get_dich_vu_by_id: {str(e)}")
        raise

def search_dich_vu(tu_khoa, loai_tim_kiem='ma_dv'):
    """
    Tìm kiếm dịch vụ theo từ khóa và loại tìm kiếm
    
    Args:
        tu_khoa (str): Từ khóa tìm kiếm
        loai_tim_kiem (str): Loại tìm kiếm (ma_dv, ten_dv, gia)
        
    Returns:
        list: Danh sách dịch vụ tìm thấy
    """
    try:
        # Kiểm tra từ khóa trống
        if not tu_khoa or tu_khoa.strip() == '':
            print("Từ khóa tìm kiếm trống")
            return []
        
        # Chuẩn hóa từ khóa
        tu_khoa = tu_khoa.strip()
        print(f"Tìm kiếm với từ khóa: '{tu_khoa}', loại: '{loai_tim_kiem}'")
            
        if loai_tim_kiem == 'ma_dv':
            query = """
            SELECT * FROM DICHVU
            WHERE MaDV LIKE %s
            ORDER BY MaDV
            """
            result = execute_query(query, (f'%{tu_khoa}%',), fetch=True)
            print(f"Tìm theo mã dịch vụ, kết quả: {len(result)} dịch vụ")
            
        elif loai_tim_kiem == 'ten_dv':
            query = """
            SELECT * FROM DICHVU
            WHERE TenDV LIKE %s
            ORDER BY TenDV
            """
            result = execute_query(query, (f'%{tu_khoa}%',), fetch=True)
            print(f"Tìm theo tên dịch vụ, kết quả: {len(result)} dịch vụ")
            
        elif loai_tim_kiem == 'gia':
            # Tìm kiếm theo khoảng giá
            try:
                # Kiểm tra xem có phải là khoảng giá (VD: 100000-200000)
                if '-' in tu_khoa:
                    parts = tu_khoa.split('-')
                    if len(parts) == 2:
                        gia_min = float(parts[0].strip())
                        gia_max = float(parts[1].strip())
                        
                        query = """
                        SELECT * FROM DICHVU
                        WHERE Gia BETWEEN %s AND %s
                        ORDER BY Gia
                        """
                        result = execute_query(query, (gia_min, gia_max), fetch=True)
                        print(f"Tìm theo khoảng giá {gia_min}-{gia_max}, kết quả: {len(result)} dịch vụ")
                    else:
                        print("Định dạng khoảng giá không hợp lệ")
                        return []
                else:
                    # Tìm kiếm giá gần đúng
                    gia = float(tu_khoa)
                    # Tìm trong khoảng ±10% của giá nhập vào
                    gia_min = gia * 0.9
                    gia_max = gia * 1.1
                    
                    query = """
                    SELECT * FROM DICHVU
                    WHERE Gia BETWEEN %s AND %s
                    ORDER BY ABS(Gia - %s)
                    """
                    result = execute_query(query, (gia_min, gia_max, gia), fetch=True)
                    print(f"Tìm theo giá gần đúng {gia} (±10%), kết quả: {len(result)} dịch vụ")
            except ValueError as ve:
                # Nếu không phải số, trả về danh sách rỗng
                print(f"Lỗi định dạng giá: {str(ve)}")
                return []
        else:
            print(f"Loại tìm kiếm không hợp lệ: {loai_tim_kiem}")
            return []
            
        # Đảm bảo giá trị Gia là số
        for item in result:
            if item['Gia'] is None:
                item['Gia'] = 0
            elif isinstance(item['Gia'], str):
                try:
                    item['Gia'] = float(item['Gia'])
                except ValueError:
                    item['Gia'] = 0
                    
        return result
    except Exception as e:
        print(f"Lỗi trong hàm search_dich_vu: {str(e)}")
        return []

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
    try:
        # Nếu không có mã dịch vụ, tạo mã mới
        if not ma_dv:
            ma_dv = get_next_dich_vu_id()
            
        # Đảm bảo giá trị gia là số
        if gia is None:
            gia = 0
        else:
            try:
                gia = float(gia)
            except (ValueError, TypeError):
                gia = 0
                
        query = """
        INSERT INTO DICHVU (MaDV, TenDV, Gia)
        VALUES (%s, %s, %s)
        """
        
        execute_query(query, (ma_dv, ten_dv, gia))
        return ma_dv, True
    except Exception as e:
        print(f"Lỗi khi tạo dịch vụ: {e}")
        return None, False

def update_dich_vu(ma_dv, ten_dv, gia):
    """
    Cập nhật thông tin dịch vụ
    
    Args:
        ma_dv (str): Mã dịch vụ
        ten_dv (str): Tên dịch vụ mới
        gia (float): Giá dịch vụ mới
        
    Returns:
        bool: Kết quả cập nhật thành công hay không
    """
    try:
        # Đảm bảo giá trị gia là số
        if gia is None:
            gia = 0
        else:
            try:
                gia = float(gia)
            except (ValueError, TypeError):
                gia = 0
                
        query = """
        UPDATE DICHVU
        SET TenDV = %s, Gia = %s
        WHERE MaDV = %s
        """
        
        execute_query(query, (ten_dv, gia, ma_dv))
        return True
    except Exception as e:
        print(f"Lỗi khi cập nhật dịch vụ: {e}")
        return False

def delete_dich_vu(ma_dv):
    """
    Xóa dịch vụ theo mã
    
    Args:
        ma_dv (str): Mã dịch vụ cần xóa
        
    Returns:
        tuple: (success, message) - Kết quả xóa và thông báo
    """
    try:
        # Kiểm tra xem dịch vụ có tồn tại không
        dich_vu = get_dich_vu_by_id(ma_dv)
        if not dich_vu:
            return False, "Không tìm thấy dịch vụ cần xóa"
            
        # Kiểm tra xem dịch vụ có đang được sử dụng trong phiếu khám không
        check_query = """
        SELECT COUNT(*) as count FROM PHIEUKHAM
        WHERE MaDV = %s
        """
        result = execute_query(check_query, (ma_dv,), fetch=True)
        
        if result and result[0]['count'] > 0:
            return False, "Không thể xóa dịch vụ đang được sử dụng trong phiếu khám"
        
        query = "DELETE FROM DICHVU WHERE MaDV = %s"
        execute_query(query, (ma_dv,))
        return True, "Xóa dịch vụ thành công"
    except Exception as e:
        print(f"Lỗi khi xóa dịch vụ: {e}")
        return False, f"Lỗi: {str(e)}"