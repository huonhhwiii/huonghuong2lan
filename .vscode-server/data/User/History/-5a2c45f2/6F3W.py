from .db import execute_query
import datetime

def thong_ke_dich_vu_su_dung(tu_ngay=None, den_ngay=None):
    """
    Thống kê dịch vụ sử dụng thông qua phiếu khám
    
    Args:
        tu_ngay (str, optional): Ngày bắt đầu thống kê (định dạng YYYY-MM-DD)
        den_ngay (str, optional): Ngày kết thúc thống kê (định dạng YYYY-MM-DD)
        
    Returns:
        list: Danh sách dịch vụ đã sử dụng và số lượng
    """
    try:
        # Xây dựng câu truy vấn cơ bản
        query = """
        SELECT 
            dv.MaDV, 
            dv.TenDV, 
            dv.Gia, 
            COUNT(pk.MaPK) as SoLuotSuDung,
            SUM(dv.Gia) as TongTien
        FROM DICHVU dv
        LEFT JOIN PHIEUKHAM pk ON dv.MaDV = pk.MaDV
        """
        
        params = []
        where_clauses = []
        
        # Thêm điều kiện lọc theo ngày nếu có
        if tu_ngay:
            where_clauses.append("pk.NgayKham >= ?")
            params.append(tu_ngay)
            
        if den_ngay:
            where_clauses.append("pk.NgayKham <= ?")
            params.append(den_ngay + " 23:59:59")  # Kết thúc ngày
            
        # Thêm điều kiện WHERE nếu có
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
            
        # Nhóm theo dịch vụ và sắp xếp theo số lượt sử dụng giảm dần
        query += """
        GROUP BY dv.MaDV, dv.TenDV, dv.Gia
        ORDER BY SoLuotSuDung DESC, dv.TenDV
        """
        
        # Thực thi truy vấn
        result = execute_query(query, tuple(params) if params else None, fetch=True)
        
        # Tính tổng số lượt sử dụng và tổng tiền
        tong_luot_su_dung = sum(item['SoLuotSuDung'] for item in result)
        tong_tien = sum(item['TongTien'] if item['TongTien'] else 0 for item in result)
        
        # Thêm thông tin tổng hợp
        summary = {
            'tong_luot_su_dung': tong_luot_su_dung,
            'tong_tien': tong_tien
        }
        
        return result, summary
        
    except Exception as e:
        print(f"Lỗi khi thống kê dịch vụ sử dụng: {e}")
        return [], {'tong_luot_su_dung': 0, 'tong_tien': 0}

def thong_ke_dich_vu_theo_thang(nam=None, thang=None):
    """
    Thống kê dịch vụ sử dụng theo tháng
    
    Args:
        nam (int, optional): Năm thống kê (mặc định là năm hiện tại)
        thang (int, optional): Tháng thống kê (mặc định là tất cả các tháng trong năm)
        
    Returns:
        list: Danh sách dịch vụ đã sử dụng và số lượng theo tháng
    """
    try:
        # Nếu không có năm, lấy năm hiện tại
        if not nam:
            nam = datetime.datetime.now().year
            
        # Xây dựng câu truy vấn cơ bản
        query = """
        SELECT 
            strftime('%m', pk.NgayKham) as Thang,
            dv.MaDV, 
            dv.TenDV, 
            COUNT(pk.MaPK) as SoLuotSuDung,
            SUM(dv.Gia) as TongTien
        FROM DICHVU dv
        JOIN PHIEUKHAM pk ON dv.MaDV = pk.MaDV
        WHERE strftime('%Y', pk.NgayKham) = ?
        """
        
        params = [str(nam)]
        
        # Thêm điều kiện lọc theo tháng nếu có
        if thang:
            query += " AND strftime('%m', pk.NgayKham) = ?"
            # Đảm bảo tháng có 2 chữ số
            params.append(f"{thang:02d}")
            
        # Nhóm theo tháng và dịch vụ, sắp xếp theo tháng và số lượt sử dụng
        query += """
        GROUP BY Thang, dv.MaDV, dv.TenDV
        ORDER BY Thang, SoLuotSuDung DESC
        """
        
        # Thực thi truy vấn
        result = execute_query(query, tuple(params), fetch=True)
        
        # Tổ chức kết quả theo tháng
        thong_ke_theo_thang = {}
        for item in result:
            thang_key = item['Thang']
            if thang_key not in thong_ke_theo_thang:
                thong_ke_theo_thang[thang_key] = {
                    'thang': int(thang_key),
                    'dich_vu': [],
                    'tong_luot_su_dung': 0,
                    'tong_tien': 0
                }
                
            thong_ke_theo_thang[thang_key]['dich_vu'].append(item)
            thong_ke_theo_thang[thang_key]['tong_luot_su_dung'] += item['SoLuotSuDung']
            thong_ke_theo_thang[thang_key]['tong_tien'] += item['TongTien'] if item['TongTien'] else 0
            
        # Chuyển từ dictionary sang list và sắp xếp theo tháng
        ket_qua = list(thong_ke_theo_thang.values())
        ket_qua.sort(key=lambda x: x['thang'])
        
        return ket_qua
        
    except Exception as e:
        print(f"Lỗi khi thống kê dịch vụ theo tháng: {e}")
        return []

