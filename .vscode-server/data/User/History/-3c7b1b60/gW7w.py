import mysql.connector
from datetime import datetime



"""
Kết nối với MySQL
"""
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="huong24052005",
        database="QuanLyGiaSu"
    )



"""
Xử lý logic cho database phụ hunh
"""
# Tạo mã phụ huynh tự động
def get_next_phuhuynh_id():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MaPH FROM PHUHUYNH ORDER BY MaPH DESC LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            last_id = int(result[0][2:])  # Remove 'PH' and convert to int
            new_id = f"PH{last_id + 1:06d}"
        else:
            new_id = "PH000001"
        
        return new_id
    except Exception as e:
        print("Lỗi khi tạo mã phụ huynh:", e)
        return "PH000001"
    finally:
        cursor.close()
        conn.close()

# Thêm phụ huynh
def insert_parent(ma_phu_huynh, ho_ten, dia_chi, so_dien_thoai, yeu_cau):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Nếu không có mã phụ huynh hoặc mã rỗng, tạo mã tự động
        if not ma_phu_huynh or ma_phu_huynh.strip() == "":
            ma_phu_huynh = get_next_phuhuynh_id()
            
        query = """
            INSERT INTO PHUHUYNH (MaPH, HoTen, SoDT, DiaChi, YeuCau)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (ma_phu_huynh, ho_ten, so_dien_thoai, dia_chi, yeu_cau))
        conn.commit()
        print("Dữ liệu insert:", (ma_phu_huynh, ho_ten, dia_chi, so_dien_thoai, yeu_cau))
        return True
    except Exception as e:
        print("Lỗi:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# Tìm kiếm phụ huynh theo MaPH hoặc HoTen
def search_parent(keyword):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Using dictionary to get results as key-value pairs
    try:
        query = """
            SELECT * FROM PHUHUYNH
            WHERE MaPH LIKE %s OR HoTen LIKE %s
        """
        like_keyword = f"%{keyword}%"
        cursor.execute(query, (like_keyword, like_keyword))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print("Lỗi:", e)
        return []
    finally:
        cursor.close()
        conn.close()

# Cập nhật thông tin phụ huynh
def update_parent(ma_phu_huynh, ho_ten, dia_chi, so_dien_thoai, yeu_cau):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE PHUHUYNH
            SET HoTen = %s, SoDT = %s, DiaChi = %s, YeuCau = %s
            WHERE MaPH = %s
        """
        cursor.execute(query, (ho_ten, so_dien_thoai, dia_chi, yeu_cau, ma_phu_huynh))
        conn.commit()
        return True
    except Exception as e:
        print("Lỗi:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# Xem danh sách phụ huynh
def get_parent_list():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM PHUHUYNH"
    cursor.execute(query)
    parents = cursor.fetchall()
    conn.close()
    return parents

# Xóa phụ huynh
def delete_parent(maph):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM PHUHUYNH WHERE MaPH = %s", (maph,))
    conn.commit()
    conn.close()


"""
Xử lý logic cho database gia sư
"""
# Thêm gia sư
def get_next_giasu_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MaGS FROM GIASU ORDER BY MaGS DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        last_id = int(result[0][2:])  # Remove 'GS' and convert to int
        new_id = f"GS{last_id + 1:06d}"
    else:
        new_id = "GS000001"
    
    return new_id

def insert_giasu(ma_gs, ho_ten, sdt, bang_cap, mon_day, kinh_nghiem):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO GIASU (MaGS, HoTen, SoDT, BangCap, MonDay, KinhNghiem)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (ma_gs, ho_ten, sdt, bang_cap, mon_day, kinh_nghiem)
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()


# Tìm gia sư
def search_tutors(search_term):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT * FROM GIASU
        WHERE MaGS LIKE %s OR HoTen LIKE %s
    """
    pattern = f"%{search_term}%"
    cursor.execute(query, (pattern, pattern))
    results = cursor.fetchall()

    connection.close()
    return results

# Cập nhật thông tin gia sư
def update_tutor(ma_gia_su, ho_ten, so_dien_thoai, bang_cap, mon_day ,king_nghiem):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE GIASU
            SET HoTen = %s, SoDT = %s, BangCap = %s, MonDay = %s, KinhNghiem = %s
            WHERE MaGS = %s
        """
        cursor.execute(query, (ho_ten, so_dien_thoai, bang_cap, mon_day ,king_nghiem, ma_gia_su))
        conn.commit()
        return True
    except Exception as e:
        print("Lỗi:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# Xem danh sách gia sư
def get_tutor_list():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM GIASU"
    cursor.execute(query)
    tutor = cursor.fetchall()
    conn.close()
    return tutor

# Xóa gia sư
def delete_tutor(maph):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM GIASU WHERE MaGS = %s", (maph,))
    conn.commit()
    conn.close()



"""
Xử lý logic cho database giao dịch
"""
# Tạo mã giao dịch tự động
def get_next_giaodich_id():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MaGD FROM GIAODICH ORDER BY MaGD DESC LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            last_id = int(result[0][2:])  # Remove 'GD' and convert to int
            new_id = f"GD{last_id + 1:06d}"
        else:
            new_id = "GD000001"
        
        return new_id
    except Exception as e:
        print("Lỗi khi tạo mã giao dịch:", e)
        return "GD000001"
    finally:
        cursor.close()
        conn.close()

# Thêm giao dịch
def insert_giao_dich(maGD, ngayGD, phiGS, phiPH, maPH, maGS):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Nếu không có mã giao dịch hoặc mã rỗng, tạo mã tự động
        if not maGD or maGD.strip() == "":
            maGD = get_next_giaodich_id()
            
        sql = """
            INSERT INTO GIAODICH (MaGD, NgayGD, PhiGS, PhiPH, MaPH, MaGS)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        # Convert ngayGD to datetime
        formatted_date = datetime.strptime(ngayGD, "%Y-%m-%d")
        cursor.execute(sql, (maGD, formatted_date, phiGS, phiPH, maPH, maGS))
        connection.commit()
        return maGD  # Trả về mã giao dịch đã tạo
    except mysql.connector.Error as e:
        print("Lỗi khi chèn dữ liệu:", e)
        raise
    finally:
        cursor.close()
        connection.close()


# Tìm giao dịch
def get_all_transactions():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM GIAODICH")
    result = cursor.fetchall()
    conn.close()
    return result

def search_transactions(keyword):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT * FROM GIAODICH
        WHERE MaGD LIKE %s OR MaPH LIKE %s
    """
    like_pattern = f"%{keyword}%"
    cursor.execute(query, (like_pattern, like_pattern))
    result = cursor.fetchall()
    conn.close()
    return result

# Sửa giao dịch
def update_transaction(MaGD, NgayGD, MaGS, MaPH, PhiPH, PhiGS):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE GIAODICH
            SET NgayGD = %s, MaGS = %s, MaPH = %s, PhiPH = %s, PhiGS = %s
            WHERE MaGD = %s
        """
        cursor.execute(sql, (NgayGD, MaGS, MaPH, PhiPH, PhiGS, MaGD))
        conn.commit()
        return True
    except Exception as e:
        print("Lỗi khi cập nhật giao dịch:", e)
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



def get_transaction_by_id(MaGD):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM GIAODICH WHERE MaGD = %s", (MaGD,))
        return cursor.fetchone()
    except Exception as e:
        print("Lỗi khi lấy giao dịch:", e)
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Xem giao dịch
def get_all_giao_dich():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM GIAODICH")
    result = cursor.fetchall()
    conn.close()
    
    formatted_result = []
    for row in result:
        MaGD, NgayGD, PhiGS, PhiPH, MaPH, MaGS = row
        formatted_result.append((
            MaGD,
            MaGS,
            MaPH,
            NgayGD,
            int(PhiGS),
            int(PhiPH)
        ))
    return formatted_result

# Xóa giao dịch
def get_transactions():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM GIAODICH")
    transactions = cursor.fetchall()
    cursor.close()
    connection.close()
    return transactions

def delete_transaction(transaction_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM GIAODICH WHERE MaGD = %s", (transaction_id,))
    connection.commit()
    cursor.close()
    connection.close()



"""
Xử lý logic lớp học
"""
# Tạo mã lớp học tự động
def get_next_lophoc_id():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MaLop FROM LOPHOC ORDER BY MaLop DESC LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            last_id = int(result[0][2:])  # Remove 'LH' and convert to int
            new_id = f"LH{last_id + 1:06d}"
        else:
            new_id = "LH000001"
        
        return new_id
    except Exception as e:
        print("Lỗi khi tạo mã lớp học:", e)
        return "LH000001"
    finally:
        cursor.close()
        conn.close()

# Thêm lớp học
def save_class_data(class_data):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Nếu không có mã lớp học hoặc mã rỗng, tạo mã tự động
        if "classId" not in class_data or not class_data["classId"] or class_data["classId"].strip() == "":
            class_data["classId"] = get_next_lophoc_id()
            
        # Query to insert new class data
        query = """
        INSERT INTO LOPHOC (MaLop, MonHoc, CapHoc, LichHoc, DiaDiem, MaGD)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (class_data["classId"], class_data["subject"], class_data["grade"], 
                  class_data["schedule"], class_data["location"], class_data["transactionId"])

        cursor.execute(query, values)
        connection.commit()

        return True  # Success

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False  # Failure

    finally:
        cursor.close()
        connection.close()



# Cập nhật lớp học
# Lấy thông tin lớp học theo MaLop
def get_class_info(class_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM LOPHOC WHERE MaLop = %s", (class_id,))
    class_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return class_info

# Cập nhật thông tin lớp học
def update_class_info(class_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE LOPHOC
        SET MonHoc = %s, CapHoc = %s, LichHoc = %s, DiaDiem = %s
        WHERE MaLop = %s
    """, (
        class_data['subject'],
        class_data['grade'],
        class_data['schedule'],
        class_data['location'],
        class_data['id']
    ))
    conn.commit()
    cursor.close()
    conn.close()