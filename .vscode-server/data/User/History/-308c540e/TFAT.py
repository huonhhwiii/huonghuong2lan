from .db import execute_query
import datetime
from .utils import get_next_hoa_don_id

def get_all_hoa_don():
    """
    Lấy danh sách tất cả hóa đơn
    
    Returns:
        list: Danh sách hóa đơn
    """
    query = """
    SELECT h.*, p.MaBN, p.MaBS, p.MaDV, p.NgayKham, 
           bn.HoTen as TenBenhNhan, 
           bs.HoTen as TenBacSi,
           dv.TenDV, dv.Gia
    FROM HOADON h
    JOIN PHIEUKHAM p ON h.MaPK = p.MaPK
    JOIN BENHNHAN bn ON p.MaBN = bn.MaBN
    JOIN BACSI bs ON p.MaBS = bs.MaBS
    JOIN DICHVU dv ON p.MaDV = dv.MaDV
    ORDER BY h.NgayLap DESC
    """
    return execute_query(query, fetch=True)

def get_hoa_don_by_id(ma_hd):
    """
    Lấy thông tin hóa đơn theo mã
    
    Args:
        ma_hd (str): Mã hóa đơn
        
    Returns:
        dict: Thông tin hóa đơn
    """
    query = """
    SELECT h.*, p.MaBN, p.MaBS, p.MaDV, p.NgayKham, 
           bn.HoTen as TenBenhNhan, 
           bs.HoTen as TenBacSi,
           dv.TenDV, dv.Gia
    FROM HOADON h
    JOIN PHIEUKHAM p ON h.MaPK = p.MaPK
    JOIN BENHNHAN bn ON p.MaBN = bn.MaBN
    JOIN BACSI bs ON p.MaBS = bs.MaBS
    JOIN DICHVU dv ON p.MaDV = dv.MaDV
    WHERE h.MaHD = %s
    """
    result = execute_query(query, (ma_hd,), fetch=True)
    return result[0] if result else None

def search_hoa_don(tu_khoa, loai_tim_kiem='ma_hoa_don'):
    """
    Tìm kiếm hóa đơn theo từ khóa và loại tìm kiếm
    
    Args:
        tu_khoa (str): Từ khóa tìm kiếm
        loai_tim_kiem (str): Loại tìm kiếm (ma_hoa_don, ma_phieu_kham, ma_benh_nhan)
        
    Returns:
        list: Danh sách hóa đơn tìm thấy
    """
    if loai_tim_kiem == 'ma_hoa_don':
        query = """
        SELECT h.*, p.MaBN, p.MaBS, p.MaDV, p.NgayKham, 
               bn.HoTen as TenBenhNhan, 
               bs.HoTen as TenBacSi,
               dv.TenDV, dv.Gia
        FROM HOADON h
        JOIN PHIEUKHAM p ON h.MaPK = p.MaPK
        JOIN BENHNHAN bn ON p.MaBN = bn.MaBN
        JOIN BACSI bs ON p.MaBS = bs.MaBS
        JOIN DICHVU dv ON p.MaDV = dv.MaDV
        WHERE h.MaHD LIKE %s
        """
    elif loai_tim_kiem == 'ma_phieu_kham':
        query = """
        SELECT h.*, p.MaBN, p.MaBS, p.MaDV, p.NgayKham, 
               bn.HoTen as TenBenhNhan, 
               bs.HoTen as TenBacSi,
               dv.TenDV, dv.Gia
        FROM HOADON h
        JOIN PHIEUKHAM p ON h.MaPK = p.MaPK
        JOIN BENHNHAN bn ON p.MaBN = bn.MaBN
        JOIN BACSI bs ON p.MaBS = bs.MaBS
        JOIN DICHVU dv ON p.MaDV = dv.MaDV
        WHERE h.MaPK LIKE %s
        """
    elif loai_tim_kiem == 'ma_benh_nhan':
        query = """
        SELECT h.*, p.MaBN, p.MaBS, p.MaDV, p.NgayKham, 
               bn.HoTen as TenBenhNhan, 
               bs.HoTen as TenBacSi,
               dv.TenDV, dv.Gia
        FROM HOADON h
        JOIN PHIEUKHAM p ON h.MaPK = p.MaPK
        JOIN BENHNHAN bn ON p.MaBN = bn.MaBN
        JOIN BACSI bs ON p.MaBS = bs.MaBS
        JOIN DICHVU dv ON p.MaDV = dv.MaDV
        WHERE p.MaBN LIKE %s
        """
    else:
        return []
        
    return execute_query(query, (f'%{tu_khoa}%',), fetch=True)

