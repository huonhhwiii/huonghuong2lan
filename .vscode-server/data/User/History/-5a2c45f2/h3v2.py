import sqlite3
import json
from datetime import datetime, timedelta
import calendar

def get_connection():
    conn = sqlite3.connect('nhakhoaso.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_tong_quan_bao_cao():
    """Lấy thông tin tổng quan cho trang báo cáo chính"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Lấy tổng số bệnh nhân
    cursor.execute("SELECT COUNT(*) as tong_benh_nhan FROM BENHNHAN")
    tong_benh_nhan = cursor.fetchone()['tong_benh_nhan']
    
    # Lấy tổng số dịch vụ
    cursor.execute("SELECT COUNT(*) as tong_dich_vu FROM DICHVU")
    tong_dich_vu = cursor.fetchone()['tong_dich_vu']
    
    # Lấy tổng số lịch hẹn
    cursor.execute("SELECT COUNT(*) as tong_lich_hen FROM LICHHEN")
    tong_lich_hen = cursor.fetchone()['tong_lich_hen']
    
    # Lấy tổng doanh thu
    cursor.execute("SELECT SUM(TongTien) as tong_doanh_thu FROM HOADON")
    result = cursor.fetchone()
    tong_doanh_thu = result['tong_doanh_thu'] if result['tong_doanh_thu'] else 0
    
    # Lấy dữ liệu cho biểu đồ dịch vụ
    cursor.execute("""
        SELECT dv.TenDV, COUNT(pk.MaDV) as so_luong
        FROM DICHVU dv
        LEFT JOIN PHIEUKHAM pk ON dv.MaDV = pk.MaDV
        GROUP BY dv.MaDV
        ORDER BY so_luong DESC
        LIMIT 5
    """)
    dich_vu_data = cursor.fetchall()
    
    dich_vu_labels = [row['TenDV'] for row in dich_vu_data]
    dich_vu_values = [row['so_luong'] for row in dich_vu_data]
    
    # Lấy dữ liệu cho biểu đồ bệnh nhân theo tháng
    current_year = datetime.now().year
    months = []
    benh_nhan_counts = []
    
    for month in range(1, 13):
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM BENHNHAN
            WHERE strftime('%Y', NgayTao) = ? AND strftime('%m', NgayTao) = ?
        """, (str(current_year), f"{month:02d}"))
        count = cursor.fetchone()['count']
        
        months.append(f"Tháng {month}")
        benh_nhan_counts.append(count)
    
    # Lấy dữ liệu cho biểu đồ doanh thu theo tháng
    doanh_thu_months = []
    doanh_thu_values = []
    
    for month in range(1, 13):
        cursor.execute("""
            SELECT SUM(TongTien) as doanh_thu
            FROM HOADON
            WHERE strftime('%Y', NgayLap) = ? AND strftime('%m', NgayLap) = ?
        """, (str(current_year), f"{month:02d}"))
        result = cursor.fetchone()
        doanh_thu = result['doanh_thu'] if result['doanh_thu'] else 0
        
        doanh_thu_months.append(f"Tháng {month}")
        doanh_thu_values.append(doanh_thu)
    
    # Lấy dữ liệu cho biểu đồ lượt khám theo tháng
    luot_kham_months = []
    luot_kham_counts = []
    
    for month in range(1, 13):
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM PHIEUKHAM
            WHERE strftime('%Y', NgayKham) = ? AND strftime('%m', NgayKham) = ?
        """, (str(current_year), f"{month:02d}"))
        count = cursor.fetchone()['count']
        
        luot_kham_months.append(f"Tháng {month}")
        luot_kham_counts.append(count)
    
    conn.close()
    
    return {
        'tong_benh_nhan': tong_benh_nhan,
        'tong_dich_vu': tong_dich_vu,
        'tong_lich_hen': tong_lich_hen,
        'tong_doanh_thu': tong_doanh_thu,
        'dich_vu_labels': json.dumps(dich_vu_labels),
        'dich_vu_data': json.dumps(dich_vu_values),
        'benh_nhan_labels': json.dumps(months),
        'benh_nhan_data': json.dumps(benh_nhan_counts),
        'doanh_thu_labels': json.dumps(doanh_thu_months),
        'doanh_thu_data': json.dumps(doanh_thu_values),
        'luot_kham_labels': json.dumps(luot_kham_months),
        'luot_kham_data': json.dumps(luot_kham_counts)
    }

def get_bao_cao_dich_vu(tu_ngay=None, den_ngay=None):
    """Lấy dữ liệu báo cáo dịch vụ"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Nếu không có ngày, lấy dữ liệu của tháng hiện tại
    if not tu_ngay or not den_ngay:
        today = datetime.now()
        first_day = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')
        last_day = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1]).strftime('%Y-%m-%d')
        tu_ngay = first_day
        den_ngay = last_day
    
    # Lấy danh sách dịch vụ và số lượng sử dụng
    cursor.execute("""
        SELECT dv.MaDV, dv.TenDV, dv.Gia, COUNT(pk.MaDV) as SoLuong, 
               SUM(dv.Gia) as DoanhThu
        FROM DICHVU dv
        LEFT JOIN PHIEUKHAM pk ON dv.MaDV = pk.MaDV
        LEFT JOIN HOADON hd ON pk.MaPK = hd.MaPK
        WHERE hd.NgayLap BETWEEN ? AND ?
        GROUP BY dv.MaDV
        ORDER BY SoLuong DESC
    """, (tu_ngay, den_ngay))
    
    dich_vu_list = []
    tong_so_luong = 0
    tong_doanh_thu = 0
    
    for row in cursor.fetchall():
        so_luong = row['SoLuong'] if row['SoLuong'] else 0
        doanh_thu = row['DoanhThu'] if row['DoanhThu'] else 0
        
        tong_so_luong += so_luong
        tong_doanh_thu += doanh_thu
        
        dich_vu_list.append({
            'MaDV': row['MaDV'],
            'TenDV': row['TenDV'],
            'Gia': row['Gia'],
            'SoLuong': so_luong,
            'DoanhThu': doanh_thu,
            'TyLe': 0  # Sẽ tính sau khi có tổng
        })
    
    # Tính tỷ lệ cho từng dịch vụ
    for dv in dich_vu_list:
        if tong_doanh_thu > 0:
            dv['TyLe'] = (dv['DoanhThu'] / tong_doanh_thu) * 100
        else:
            dv['TyLe'] = 0
    
    # Lấy dịch vụ phổ biến nhất
    dich_vu_pho_bien = dich_vu_list[0]['TenDV'] if dich_vu_list else "Không có dữ liệu"
    
    # Chuẩn bị dữ liệu cho biểu đồ
    dich_vu_labels = [dv['TenDV'] for dv in dich_vu_list]
    dich_vu_data = [dv['SoLuong'] for dv in dich_vu_list]
    doanh_thu_data = [dv['DoanhThu'] for dv in dich_vu_list]
    
    conn.close()
    
    return {
        'tu_ngay': tu_ngay,
        'den_ngay': den_ngay,
        'dich_vu_list': dich_vu_list,
        'tong_dich_vu': len(dich_vu_list),
        'tong_so_luong': tong_so_luong,
        'tong_doanh_thu': tong_doanh_thu,
        'dich_vu_pho_bien': dich_vu_pho_bien,
        'dich_vu_labels': json.dumps(dich_vu_labels),
        'dich_vu_data': json.dumps(dich_vu_data),
        'doanh_thu_data': json.dumps(doanh_thu_data)
    }

