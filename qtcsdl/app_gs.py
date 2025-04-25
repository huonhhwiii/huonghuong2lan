# Thêm các hàm xử lý gia sư vào app.py

# Thêm gia sư mới
@app.route("/them_gs", methods=["GET", "POST"])
@login_required
def them_gs():
    if request.method == "POST":
        try:
            # Lấy dữ liệu từ form
            ho_ten = request.form.get('hoTen')
            so_dt = request.form.get('soDT')
            bang_cap = request.form.get('bangCap')
            mon_day = request.form.get('monDay')
            kinh_nghiem = request.form.get('kinhNghiem')
            
            # Kiểm tra dữ liệu
            if not ho_ten or not so_dt:
                flash("Vui lòng điền đầy đủ thông tin bắt buộc!", "danger")
                return render_template("them_gs_new.html")
            
            # Kiểm tra định dạng số điện thoại
            import re
            if not re.match(r'^0[0-9]{9}$', so_dt):
                flash("Số điện thoại không hợp lệ! Vui lòng nhập 10 chữ số bắt đầu bằng số 0.", "danger")
                return render_template("them_gs_new.html")
            
            # Kết nối database
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Kiểm tra số điện thoại đã tồn tại chưa
            cursor.execute("SELECT * FROM GIASU WHERE SoDT = %s", (so_dt,))
            if cursor.fetchone():
                flash("Số điện thoại đã tồn tại trong hệ thống!", "danger")
                return render_template("them_gs_new.html")
            
            # Tạo mã gia sư mới
            cursor.execute("SELECT MAX(CAST(SUBSTRING(MaGS, 3) AS UNSIGNED)) FROM GIASU")
            result = cursor.fetchone()
            max_id = result[list(result.keys())[0]] or 0
            ma_gs = f"GS{max_id + 1:05d}"
            
            # Thêm gia sư mới vào database
            query = """
                INSERT INTO GIASU (MaGS, HoTen, SoDT, BangCap, MonDay, KinhNghiem)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (ma_gs, ho_ten, so_dt, bang_cap, mon_day, kinh_nghiem))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            flash(f"Đã thêm gia sư {ho_ten} thành công!", "success")
            return redirect(url_for('qlgs'))
            
        except Exception as e:
            flash(f"Lỗi khi thêm gia sư: {str(e)}", "danger")
            return render_template("them_gs_new.html")
    
    return render_template("them_gs_new.html")


# Xem chi tiết gia sư
@app.route("/xem_gs/<ma_gs>")
@login_required
def xem_gs(ma_gs):
    try:
        # Kết nối database
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Lấy thông tin gia sư
        cursor.execute("SELECT * FROM GIASU WHERE MaGS = %s", (ma_gs,))
        gs = cursor.fetchone()
        
        if not gs:
            flash("Không tìm thấy gia sư!", "danger")
            return redirect(url_for('qlgs'))
        
        # Lấy danh sách lớp học của gia sư (thông qua giao dịch)
        query_lh = """
            SELECT lh.* 
            FROM LOPHOC lh
            JOIN GIAODICH gd ON lh.MaGD = gd.MaGD
            WHERE gd.MaGS = %s
        """
        cursor.execute(query_lh, (ma_gs,))
        ds_lh = cursor.fetchall()
        
        # Lấy lịch sử giao dịch của gia sư
        query_gd = """
            SELECT gd.*, ph.HoTen AS TenPH
            FROM GIAODICH gd
            JOIN PHUHUYNH ph ON gd.MaPH = ph.MaPH
            WHERE gd.MaGS = %s
        """
        cursor.execute(query_gd, (ma_gs,))
        ds_gd = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template("xem_gs_new.html", gs=gs, ds_lh=ds_lh, ds_gd=ds_gd)
        
    except Exception as e:
        flash(f"Lỗi khi xem thông tin gia sư: {str(e)}", "danger")
        return redirect(url_for('qlgs'))


# Sửa thông tin gia sư
@app.route("/sua_gs/<ma_gs>", methods=["GET", "POST"])
@login_required
def sua_gs(ma_gs):
    try:
        # Kết nối database
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Lấy thông tin gia sư
        cursor.execute("SELECT * FROM GIASU WHERE MaGS = %s", (ma_gs,))
        gs = cursor.fetchone()
        
        if not gs:
            flash("Không tìm thấy gia sư!", "danger")
            return redirect(url_for('qlgs'))
        
        if request.method == "POST":
            # Lấy dữ liệu từ form
            ho_ten = request.form.get('hoTen')
            so_dt = request.form.get('soDT')
            bang_cap = request.form.get('bangCap')
            mon_day = request.form.get('monDay')
            kinh_nghiem = request.form.get('kinhNghiem')
            
            # Kiểm tra dữ liệu
            if not ho_ten or not so_dt:
                flash("Vui lòng điền đầy đủ thông tin bắt buộc!", "danger")
                return render_template("sua_gs_new.html", gs=gs)
            
            # Kiểm tra định dạng số điện thoại
            import re
            if not re.match(r'^0[0-9]{9}$', so_dt):
                flash("Số điện thoại không hợp lệ! Vui lòng nhập 10 chữ số bắt đầu bằng số 0.", "danger")
                return render_template("sua_gs_new.html", gs=gs)
            
            # Kiểm tra số điện thoại đã tồn tại chưa (nếu thay đổi)
            if so_dt != gs['SoDT']:
                cursor.execute("SELECT * FROM GIASU WHERE SoDT = %s AND MaGS != %s", (so_dt, ma_gs))
                if cursor.fetchone():
                    flash("Số điện thoại đã tồn tại trong hệ thống!", "danger")
                    return render_template("sua_gs_new.html", gs=gs)
            
            # Cập nhật thông tin gia sư
            query = """
                UPDATE GIASU
                SET HoTen = %s, SoDT = %s, BangCap = %s, MonDay = %s, KinhNghiem = %s
                WHERE MaGS = %s
            """
            cursor.execute(query, (ho_ten, so_dt, bang_cap, mon_day, kinh_nghiem, ma_gs))
            conn.commit()
            
            flash(f"Đã cập nhật thông tin gia sư {ho_ten} thành công!", "success")
            return redirect(url_for('xem_gs', ma_gs=ma_gs))
        
        cursor.close()
        conn.close()
        
        return render_template("sua_gs_new.html", gs=gs)
        
    except Exception as e:
        flash(f"Lỗi khi sửa thông tin gia sư: {str(e)}", "danger")
        return redirect(url_for('qlgs'))


# Xóa gia sư
@app.route("/xoa_gs/<ma_gs>")
@login_required
def xoa_gs(ma_gs):
    try:
        # Kết nối database
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Kiểm tra gia sư có tồn tại không
        cursor.execute("SELECT * FROM GIASU WHERE MaGS = %s", (ma_gs,))
        gs = cursor.fetchone()
        
        if not gs:
            flash("Không tìm thấy gia sư!", "danger")
            return redirect(url_for('qlgs'))
        
        # Kiểm tra gia sư có giao dịch không
        cursor.execute("SELECT * FROM GIAODICH WHERE MaGS = %s", (ma_gs,))
        if cursor.fetchone():
            flash("Không thể xóa gia sư này vì đã có giao dịch liên quan!", "danger")
            return redirect(url_for('qlgs'))
        
        # Xóa gia sư
        cursor.execute("DELETE FROM GIASU WHERE MaGS = %s", (ma_gs,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash(f"Đã xóa gia sư {gs['HoTen']} thành công!", "success")
        return redirect(url_for('qlgs'))
        
    except Exception as e:
        flash(f"Lỗi khi xóa gia sư: {str(e)}", "danger")
        return redirect(url_for('qlgs'))


# Tìm kiếm gia sư
@app.route("/tim_gs")
@login_required
def tim_gs():
    try:
        # Lấy tham số tìm kiếm
        keyword = request.args.get('keyword', '')
        field = request.args.get('field', 'all')
        
        if not keyword:
            return render_template("tim_gs_new.html")
        
        # Kết nối database
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Xây dựng câu truy vấn tìm kiếm
        query = "SELECT * FROM GIASU WHERE 1=1"
        params = []
        
        # Tìm theo từ khóa
        if field == 'all':
            query += " AND (HoTen LIKE %s OR SoDT LIKE %s OR BangCap LIKE %s OR MonDay LIKE %s)"
            params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
        else:
            query += f" AND {field} LIKE %s"
            params.append(f"%{keyword}%")
        
        # Thực hiện tìm kiếm
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template("tim_gs_new.html", results=results)
        
    except Exception as e:
        flash(f"Lỗi khi tìm kiếm gia sư: {str(e)}", "danger")
        return render_template("tim_gs_new.html")