def create_hoa_don(ma_pk, phuong_thuc_thanh_toan, ma_hd=None, ngay_lap=None):
    """
    Tạo mới hóa đơn
    
    Args:
        ma_pk (str): Mã phiếu khám
        phuong_thuc_thanh_toan (str): Phương thức thanh toán
        ma_hd (str, optional): Mã hóa đơn (nếu không cung cấp sẽ tự động tạo)
        ngay_lap (str, optional): Ngày lập hóa đơn (định dạng YYYY-MM-DD HH:MM:SS)
        
    Returns:
        tuple: (ma_hd, success) - Mã hóa đơn và kết quả thành công hay không
    """
    # Nếu không có mã hóa đơn, tạo mã mới
    if not ma_hd:
        ma_hd = get_next_hoa_don_id()
        
    # Nếu không có ngày lập, sử dụng ngày hiện tại
    if not ngay_lap:
        ngay_lap = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Lấy thông tin giá dịch vụ từ phiếu khám
    query_gia = """
    SELECT dv.Gia
    FROM PHIEUKHAM pk
    JOIN DICHVU dv ON pk.MaDV = dv.MaDV
    WHERE pk.MaPK = %s
    """
    result = execute_query(query_gia, (ma_pk,), fetch=True)
    
    if not result:
        return None, False
    
    tong_tien = result[0]['Gia']
    
    # Tạo hóa đơn mới
    query = """
    INSERT INTO HOADON (MaHD, MaPK, NgayLap, TongTien, PhuongThucThanhToan)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    try:
        execute_query(query, (ma_hd, ma_pk, ngay_lap, tong_tien, phuong_thuc_thanh_toan))
        return ma_hd, True
    except Exception as e:
        print(f"Lỗi khi tạo hóa đơn: {e}")
        return None, False

def update_hoa_don(ma_hd, ma_pk, phuong_thuc_thanh_toan, trang_thai=None):
    """
    Cập nhật thông tin hóa đơn
    
    Args:
        ma_hd (str): Mã hóa đơn
        ma_pk (str): Mã phiếu khám
        phuong_thuc_thanh_toan (str): Phương thức thanh toán
        trang_thai (str, optional): Trạng thái hóa đơn
        
    Returns:
        bool: Kết quả cập nhật
    """
    # Lấy thông tin giá dịch vụ từ phiếu khám
    query_gia = """
    SELECT dv.Gia
    FROM PHIEUKHAM pk
    JOIN DICHVU dv ON pk.MaDV = dv.MaDV
    WHERE pk.MaPK = %s
    """
    result = execute_query(query_gia, (ma_pk,), fetch=True)
    
    if not result:
        return False
    
    tong_tien = result[0]['Gia']
    
    # Cập nhật hóa đơn
    if trang_thai:
        query = """
        UPDATE HOADON
        SET MaPK = %s, TongTien = %s, PhuongThucThanhToan = %s, TrangThai = %s
        WHERE MaHD = %s
        """
        params = (ma_pk, tong_tien, phuong_thuc_thanh_toan, trang_thai, ma_hd)
    else:
        query = """
        UPDATE HOADON
        SET MaPK = %s, TongTien = %s, PhuongThucThanhToan = %s
        WHERE MaHD = %s
        """
        params = (ma_pk, tong_tien, phuong_thuc_thanh_toan, ma_hd)
    
    try:
        execute_query(query, params)
        return True
    except Exception as e:
        print(f"Lỗi khi cập nhật hóa đơn: {e}")
        return False

def delete_hoa_don(ma_hd):
    """
    Xóa hóa đơn theo mã
    
    Args:
        ma_hd (str): Mã hóa đơn
        
    Returns:
        tuple: (success, message) - Kết quả xóa và thông báo
    """
    query = "DELETE FROM HOADON WHERE MaHD = %s"
    try:
        execute_query(query, (ma_hd,))
        return True, "Xóa hóa đơn thành công"
    except Exception as e:
        print(f"Lỗi khi xóa hóa đơn: {e}")
        return False, f"Lỗi: {str(e)}"

def get_phieu_kham_chua_thanh_toan():
    """
    Lấy danh sách phiếu khám chưa có hóa đơn
    
    Returns:
        list: Danh sách phiếu khám chưa thanh toán
    """
    query = """
    SELECT p.*, bn.HoTen as TenBenhNhan, bs.HoTen as TenBacSi, dv.TenDV, dv.Gia
    FROM PHIEUKHAM p
    JOIN BENHNHAN bn ON p.MaBN = bn.MaBN
    JOIN BACSI bs ON p.MaBS = bs.MaBS
    JOIN DICHVU dv ON p.MaDV = dv.MaDV
    WHERE p.MaPK NOT IN (SELECT MaPK FROM HOADON)
    ORDER BY p.NgayKham DESC
    """
    return execute_query(query, fetch=True)