def get_bao_cao_benh_nhan(tu_ngay=None, den_ngay=None, loai_bao_cao='all'):
    """Lấy dữ liệu báo cáo bệnh nhân"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Nếu không có ngày, lấy dữ liệu của tháng hiện tại
    if not tu_ngay or not den_ngay:
        today = datetime.now()
        first_day = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')
        last_day = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1]).strftime('%Y-%m-%d')
        tu_ngay = first_day
        den_ngay = last_day
    
    # Lấy tổng số bệnh nhân
    if loai_bao_cao == 'new':
        cursor.execute("""
            SELECT COUNT(*) as tong_benh_nhan
            FROM BENHNHAN
            WHERE NgayTao BETWEEN ? AND ?
        """, (tu_ngay, den_ngay))
    else:
        cursor.execute("""
            SELECT COUNT(DISTINCT bn.MaBN) as tong_benh_nhan
            FROM BENHNHAN bn
            LEFT JOIN PHIEUKHAM pk ON bn.MaBN = pk.MaBN
            WHERE pk.NgayKham BETWEEN ? AND ?
        """, (tu_ngay, den_ngay))
    
    tong_benh_nhan = cursor.fetchone()['tong_benh_nhan']
    
    # Lấy số bệnh nhân mới (đăng ký trong khoảng thời gian)
    cursor.execute("""
        SELECT COUNT(*) as benh_nhan_moi
        FROM BENHNHAN
        WHERE NgayTao BETWEEN ? AND ?
    """, (tu_ngay, den_ngay))
    
    benh_nhan_moi = cursor.fetchone()['benh_nhan_moi']
    
    # Lấy số bệnh nhân quay lại (đã đăng ký trước khoảng thời gian nhưng có khám trong khoảng thời gian)
    cursor.execute("""
        SELECT COUNT(DISTINCT bn.MaBN) as benh_nhan_quay_lai
        FROM BENHNHAN bn
        JOIN PHIEUKHAM pk ON bn.MaBN = pk.MaBN
        WHERE pk.NgayKham BETWEEN ? AND ?
        AND bn.NgayTao < ?
    """, (tu_ngay, den_ngay, tu_ngay))
    
    benh_nhan_quay_lai = cursor.fetchone()['benh_nhan_quay_lai']
    
    # Tính tỷ lệ quay lại
    ty_le_quay_lai = 0
    if tong_benh_nhan > 0:
        ty_le_quay_lai = (benh_nhan_quay_lai / tong_benh_nhan) * 100
    
    # Lấy dữ liệu bệnh nhân theo thời gian (theo tuần)
    start_date = datetime.strptime(tu_ngay, '%Y-%m-%d')
    end_date = datetime.strptime(den_ngay, '%Y-%m-%d')
    
    benh_nhan_theo_thoi_gian = []
    thoi_gian_labels = []
    tong_so_data = []
    benh_nhan_moi_data = []
    benh_nhan_quay_lai_data = []
    
    # Chia thành các khoảng thời gian (tuần hoặc tháng tùy thuộc vào khoảng thời gian)
    delta = (end_date - start_date).days
    
    if delta <= 31:  # Nếu khoảng thời gian <= 1 tháng, chia theo ngày
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            next_date = current_date + timedelta(days=1)
            
            # Lấy tổng số bệnh nhân trong ngày
            cursor.execute("""
                SELECT COUNT(DISTINCT bn.MaBN) as tong_so
                FROM BENHNHAN bn
                LEFT JOIN PHIEUKHAM pk ON bn.MaBN = pk.MaBN
                WHERE pk.NgayKham = ?
            """, (date_str,))
            tong_so = cursor.fetchone()['tong_so']
            
            # Lấy số bệnh nhân mới trong ngày
            cursor.execute("""
                SELECT COUNT(*) as benh_nhan_moi
                FROM BENHNHAN
                WHERE NgayTao = ?
            """, (date_str,))
            bn_moi = cursor.fetchone()['benh_nhan_moi']
            
            # Lấy số bệnh nhân quay lại trong ngày
            cursor.execute("""
                SELECT COUNT(DISTINCT bn.MaBN) as benh_nhan_quay_lai
                FROM BENHNHAN bn
                JOIN PHIEUKHAM pk ON bn.MaBN = pk.MaBN
                WHERE pk.NgayKham = ?
                AND bn.NgayTao < ?
            """, (date_str, date_str))
            bn_quay_lai = cursor.fetchone()['benh_nhan_quay_lai']
            
            # Tính tỷ lệ quay lại
            ty_le = 0
            if tong_so > 0:
                ty_le = (bn_quay_lai / tong_so) * 100
            
            benh_nhan_theo_thoi_gian.append({
                'ThoiGian': current_date.strftime('%d/%m/%Y'),
                'TongSo': tong_so,
                'BenhNhanMoi': bn_moi,
                'BenhNhanQuayLai': bn_quay_lai,
                'TyLeQuayLai': ty_le
            })
            
            thoi_gian_labels.append(current_date.strftime('%d/%m'))
            tong_so_data.append(tong_so)
            benh_nhan_moi_data.append(bn_moi)
            benh_nhan_quay_lai_data.append(bn_quay_lai)
            
            current_date = next_date
    else:  # Nếu khoảng thời gian > 1 tháng, chia theo tuần
        current_date = start_date
        week_num = 1
        
        while current_date <= end_date:
            week_end = min(current_date + timedelta(days=6), end_date)
            week_start_str = current_date.strftime('%Y-%m-%d')
            week_end_str = week_end.strftime('%Y-%m-%d')
            
            # Lấy tổng số bệnh nhân trong tuần
            cursor.execute("""
                SELECT COUNT(DISTINCT bn.MaBN) as tong_so
                FROM BENHNHAN bn
                LEFT JOIN PHIEUKHAM pk ON bn.MaBN = pk.MaBN
                WHERE pk.NgayKham BETWEEN ? AND ?
            """, (week_start_str, week_end_str))
            tong_so = cursor.fetchone()['tong_so']
            
            # Lấy số bệnh nhân mới trong tuần
            cursor.execute("""
                SELECT COUNT(*) as benh_nhan_moi
                FROM BENHNHAN
                WHERE NgayTao BETWEEN ? AND ?
            """, (week_start_str, week_end_str))
            bn_moi = cursor.fetchone()['benh_nhan_moi']
            
            # Lấy số bệnh nhân quay lại trong tuần
            cursor.execute("""
                SELECT COUNT(DISTINCT bn.MaBN) as benh_nhan_quay_lai
                FROM BENHNHAN bn
                JOIN PHIEUKHAM pk ON bn.MaBN = pk.MaBN
                WHERE pk.NgayKham BETWEEN ? AND ?
                AND bn.NgayTao < ?
            """, (week_start_str, week_end_str, week_start_str))
            bn_quay_lai = cursor.fetchone()['benh_nhan_quay_lai']
            
            # Tính tỷ lệ quay lại
            ty_le = 0
            if tong_so > 0:
                ty_le = (bn_quay_lai / tong_so) * 100
            
            benh_nhan_theo_thoi_gian.append({
                'ThoiGian': f"Tuần {week_num} ({current_date.strftime('%d/%m')} - {week_end.strftime('%d/%m')})",
                'TongSo': tong_so,
                'BenhNhanMoi': bn_moi,
                'BenhNhanQuayLai': bn_quay_lai,
                'TyLeQuayLai': ty_le
            })
            
            thoi_gian_labels.append(f"Tuần {week_num}")
            tong_so_data.append(tong_so)
            benh_nhan_moi_data.append(bn_moi)
            benh_nhan_quay_lai_data.append(bn_quay_lai)
            
            current_date = week_end + timedelta(days=1)
            week_num += 1
    
    # Lấy phân bố bệnh nhân theo độ tuổi
    cursor.execute("""
        SELECT 
            CASE 
                WHEN (strftime('%Y', 'now') - strftime('%Y', NgaySinh)) < 18 THEN 'Dưới 18 tuổi'
                WHEN (strftime('%Y', 'now') - strftime('%Y', NgaySinh)) BETWEEN 18 AND 30 THEN '18-30 tuổi'
                WHEN (strftime('%Y', 'now') - strftime('%Y', NgaySinh)) BETWEEN 31 AND 45 THEN '31-45 tuổi'
                WHEN (strftime('%Y', 'now') - strftime('%Y', NgaySinh)) BETWEEN 46 AND 60 THEN '46-60 tuổi'
                ELSE 'Trên 60 tuổi'
            END as NhomTuoi,
            COUNT(*) as SoLuong
        FROM BENHNHAN
        WHERE MaBN IN (
            SELECT DISTINCT bn.MaBN
            FROM BENHNHAN bn
            LEFT JOIN PHIEUKHAM pk ON bn.MaBN = pk.MaBN
            WHERE pk.NgayKham BETWEEN ? AND ?
        )
        GROUP BY NhomTuoi
        ORDER BY 
            CASE NhomTuoi
                WHEN 'Dưới 18 tuổi' THEN 1
                WHEN '18-30 tuổi' THEN 2
                WHEN '31-45 tuổi' THEN 3
                WHEN '46-60 tuổi' THEN 4
                WHEN 'Trên 60 tuổi' THEN 5
            END
    """, (tu_ngay, den_ngay))
    
    benh_nhan_theo_tuoi = []
    nhom_tuoi_labels = []
    nhom_tuoi_data = []
    
    for row in cursor.fetchall():
        ty_le = 0
        if tong_benh_nhan > 0:
            ty_le = (row['SoLuong'] / tong_benh_nhan) * 100
        
        benh_nhan_theo_tuoi.append({
            'NhomTuoi': row['NhomTuoi'],
            'SoLuong': row['SoLuong'],
            'TyLe': ty_le
        })
        
        nhom_tuoi_labels.append(row['NhomTuoi'])
        nhom_tuoi_data.append(row['SoLuong'])
    
    # Lấy phân bố bệnh nhân theo giới tính
    cursor.execute("""
        SELECT 
            CASE 
                WHEN GioiTinh = 1 THEN 'Nam'
                WHEN GioiTinh = 0 THEN 'Nữ'
                ELSE 'Khác'
            END as GioiTinh,
            COUNT(*) as SoLuong
        FROM BENHNHAN
        WHERE MaBN IN (
            SELECT DISTINCT bn.MaBN
            FROM BENHNHAN bn
            LEFT JOIN PHIEUKHAM pk ON bn.MaBN = pk.MaBN
            WHERE pk.NgayKham BETWEEN ? AND ?
        )
        GROUP BY GioiTinh
    """, (tu_ngay, den_ngay))
    
    benh_nhan_theo_gioi_tinh = []
    gioi_tinh_labels = []
    gioi_tinh_data = []
    
    for row in cursor.fetchall():
        ty_le = 0
        if tong_benh_nhan > 0:
            ty_le = (row['SoLuong'] / tong_benh_nhan) * 100
        
        benh_nhan_theo_gioi_tinh.append({
            'GioiTinh': row['GioiTinh'],
            'SoLuong': row['SoLuong'],
            'TyLe': ty_le
        })
        
        gioi_tinh_labels.append(row['GioiTinh'])
        gioi_tinh_data.append(row['SoLuong'])
    
    conn.close()
    
    return {
        'tu_ngay': tu_ngay,
        'den_ngay': den_ngay,
        'loai_bao_cao': loai_bao_cao,
        'tong_benh_nhan': tong_benh_nhan,
        'benh_nhan_moi': benh_nhan_moi,
        'benh_nhan_quay_lai': benh_nhan_quay_lai,
        'ty_le_quay_lai': ty_le_quay_lai,
        'benh_nhan_theo_thoi_gian': benh_nhan_theo_thoi_gian,
        'benh_nhan_theo_tuoi': benh_nhan_theo_tuoi,
        'benh_nhan_theo_gioi_tinh': benh_nhan_theo_gioi_tinh,
        'thoi_gian_labels': json.dumps(thoi_gian_labels),
        'tong_so_data': json.dumps(tong_so_data),
        'benh_nhan_moi_data': json.dumps(benh_nhan_moi_data),
        'benh_nhan_quay_lai_data': json.dumps(benh_nhan_quay_lai_data),
        'nhom_tuoi_labels': json.dumps(nhom_tuoi_labels),
        'nhom_tuoi_data': json.dumps(nhom_tuoi_data),
        'gioi_tinh_labels': json.dumps(gioi_tinh_labels),
        'gioi_tinh_data': json.dumps(gioi_tinh_data)
    }

def get_bao_cao_doanh_thu(tu_ngay=None, den_ngay=None, loai_bao_cao='day'):
    """Lấy dữ liệu báo cáo doanh thu"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Nếu không có ngày, lấy dữ liệu của tháng hiện tại
    if not tu_ngay or not den_ngay:
        today = datetime.now()
        first_day = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')
        last_day = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1]).strftime('%Y-%m-%d')
        tu_ngay = first_day
        den_ngay = last_day
    
    # Lấy tổng doanh thu
    cursor.execute("""
        SELECT SUM(TongTien) as tong_doanh_thu
        FROM HOADON
        WHERE NgayLap BETWEEN ? AND ?
    """, (tu_ngay, den_ngay))
    
    result = cursor.fetchone()
    tong_doanh_thu = result['tong_doanh_thu'] if result['tong_doanh_thu'] else 0
    
    # Lấy tổng số hóa đơn
    cursor.execute("""
        SELECT COUNT(*) as tong_hoa_don
        FROM HOADON
        WHERE NgayLap BETWEEN ? AND ?
    """, (tu_ngay, den_ngay))
    
    tong_hoa_don = cursor.fetchone()['tong_hoa_don']
    
    # Tính doanh thu trung bình
    doanh_thu_trung_binh = 0
    if tong_hoa_don > 0:
        doanh_thu_trung_binh = tong_doanh_thu / tong_hoa_don
    
    # Lấy doanh thu cao nhất
    cursor.execute("""
        SELECT MAX(TongTien) as doanh_thu_cao_nhat
        FROM HOADON
        WHERE NgayLap BETWEEN ? AND ?
    """, (tu_ngay, den_ngay))
    
    result = cursor.fetchone()
    doanh_thu_cao_nhat = result['doanh_thu_cao_nhat'] if result['doanh_thu_cao_nhat'] else 0
    
    # Lấy doanh thu theo thời gian
    doanh_thu_theo_thoi_gian = []
    thoi_gian_labels = []
    doanh_thu_data = []
    
    # Format thời gian theo loại báo cáo
    if loai_bao_cao == 'day':
        # Báo cáo theo ngày
        start_date = datetime.strptime(tu_ngay, '%Y-%m-%d')
        end_date = datetime.strptime(den_ngay, '%Y-%m-%d')
        
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            
            cursor.execute("""
                SELECT COUNT(*) as so_luong, SUM(TongTien) as doanh_thu
                FROM HOADON
                WHERE date(NgayLap) = ?
            """, (date_str,))
            
            row = cursor.fetchone()
            so_luong = row['so_luong'] if row['so_luong'] else 0
            doanh_thu = row['doanh_thu'] if row['doanh_thu'] else 0
            
            ty_le = 0
            if tong_doanh_thu > 0:
                ty_le = (doanh_thu / tong_doanh_thu) * 100
            
            doanh_thu_theo_thoi_gian.append({
                'ThoiGian': current_date.strftime('%d/%m/%Y'),
                'SoLuongHoaDon': so_luong,
                'DoanhThu': doanh_thu,
                'TyLe': ty_le
            })
            
            thoi_gian_labels.append(current_date.strftime('%d/%m'))
            doanh_thu_data.append(doanh_thu)
            
            current_date += timedelta(days=1)
    
    elif loai_bao_cao == 'month':
        # Báo cáo theo tháng
        start_date = datetime.strptime(tu_ngay, '%Y-%m-%d')
        end_date = datetime.strptime(den_ngay, '%Y-%m-%d')
        
        # Lấy tháng đầu tiên và cuối cùng
        start_month = start_date.replace(day=1)
        end_month = end_date.replace(day=1)
        
        current_month = start_month
        while current_month <= end_month:
            month_start = current_month.strftime('%Y-%m-%d')
            last_day = calendar.monthrange(current_month.year, current_month.month)[1]
            month_end = current_month.replace(day=last_day).strftime('%Y-%m-%d')
            
            cursor.execute("""
                SELECT COUNT(*) as so_luong, SUM(TongTien) as doanh_thu
                FROM HOADON
                WHERE date(NgayLap) BETWEEN ? AND ?
            """, (month_start, month_end))
            
            row = cursor.fetchone()
            so_luong = row['so_luong'] if row['so_luong'] else 0
            doanh_thu = row['doanh_thu'] if row['doanh_thu'] else 0
            
            ty_le = 0
            if tong_doanh_thu > 0:
                ty_le = (doanh_thu / tong_doanh_thu) * 100
            
            doanh_thu_theo_thoi_gian.append({
                'ThoiGian': f"Tháng {current_month.month}/{current_month.year}",
                'SoLuongHoaDon': so_luong,
                'DoanhThu': doanh_thu,
                'TyLe': ty_le
            })
            
            thoi_gian_labels.append(f"T{current_month.month}/{current_month.year}")
            doanh_thu_data.append(doanh_thu)
            
            # Chuyển sang tháng tiếp theo
            if current_month.month == 12:
                current_month = current_month.replace(year=current_month.year + 1, month=1)
            else:
                current_month = current_month.replace(month=current_month.month + 1)
    
    elif loai_bao_cao == 'quarter':
        # Báo cáo theo quý
        start_date = datetime.strptime(tu_ngay, '%Y-%m-%d')
        end_date = datetime.strptime(den_ngay, '%Y-%m-%d')
        
        # Lấy quý đầu tiên và cuối cùng
        start_quarter = (start_date.month - 1) // 3 + 1
        start_year = start_date.year
        
        end_quarter = (end_date.month - 1) // 3 + 1
        end_year = end_date.year
        
        current_year = start_year
        current_quarter = start_quarter
        
        while current_year < end_year or (current_year == end_year and current_quarter <= end_quarter):
            quarter_start_month = (current_quarter - 1) * 3 + 1
            quarter_end_month = quarter_start_month + 2
            
            quarter_start = datetime(current_year, quarter_start_month, 1).strftime('%Y-%m-%d')
            quarter_end = datetime(current_year, quarter_end_month, calendar.monthrange(current_year, quarter_end_month)[1]).strftime('%Y-%m-%d')
            
            cursor.execute("""
                SELECT COUNT(*) as so_luong, SUM(TongTien) as doanh_thu
                FROM HOADON
                WHERE date(NgayLap) BETWEEN ? AND ?
            """, (quarter_start, quarter_end))
            
            row = cursor.fetchone()
            so_luong = row['so_luong'] if row['so_luong'] else 0
            doanh_thu = row['doanh_thu'] if row['doanh_thu'] else 0
            
            ty_le = 0
            if tong_doanh_thu > 0:
                ty_le = (doanh_thu / tong_doanh_thu) * 100
            
            doanh_thu_theo_thoi_gian.append({
                'ThoiGian': f"Quý {current_quarter}/{current_year}",
                'SoLuongHoaDon': so_luong,
                'DoanhThu': doanh_thu,
                'TyLe': ty_le
            })
            
            thoi_gian_labels.append(f"Q{current_quarter}/{current_year}")
            doanh_thu_data.append(doanh_thu)
            
            # Chuyển sang quý tiếp theo
            current_quarter += 1
            if current_quarter > 4:
                current_quarter = 1
                current_year += 1
    
    elif loai_bao_cao == 'year':
        # Báo cáo theo năm
        start_date = datetime.strptime(tu_ngay, '%Y-%m-%d')
        end_date = datetime.strptime(den_ngay, '%Y-%m-%d')
        
        start_year = start_date.year
        end_year = end_date.year
        
        for year in range(start_year, end_year + 1):
            year_start = datetime(year, 1, 1).strftime('%Y-%m-%d')
            year_end = datetime(year, 12, 31).strftime('%Y-%m-%d')
            
            cursor.execute("""
                SELECT COUNT(*) as so_luong, SUM(TongTien) as doanh_thu
                FROM HOADON
                WHERE date(NgayLap) BETWEEN ? AND ?
            """, (year_start, year_end))
            
            row = cursor.fetchone()
            so_luong = row['so_luong'] if row['so_luong'] else 0
            doanh_thu = row['doanh_thu'] if row['doanh_thu'] else 0
            
            ty_le = 0
            if tong_doanh_thu > 0:
                ty_le = (doanh_thu / tong_doanh_thu) * 100
            
            doanh_thu_theo_thoi_gian.append({
                'ThoiGian': f"Năm {year}",
                'SoLuongHoaDon': so_luong,
                'DoanhThu': doanh_thu,
                'TyLe': ty_le
            })
            
            thoi_gian_labels.append(str(year))
            doanh_thu_data.append(doanh_thu)
    
    # Lấy doanh thu theo phương thức thanh toán
    cursor.execute("""
        SELECT PhuongThucThanhToan, COUNT(*) as so_luong, SUM(TongTien) as doanh_thu
        FROM HOADON
        WHERE NgayLap BETWEEN ? AND ?
        GROUP BY PhuongThucThanhToan
    """, (tu_ngay, den_ngay))
    
    doanh_thu_theo_pttt = []
    pttt_labels = []
    pttt_data = []
    
    for row in cursor.fetchall():
        doanh_thu = row['doanh_thu'] if row['doanh_thu'] else 0
        
        ty_le = 0
        if tong_doanh_thu > 0:
            ty_le = (doanh_thu / tong_doanh_thu) * 100
        
        doanh_thu_theo_pttt.append({
            'PhuongThucThanhToan': row['PhuongThucThanhToan'],
            'SoLuongHoaDon': row['so_luong'],
            'DoanhThu': doanh_thu,
            'TyLe': ty_le
        })
        
        pttt_labels.append(row['PhuongThucThanhToan'])
        pttt_data.append(doanh_thu)
    
    # Lấy doanh thu theo dịch vụ
    cursor.execute("""
        SELECT dv.MaDV, dv.TenDV, COUNT(pk.MaDV) as so_luong, SUM(hd.TongTien) as doanh_thu
        FROM DICHVU dv
        JOIN PHIEUKHAM pk ON dv.MaDV = pk.MaDV
        JOIN HOADON hd ON pk.MaPK = hd.MaPK
        WHERE hd.NgayLap BETWEEN ? AND ?
        GROUP BY dv.MaDV
        ORDER BY doanh_thu DESC
    """, (tu_ngay, den_ngay))
    
    doanh_thu_theo_dich_vu = []
    tong_so_luong_dich_vu = 0
    
    for row in cursor.fetchall():
        so_luong = row['so_luong'] if row['so_luong'] else 0
        doanh_thu = row['doanh_thu'] if row['doanh_thu'] else 0
        
        tong_so_luong_dich_vu += so_luong
        
        ty_le = 0
        if tong_doanh_thu > 0:
            ty_le = (doanh_thu / tong_doanh_thu) * 100
        
        doanh_thu_theo_dich_vu.append({
            'MaDV': row['MaDV'],
            'TenDV': row['TenDV'],
            'SoLuong': so_luong,
            'DoanhThu': doanh_thu,
            'TyLe': ty_le
        })
    
    conn.close()
    
    return {
        'tu_ngay': tu_ngay,
        'den_ngay': den_ngay,
        'loai_bao_cao': loai_bao_cao,
        'tong_doanh_thu': tong_doanh_thu,
        'tong_hoa_don': tong_hoa_don,
        'doanh_thu_trung_binh': doanh_thu_trung_binh,
        'doanh_thu_cao_nhat': doanh_thu_cao_nhat,
        'doanh_thu_theo_thoi_gian': doanh_thu_theo_thoi_gian,
        'doanh_thu_theo_pttt': doanh_thu_theo_pttt,
        'doanh_thu_theo_dich_vu': doanh_thu_theo_dich_vu,
        'tong_so_luong_dich_vu': tong_so_luong_dich_vu,
        'thoi_gian_labels': json.dumps(thoi_gian_labels),
        'doanh_thu_data': json.dumps(doanh_thu_data),
        'pttt_labels': json.dumps(pttt_labels),
        'pttt_data': json.dumps(pttt_data)
    }