def thong_ke_dich_vu_theo_bac_si(ma_bac_si=None, tu_ngay=None, den_ngay=None):
    """
    Thống kê dịch vụ sử dụng theo bác sĩ
    
    Args:
        ma_bac_si (str, optional): Mã bác sĩ cần thống kê (mặc định là tất cả bác sĩ)
        tu_ngay (str, optional): Ngày bắt đầu thống kê (định dạng YYYY-MM-DD)
        den_ngay (str, optional): Ngày kết thúc thống kê (định dạng YYYY-MM-DD)
        
    Returns:
        list: Danh sách dịch vụ đã sử dụng và số lượng theo bác sĩ
    """
    try:
        # Xây dựng câu truy vấn cơ bản
        query = """
        SELECT 
            bs.MaBS,
            bs.HoTen as TenBacSi,
            dv.MaDV, 
            dv.TenDV, 
            COUNT(pk.MaPK) as SoLuotSuDung,
            SUM(dv.Gia) as TongTien
        FROM DICHVU dv
        JOIN PHIEUKHAM pk ON dv.MaDV = pk.MaDV
        JOIN BACSI bs ON pk.MaBS = bs.MaBS
        """
        
        params = []
        where_clauses = []
        
        # Thêm điều kiện lọc theo bác sĩ nếu có
        if ma_bac_si:
            where_clauses.append("bs.MaBS = ?")
            params.append(ma_bac_si)
            
        # Thêm điều kiện lọc theo ngày nếu có
        if tu_ngay:
            where_clauses.append("pk.NgayKham >= ?")
            params.append(tu_ngay)
            
        if den_ngay:
            where_clauses.append("pk.NgayKham <= ?")
            params.append(den_ngay + " 23:59:59")  # Kết thúc ngày
            
        # Thêm điều kiện WHERE nếu có
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
            
        # Nhóm theo bác sĩ và dịch vụ, sắp xếp theo bác sĩ và số lượt sử dụng
        query += """
        GROUP BY bs.MaBS, bs.HoTen, dv.MaDV, dv.TenDV
        ORDER BY bs.HoTen, SoLuotSuDung DESC
        """
        
        # Thực thi truy vấn
        result = execute_query(query, tuple(params) if params else None, fetch=True)
        
        # Tổ chức kết quả theo bác sĩ
        thong_ke_theo_bac_si = {}
        for item in result:
            ma_bs = item['MaBS']
            if ma_bs not in thong_ke_theo_bac_si:
                thong_ke_theo_bac_si[ma_bs] = {
                    'ma_bac_si': ma_bs,
                    'ten_bac_si': item['TenBacSi'],
                    'dich_vu': [],
                    'tong_luot_su_dung': 0,
                    'tong_tien': 0
                }
                
            thong_ke_theo_bac_si[ma_bs]['dich_vu'].append({
                'MaDV': item['MaDV'],
                'TenDV': item['TenDV'],
                'SoLuotSuDung': item['SoLuotSuDung'],
                'TongTien': item['TongTien']
            })
            thong_ke_theo_bac_si[ma_bs]['tong_luot_su_dung'] += item['SoLuotSuDung']
            thong_ke_theo_bac_si[ma_bs]['tong_tien'] += item['TongTien'] if item['TongTien'] else 0
            
        # Chuyển từ dictionary sang list và sắp xếp theo tên bác sĩ
        ket_qua = list(thong_ke_theo_bac_si.values())
        ket_qua.sort(key=lambda x: x['ten_bac_si'])
        
        return ket_qua
        
    except Exception as e:
        print(f"Lỗi khi thống kê dịch vụ theo bác sĩ: {e}")
        return []