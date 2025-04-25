from .db import execute_query

def generate_next_id(table_name, id_field, prefix, length):
    """
    Tạo ID tiếp theo cho bảng dựa trên ID lớn nhất hiện tại
    
    Args:
        table_name (str): Tên bảng
        id_field (str): Tên trường ID
        prefix (str): Tiền tố của ID (ví dụ: 'BN', 'BS', 'DV', 'LH', 'PK')
        length (int): Độ dài của phần số trong ID
        
    Returns:
        str: ID tiếp theo
    """
    query = f"SELECT MAX({id_field}) as max_id FROM {table_name}"
    result = execute_query(query, fetch=True)
    
    if not result or not result[0]['max_id']:
        # Nếu không có ID nào, tạo ID đầu tiên
        return f"{prefix}{'0' * (length - 1)}1"
    
    # Lấy ID lớn nhất hiện tại
    max_id = result[0]['max_id']
    
    # Tách phần số từ ID
    numeric_part = max_id[len(prefix):]
    
    # Tăng giá trị lên 1
    next_numeric_value = int(numeric_part) + 1
    
    # Tạo ID mới với định dạng chuẩn
    next_id = f"{prefix}{next_numeric_value:0{length}d}"
    
    return next_id

def get_next_benh_nhan_id():
    """
    Tạo mã bệnh nhân tiếp theo
    
    Returns:
        str: Mã bệnh nhân mới
    """
    return generate_next_id('BENHNHAN', 'MaBN', 'BN', 5)

def get_next_bac_si_id():
    """
    Tạo mã bác sĩ tiếp theo
    
    Returns:
        str: Mã bác sĩ mới
    """
    return generate_next_id('BACSI', 'MaBS', 'BS', 8)

def get_next_dich_vu_id():
    """
    Tạo mã dịch vụ tiếp theo
    
    Returns:
        str: Mã dịch vụ mới
    """
    return generate_next_id('DICHVU', 'MaDV', 'DV', 8)

def get_next_lich_hen_id():
    """
    Tạo mã lịch hẹn tiếp theo
    
    Returns:
        str: Mã lịch hẹn mới
    """
    return generate_next_id('LICHHEN', 'MaLH', 'LH', 5)

def get_next_phieu_kham_id():
    """
    Tạo mã phiếu khám tiếp theo
    
    Returns:
        str: Mã phiếu khám mới
    """
    return generate_next_id('PHIEUKHAM', 'MaPK', 'PK', 5)