def get_bao_cao_luot_kham(tu_ngay=None, den_ngay=None, loai_bao_cao='day'):
    """Lấy dữ liệu báo cáo số lượt khám từ bảng PHIEUKHAM theo ngày, tháng hoặc khoảng thời gian"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Nếu không có ngày, lấy dữ liệu của tháng hiện tại
    if not tu_ngay or not den_ngay:
        today = datetime.now()
        first_day = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')
        last_day = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1]).strftime('%Y-%m-%d')
        tu_ngay = first_day
        den_ngay = last_day
    
    # Lấy tổng số lượt khám
    cursor.execute("""
        SELECT COUNT(*) as tong_luot_kham
        FROM PHIEUKHAM
        WHERE date(NgayKham) BETWEEN ? AND ?
    """, (tu_ngay, den_ngay))
    
    tong_luot_kham = cursor.fetchone()['tong_luot_kham']
    
    # Lấy số lượt khám trung bình mỗi ngày
    start_date = datetime.strptime(tu_ngay, '%Y-%m-%d')
    end_date = datetime.strptime(den_ngay, '%Y-%m-%d')
    so_ngay = (end_date - start_date).days + 1
    
    luot_kham_trung_binh = 0
    if so_ngay > 0:
        luot_kham_trung_binh = tong_luot_kham / so_ngay
    
    # Lấy ngày có nhiều lượt khám nhất
    cursor.execute("""
        SELECT date(NgayKham) as ngay, COUNT(*) as so_luot
        FROM PHIEUKHAM
        WHERE date(NgayKham) BETWEEN ? AND ?
        GROUP BY date(NgayKham)
        ORDER BY so_luot DESC
        LIMIT 1
    """, (tu_ngay, den_ngay))
    
    result = cursor.fetchone()
    ngay_nhieu_nhat = result['ngay'] if result else None
    so_luot_nhieu_nhat = result['so_luot'] if result else 0
    
    # Định dạng lại ngày nhiều nhất để hiển thị
    if ngay_nhieu_nhat:
        try:
            ngay_obj = datetime.strptime(ngay_nhieu_nhat, '%Y-%m-%d')
            ngay_nhieu_nhat = ngay_obj.strftime('%d/%m/%Y')
        except:
            pass
    
    # Lấy dữ liệu lượt khám theo thời gian
    luot_kham_theo_thoi_gian = []
    thoi_gian_labels = []
    luot_kham_data = []
    
    # Chia thành các khoảng thời gian tùy thuộc vào loại báo cáo
    if loai_bao_cao == 'day':  # Theo ngày
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Lấy số lượt khám trong ngày
            cursor.execute("""
                SELECT COUNT(*) as so_luot
                FROM PHIEUKHAM
                WHERE date(NgayKham) = ?
            """, (date_str,))
            
            so_luot = cursor.fetchone()['so_luot']
            
            luot_kham_theo_thoi_gian.append({
                'ThoiGian': current_date.strftime('%d/%m/%Y'),
                'SoLuot': so_luot
            })
            
            thoi_gian_labels.append(current_date.strftime('%d/%m'))
            luot_kham_data.append(so_luot)
            
            current_date += timedelta(days=1)
            
    elif loai_bao_cao == 'week':  # Theo tuần
        current_date = start_date
        week_num = 1
        
        while current_date <= end_date:
            week_end = min(current_date + timedelta(days=6), end_date)
            week_start_str = current_date.strftime('%Y-%m-%d')
            week_end_str = week_end.strftime('%Y-%m-%d')
            
            # Lấy số lượt khám trong tuần
            cursor.execute("""
                SELECT COUNT(*) as so_luot
                FROM PHIEUKHAM
                WHERE date(NgayKham) BETWEEN ? AND ?
            """, (week_start_str, week_end_str))
            
            so_luot = cursor.fetchone()['so_luot']
            
            luot_kham_theo_thoi_gian.append({
                'ThoiGian': f"Tuần {week_num} ({current_date.strftime('%d/%m')} - {week_end.strftime('%d/%m')})",
                'SoLuot': so_luot
            })
            
            thoi_gian_labels.append(f"Tuần {week_num}")
            luot_kham_data.append(so_luot)
            
            current_date = week_end + timedelta(days=1)
            week_num += 1
            
    elif loai_bao_cao == 'month':  # Theo tháng
        # Lấy tháng đầu tiên và tháng cuối cùng
        start_year = start_date.year
        start_month = start_date.month
        end_year = end_date.year
        end_month = end_date.month
        
        current_year = start_year
        current_month = start_month
        month_num = 1
        
        while (current_year < end_year) or (current_year == end_year and current_month <= end_month):
            # Tính ngày đầu và cuối của tháng
            first_day_of_month = datetime(current_year, current_month, 1)
            last_day_of_month = datetime(current_year, current_month, calendar.monthrange(current_year, current_month)[1])
            
            # Điều chỉnh nếu tháng đầu hoặc cuối nằm trong khoảng thời gian
            if first_day_of_month < start_date:
                first_day_of_month = start_date
            if last_day_of_month > end_date:
                last_day_of_month = end_date
                
            month_start_str = first_day_of_month.strftime('%Y-%m-%d')
            month_end_str = last_day_of_month.strftime('%Y-%m-%d')
            
            # Lấy số lượt khám trong tháng
            cursor.execute("""
                SELECT COUNT(*) as so_luot
                FROM PHIEUKHAM
                WHERE date(NgayKham) BETWEEN ? AND ?
            """, (month_start_str, month_end_str))
            
            so_luot = cursor.fetchone()['so_luot']
            
            luot_kham_theo_thoi_gian.append({
                'ThoiGian': f"Tháng {current_month}/{current_year}",
                'SoLuot': so_luot
            })
            
            thoi_gian_labels.append(f"T{current_month}/{current_year}")
            luot_kham_data.append(so_luot)
            
            # Tăng tháng
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
            
            month_num += 1
    
    # Lấy số lượt khám theo bác sĩ
    cursor.execute("""
        SELECT bs.MaBS, bs.HoTen, COUNT(pk.MaBS) as so_luot
        FROM BACSI bs
        LEFT JOIN PHIEUKHAM pk ON bs.MaBS = pk.MaBS
        WHERE date(pk.NgayKham) BETWEEN ? AND ?
        GROUP BY bs.MaBS
        ORDER BY so_luot DESC
    """, (tu_ngay, den_ngay))
    
    luot_kham_theo_bac_si = []
    bac_si_labels = []
    bac_si_data = []
    
    for row in cursor.fetchall():
        luot_kham_theo_bac_si.append({
            'MaBS': row['MaBS'],
            'HoTen': row['HoTen'],
            'SoLuot': row['so_luot']
        })
        
        bac_si_labels.append(row['HoTen'])
        bac_si_data.append(row['so_luot'])
    
    # Lấy số lượt khám theo dịch vụ
    cursor.execute("""
        SELECT dv.MaDV, dv.TenDV, COUNT(pk.MaDV) as so_luot
        FROM DICHVU dv
        LEFT JOIN PHIEUKHAM pk ON dv.MaDV = pk.MaDV
        WHERE date(pk.NgayKham) BETWEEN ? AND ?
        GROUP BY dv.MaDV
        ORDER BY so_luot DESC
    """, (tu_ngay, den_ngay))
    
    luot_kham_theo_dich_vu = []
    dich_vu_labels = []
    dich_vu_data = []
    
    for row in cursor.fetchall():
        luot_kham_theo_dich_vu.append({
            'MaDV': row['MaDV'],
            'TenDV': row['TenDV'],
            'SoLuot': row['so_luot']
        })
        
        dich_vu_labels.append(row['TenDV'])
        dich_vu_data.append(row['so_luot'])
    
    conn.close()
    
    return {
        'tu_ngay': tu_ngay,
        'den_ngay': den_ngay,
        'loai_bao_cao': loai_bao_cao,
        'tong_luot_kham': tong_luot_kham,
        'luot_kham_trung_binh': luot_kham_trung_binh,
        'ngay_nhieu_nhat': ngay_nhieu_nhat,
        'so_luot_nhieu_nhat': so_luot_nhieu_nhat,
        'luot_kham_theo_thoi_gian': luot_kham_theo_thoi_gian,
        'luot_kham_theo_bac_si': luot_kham_theo_bac_si,
        'luot_kham_theo_dich_vu': luot_kham_theo_dich_vu,
        'thoi_gian_labels': json.dumps(thoi_gian_labels),
        'luot_kham_data': json.dumps(luot_kham_data),
        'bac_si_labels': json.dumps(bac_si_labels),
        'bac_si_data': json.dumps(bac_si_data),
        'dich_vu_labels': json.dumps(dich_vu_labels),
        'dich_vu_data': json.dumps(dich_vu_data)
    }

def get_bao_cao_luong_dich_vu(tu_ngay=None, den_ngay=None):
    """Lấy dữ liệu báo cáo lượng dịch vụ từ bảng PHIEUKHAM"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Nếu không có ngày, lấy dữ liệu của tháng hiện tại
    if not tu_ngay or not den_ngay:
        today = datetime.now()
        first_day = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')
        last_day = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1]).strftime('%Y-%m-%d')
        tu_ngay = first_day
        den_ngay = last_day
    
    # Lấy danh sách dịch vụ và số lượng sử dụng từ bảng PHIEUKHAM
    cursor.execute("""
        SELECT dv.MaDV, dv.TenDV, COUNT(pk.MaDV) as SoLuong
        FROM DICHVU dv
        LEFT JOIN PHIEUKHAM pk ON dv.MaDV = pk.MaDV
        WHERE pk.NgayKham BETWEEN ? AND ?
        GROUP BY dv.MaDV
        ORDER BY SoLuong DESC
    """, (tu_ngay, den_ngay))
    
    dich_vu_list = []
    tong_so_luong = 0
    
    for row in cursor.fetchall():
        so_luong = row['SoLuong'] if row['SoLuong'] else 0
        tong_so_luong += so_luong
        
        dich_vu_list.append({
            'MaDV': row['MaDV'],
            'TenDV': row['TenDV'],
            'SoLuong': so_luong,
            'TyLe': 0  # Sẽ tính sau khi có tổng
        })
    
    # Tính tỷ lệ cho từng dịch vụ dựa trên số lượng
    for dv in dich_vu_list:
        if tong_so_luong > 0:
            dv['TyLe'] = (dv['SoLuong'] / tong_so_luong) * 100
        else:
            dv['TyLe'] = 0
    
    # Lấy dịch vụ phổ biến nhất
    dich_vu_pho_bien = dich_vu_list[0]['TenDV'] if dich_vu_list else "Không có dữ liệu"
    
    # Chuẩn bị dữ liệu cho biểu đồ
    dich_vu_labels = [dv['TenDV'] for dv in dich_vu_list]
    dich_vu_data = [dv['SoLuong'] for dv in dich_vu_list]
    
    conn.close()
    
    return {
        'tu_ngay': tu_ngay,
        'den_ngay': den_ngay,
        'dich_vu_list': dich_vu_list,
        'tong_dich_vu': len(dich_vu_list),
        'tong_so_luong': tong_so_luong,
        'dich_vu_pho_bien': dich_vu_pho_bien,
        'dich_vu_labels': json.dumps(dich_vu_labels),
        'dich_vu_data': json.dumps(dich_vu_data)
    }