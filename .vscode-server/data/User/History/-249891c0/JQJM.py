import mysql.connector

def add_ph(maph, hoten, sodt, diachi,yeucau):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='huong24052005',
        database='QuanLyGiaSu'
    )
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True for easier Jinja use
    cursor.execute("SELECT * FROM GIASU")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    try:
            query = """
                INSERT INTO phu_huynh (ma_phu_huynh, ho_ten, dia_chi, so_dien_thoai, yeu_cau)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (parent_id, full_name, address, phone, requirements))
            db.commit()
            flash("Đã thêm phụ huynh thành công!", "success")
            return redirect(url_for("them_ph"))
        except Exception as e:
            db.rollback()
            flash(f"Lỗi khi thêm phụ huynh: {str(e)}", "danger")