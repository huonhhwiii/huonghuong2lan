from flask import Flask, render_template, redirect, request, url_for, flash, jsonify, session
from help import *
import os

app = Flask(__name__)
app.secret_key = 'n7_super_secret_key_123'

# Tạo bảng người dùng khi khởi động ứng dụng
# Trong Flask 2.0+, before_first_request đã bị loại bỏ
# Sử dụng cách khác để khởi tạo cơ sở dữ liệu
def initialize_database():
    try:
        create_users_table()
    except Exception as e:
        print(f"Lỗi khi khởi tạo cơ sở dữ liệu: {e}")

# Gọi hàm khởi tạo khi ứng dụng khởi động
with app.app_context():
    initialize_database()


# Middleware kiểm tra đăng nhập
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập để tiếp tục', 'warning')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# Trang đăng nhập
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = check_login(username, password)
        if user:
            # Lưu thông tin người dùng vào session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['quyen'] = user['quyen']
            
            flash(f"Đăng nhập thành công! Xin chào {user['ho_ten']}", "success")
            return redirect(url_for("trangchu"))
        else:
            flash("Tên đăng nhập hoặc mật khẩu không đúng", "danger")
    
    return render_template("login.html")

# Trang đăng ký
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        ho_ten = request.form.get("ho_ten")
        email = request.form.get("email")
        
        # Kiểm tra mật khẩu xác nhận
        if password != confirm_password:
            flash("Mật khẩu xác nhận không khớp", "danger")
            return render_template("register.html")
        
        # Đăng ký người dùng mới
        success, message = register_user(username, password, ho_ten, email)
        if success:
            flash(message, "success")
            return redirect(url_for("login"))
        else:
            flash(message, "danger")
    
    return render_template("register.html")

# Đăng xuất
@app.route("/logout")
def logout():
    # Xóa thông tin người dùng khỏi session
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('quyen', None)
    flash("Đã đăng xuất thành công", "success")
    return redirect(url_for("login"))

# Trang chu
@app.route("/")
def index():
    # Chuyển hướng đến trang đăng nhập nếu chưa đăng nhập
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('trangchu'))

# Trang chủ sau khi đăng nhập
@app.route("/trangchu")
@login_required
def trangchu():
    # Lấy số lượng phụ huynh, gia sư, giao dịch, lớp học để hiển thị trên trang chủ
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Đếm số lượng phụ huynh
        cursor.execute("SELECT COUNT(*) FROM PHUHUYNH")
        ph_count = cursor.fetchone()[0]
        
        # Đếm số lượng gia sư
        cursor.execute("SELECT COUNT(*) FROM GIASU")
        gs_count = cursor.fetchone()[0]
        
        # Đếm số lượng giao dịch
        cursor.execute("SELECT COUNT(*) FROM GIAODICH")
        gd_count = cursor.fetchone()[0]
        
        # Đếm số lượng lớp học
        cursor.execute("SELECT COUNT(*) FROM LOPHOC")
        lh_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        from datetime import datetime
        now = datetime.now()
        
        return render_template("trangchu_new.html", 
                              ph_count=ph_count, 
                              gs_count=gs_count, 
                              gd_count=gd_count, 
                              lh_count=lh_count,
                              now=now)
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu cho trang chủ: {e}")
        return render_template("trangchu_new.html")

# Trang quan ly phu huynh
@app.route("/qlph")
@login_required
def qlph():
    try:
        # Lấy danh sách phụ huynh từ cơ sở dữ liệu
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM PHUHUYNH")
        ds_ph = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template("qlph_new.html", ds_ph=ds_ph)
    except Exception as e:
        print(f"Lỗi khi lấy danh sách phụ huynh: {e}")
        flash("Có lỗi xảy ra khi tải danh sách phụ huynh", "danger")
        return render_template("qlph_new.html", ds_ph=[])

# Trang quan ly gia su
@app.route("/qlgs")
@login_required
def qlgs():
    try:
        # Lấy danh sách gia sư từ cơ sở dữ liệu
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM GIASU")
        ds_gs = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template("qlgs_new.html", ds_gs=ds_gs)
    except Exception as e:
        print(f"Lỗi khi lấy danh sách gia sư: {e}")
        flash("Có lỗi xảy ra khi tải danh sách gia sư", "danger")
        return render_template("qlgs_new.html", ds_gs=[])

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


# Trang quan ly giao dich (đã chuyển xuống phần Quản lý giao dịch)

# Trang quan ly lop hoc
@app.route("/qllh")
@login_required
def qllh():
    try:
        # Lấy danh sách lớp học từ cơ sở dữ liệu
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM LOPHOC")
        ds_lh = cursor.fetchall()
        
        # Đếm số lượng lớp học theo môn học
        cursor.execute("SELECT COUNT(*) FROM LOPHOC WHERE MonHoc LIKE '%Toán%'")
        math_classes = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM LOPHOC WHERE MonHoc LIKE '%Văn%'")
        literature_classes = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM LOPHOC WHERE MonHoc LIKE '%Anh%'")
        english_classes = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return render_template("qllh_new.html", 
                              ds_lh=ds_lh,
                              total_classes=len(ds_lh),
                              math_classes=math_classes,
                              literature_classes=literature_classes,
                              english_classes=english_classes)
    except Exception as e:
        print(f"Lỗi khi lấy danh sách lớp học: {e}")
        flash("Có lỗi xảy ra khi tải danh sách lớp học", "danger")
        return render_template("qllh_new.html", ds_lh=[])


"""
Quản lý phụ huynh
"""
# Thêm phụ huynh
@app.route("/them_ph", methods=["GET", "POST"])
@login_required
def them_ph():
    if request.method == "POST":
        try:
            # Lấy dữ liệu từ form
            ho_ten = request.form.get('hoTen')
            so_dt = request.form.get('soDT')
            dia_chi = request.form.get('diaChi')
            yeu_cau = request.form.get('yeuCau')
            
            # Kiểm tra dữ liệu
            if not ho_ten or not so_dt or not dia_chi:
                flash("Vui lòng điền đầy đủ thông tin bắt buộc!", "danger")
                return render_template("them_ph_new.html")
            
            # Kiểm tra định dạng số điện thoại
            import re
            if not re.match(r'^0[0-9]{9}$', so_dt):
                flash("Số điện thoại không hợp lệ! Vui lòng nhập 10 chữ số bắt đầu bằng số 0.", "danger")
                return render_template("them_ph_new.html")
            
            # Kết nối database và thêm phụ huynh
            conn = get_connection()
            cursor = conn.cursor()
            
            # Tạo mã phụ huynh tự động (PH + số ngẫu nhiên)
            import random
            ma_ph = f"PH{random.randint(1000, 9999):05d}"
            
            # Kiểm tra mã đã tồn tại chưa
            cursor.execute("SELECT COUNT(*) FROM PHUHUYNH WHERE MaPH = %s", (ma_ph,))
            if cursor.fetchone()[0] > 0:
                ma_ph = f"PH{random.randint(10000, 99999):05d}"
            
            # Thêm phụ huynh mới
            query = """
                INSERT INTO PHUHUYNH (MaPH, HoTen, SoDT, DiaChi, YeuCau)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (ma_ph, ho_ten, so_dt, dia_chi, yeu_cau))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            flash(f"Đã thêm phụ huynh {ho_ten} thành công!", "success")
            return redirect(url_for('qlph'))
            
        except Exception as e:
            flash(f"Lỗi khi thêm phụ huynh: {str(e)}", "danger")
            return render_template("them_ph_new.html")
    
    return render_template("them_ph_new.html")


# Tìm kiếm phụ huynh
@app.route("/tim_ph")
@login_required
def tim_ph():
    try:
        # Lấy tham số tìm kiếm
        keyword = request.args.get('keyword', '')
        field = request.args.get('field', 'all')
        
        if not keyword:
            return render_template("tim_ph_new.html")
        
        # Kết nối database
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Xây dựng câu truy vấn tìm kiếm
        query = "SELECT * FROM PHUHUYNH WHERE 1=1"
        params = []
        
        # Tìm theo từ khóa
        if field == 'all':
            query += " AND (HoTen LIKE %s OR SoDT LIKE %s OR DiaChi LIKE %s OR YeuCau LIKE %s)"
            params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
        else:
            query += f" AND {field} LIKE %s"
            params.append(f"%{keyword}%")
        
        # Thực hiện tìm kiếm
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template("tim_ph_new.html", results=results)
        
    except Exception as e:
        flash(f"Lỗi khi tìm kiếm phụ huynh: {str(e)}", "danger")
        return render_template("tim_ph_new.html")

# Sửa thông tin phụ huynh
@app.route("/sua_ph/<ma_ph>", methods=["GET", "POST"])
@login_required
def sua_ph(ma_ph):
    try:
        # Kết nối database
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Lấy thông tin phụ huynh
        cursor.execute("SELECT * FROM PHUHUYNH WHERE MaPH = %s", (ma_ph,))
        ph = cursor.fetchone()
        
        if not ph:
            flash("Không tìm thấy phụ huynh!", "danger")
            return redirect(url_for('qlph'))
        
        if request.method == "POST":
            # Lấy dữ liệu từ form
            ho_ten = request.form.get('hoTen')
            so_dt = request.form.get('soDT')
            dia_chi = request.form.get('diaChi')
            yeu_cau = request.form.get('yeuCau')
            
            # Kiểm tra dữ liệu
            if not ho_ten or not so_dt or not dia_chi:
                flash("Vui lòng điền đầy đủ thông tin bắt buộc!", "danger")
                return render_template("sua_ph_new.html", ph=ph)
            
            # Kiểm tra định dạng số điện thoại
            import re
            if not re.match(r'^0[0-9]{9}$', so_dt):
                flash("Số điện thoại không hợp lệ! Vui lòng nhập 10 chữ số bắt đầu bằng số 0.", "danger")
                return render_template("sua_ph_new.html", ph=ph)
            
            # Cập nhật thông tin phụ huynh
            query = """
                UPDATE PHUHUYNH
                SET HoTen = %s, SoDT = %s, DiaChi = %s, YeuCau = %s
                WHERE MaPH = %s
            """
            cursor.execute(query, (ho_ten, so_dt, dia_chi, yeu_cau, ma_ph))
            conn.commit()
            
            flash(f"Đã cập nhật thông tin phụ huynh {ho_ten} thành công!", "success")
            return redirect(url_for('xem_ph', ma_ph=ma_ph))
        
        cursor.close()
        conn.close()
        
        return render_template("sua_ph_new.html", ph=ph)
        
    except Exception as e:
        flash(f"Lỗi khi sửa thông tin phụ huynh: {str(e)}", "danger")
        return redirect(url_for('qlph'))

# Xem chi tiết phụ huynh
@app.route("/xem_ph/<ma_ph>")
@login_required
def xem_ph(ma_ph):
    try:
        # Kết nối database
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Lấy thông tin phụ huynh
        cursor.execute("SELECT * FROM PHUHUYNH WHERE MaPH = %s", (ma_ph,))
        ph = cursor.fetchone()
        
        if not ph:
            flash("Không tìm thấy phụ huynh!", "danger")
            return redirect(url_for('qlph'))
        
        # Lấy danh sách lớp học của phụ huynh (thông qua giao dịch)
        query_lh = """
            SELECT lh.* 
            FROM LOPHOC lh
            JOIN GIAODICH gd ON lh.MaGD = gd.MaGD
            WHERE gd.MaPH = %s
        """
        cursor.execute(query_lh, (ma_ph,))
        ds_lh = cursor.fetchall()
        
        # Lấy lịch sử giao dịch của phụ huynh
        query_gd = """
            SELECT gd.*, gs.HoTen AS TenGS
            FROM GIAODICH gd
            LEFT JOIN GIASU gs ON gd.MaGS = gs.MaGS
            WHERE gd.MaPH = %s
        """
        cursor.execute(query_gd, (ma_ph,))
        ds_gd = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template("xem_ph_new.html", ph=ph, ds_lh=ds_lh, ds_gd=ds_gd)
        
    except Exception as e:
        flash(f"Lỗi khi xem thông tin phụ huynh: {str(e)}", "danger")
        return redirect(url_for('qlph'))

# Xóa phụ huynh
@app.route("/xoa_ph/<ma_ph>")
@login_required
def xoa_ph(ma_ph):
    try:
        # Kết nối database
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Kiểm tra phụ huynh có tồn tại không
        cursor.execute("SELECT HoTen FROM PHUHUYNH WHERE MaPH = %s", (ma_ph,))
        ph = cursor.fetchone()
        
        if not ph:
            flash("Không tìm thấy phụ huynh!", "danger")
            return redirect(url_for('qlph'))
        
        # Kiểm tra phụ huynh có giao dịch không
        cursor.execute("SELECT COUNT(*) AS count FROM GIAODICH WHERE MaPH = %s", (ma_ph,))
        count = cursor.fetchone()['count']
        
        if count > 0:
            flash(f"Không thể xóa phụ huynh {ph['HoTen']} vì đã có {count} giao dịch liên quan!", "warning")
            return redirect(url_for('qlph'))
        
        # Xóa phụ huynh
        cursor.execute("DELETE FROM PHUHUYNH WHERE MaPH = %s", (ma_ph,))
        conn.commit()
        
        flash(f"Đã xóa phụ huynh {ph['HoTen']} thành công!", "success")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        flash(f"Lỗi khi xóa phụ huynh: {str(e)}", "danger")
    
    return redirect(url_for('qlph'))



"""
Quản lý gia sư - Các hàm cũ đã được thay thế bằng các hàm mới
"""

# Các hàm cũ đã được thay thế bằng các hàm mới ở phần trên

# Hàm lưu gia sư cũ - giữ lại để tương thích
@app.route("/luu_gs", methods=["POST"])
def luu_gs():
    try:
        # Chuyển hướng đến hàm thêm gia sư mới
        return redirect(url_for("them_gs"))
    except Exception as e:
        flash(f"Lỗi khi thêm gia sư: {str(e)}", "error")
        return redirect(url_for("them_gs"))
    

# Các hàm cũ đã được thay thế bằng các hàm mới ở phần trên
# Giữ lại định nghĩa rỗng để tránh lỗi
def sua_gs_old():
    pass

# Xem danh sách gia sư - Hàm cũ đã được thay thế
@app.route("/ds_gs")
def ds_gs():
    # Chuyển hướng đến trang quản lý gia sư mới
    return redirect(url_for("qlgs"))

# Xóa gia sư - Hàm cũ đã được thay thế
# Giữ lại route để tương thích với các liên kết cũ
@app.route("/xoa_gs")
def xoa_gs_old():
    return redirect(url_for("qlgs"))

# Chuyển hướng các route cũ đến route mới
@app.route("/xoa_gs/<maph>", methods=["GET"])
def delete_tutor_route(maph):
    # Chuyển hướng đến route xóa gia sư mới
    return redirect(url_for("xoa_gs", ma_gs=maph))



"""
Quản lý giao dịch
"""
# Trang quản lý giao dịch
@app.route("/qlgd")
@login_required
def qlgd():
    try:
        # Lấy danh sách giao dịch từ cơ sở dữ liệu
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Lấy danh sách giao dịch với thông tin phụ huynh và gia sư
        query = """
            SELECT gd.*, ph.HoTen AS TenPH, gs.HoTen AS TenGS
            FROM GIAODICH gd
            LEFT JOIN PHUHUYNH ph ON gd.MaPH = ph.MaPH
            LEFT JOIN GIASU gs ON gd.MaGS = gs.MaGS
        """
        cursor.execute(query)
        ds_gd = cursor.fetchall()
        
        # Đếm số lượng giao dịch theo trạng thái
        # Trong trường hợp này, chúng ta chưa có trường trạng thái, nên tạm thời đặt tất cả là 'completed'
        for gd in ds_gd:
            gd['TrangThai'] = 'completed'
            gd['SoTien'] = gd['PhiPH']  # Để tương thích với template
        
        # Đếm số lượng giao dịch
        total_transactions = len(ds_gd)
        completed_transactions = total_transactions
        pending_transactions = 0
        cancelled_transactions = 0
        
        cursor.close()
        conn.close()
        
        return render_template("qlgd_new.html", 
                              ds_gd=ds_gd,
                              total_transactions=total_transactions,
                              completed_transactions=completed_transactions,
                              pending_transactions=pending_transactions,
                              cancelled_transactions=cancelled_transactions)
    except Exception as e:
        print(f"Lỗi khi lấy danh sách giao dịch: {e}")
        flash("Có lỗi xảy ra khi tải danh sách giao dịch", "danger")
        return render_template("qlgd_new.html", ds_gd=[])

# Thêm giao dịch mới
@app.route("/them_gd", methods=["GET", "POST"])
@login_required
def them_gd():
    if request.method == "POST":
        try:
            # Lấy dữ liệu từ form
            ma_gd = request.form.get('maGD', '')
            ngay_gd = request.form.get('ngayGD')
            phi_gs = float(request.form.get('phiGS'))
            phi_ph = float(request.form.get('phiPH'))
            ma_ph = request.form.get('maPH')
            ma_gs = request.form.get('maGS')
            
            # Kiểm tra dữ liệu
            if not ngay_gd or not ma_ph or not ma_gs:
                flash("Vui lòng điền đầy đủ thông tin bắt buộc!", "danger")
                next_id = get_next_giaodich_id()
                return render_template("them_gd_new.html", next_id=next_id)
            
            # Kiểm tra logic phí
            if phi_ph < phi_gs:
                flash("Phí phụ huynh không được nhỏ hơn phí gia sư!", "danger")
                next_id = get_next_giaodich_id()
                return render_template("them_gd_new.html", next_id=next_id)
            
            # Kiểm tra phụ huynh và gia sư có tồn tại không
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM PHUHUYNH WHERE MaPH = %s", (ma_ph,))
            if not cursor.fetchone():
                flash("Mã phụ huynh không tồn tại trong hệ thống!", "danger")
                next_id = get_next_giaodich_id()
                return render_template("them_gd_new.html", next_id=next_id)
            
            cursor.execute("SELECT * FROM GIASU WHERE MaGS = %s", (ma_gs,))
            if not cursor.fetchone():
                flash("Mã gia sư không tồn tại trong hệ thống!", "danger")
                next_id = get_next_giaodich_id()
                return render_template("them_gd_new.html", next_id=next_id)
            
            cursor.close()
            conn.close()
            
            # Thêm giao dịch mới vào database
            created_ma_gd = insert_giao_dich(ma_gd, ngay_gd, phi_gs, phi_ph, ma_ph, ma_gs)
            
            flash(f"Đã thêm giao dịch thành công với mã: {created_ma_gd}!", "success")
            return redirect(url_for('qlgd'))
            
        except Exception as e:
            flash(f"Lỗi khi thêm giao dịch: {str(e)}", "danger")
            next_id = get_next_giaodich_id()
            return render_template("them_gd_new.html", next_id=next_id)
    
    # GET request
    next_id = get_next_giaodich_id()
    return render_template("them_gd_new.html", next_id=next_id)

# Xem chi tiết giao dịch
@app.route("/xem_gd/<ma_gd>")
@login_required
def xem_gd(ma_gd):
    try:
        # Kết nối database
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Lấy thông tin giao dịch
        cursor.execute("SELECT * FROM GIAODICH WHERE MaGD = %s", (ma_gd,))
        gd = cursor.fetchone()
        
        if not gd:
            flash("Không tìm thấy giao dịch!", "danger")
            return redirect(url_for('qlgd'))
        
        # Lấy thông tin phụ huynh
        cursor.execute("SELECT * FROM PHUHUYNH WHERE MaPH = %s", (gd['MaPH'],))
        ph = cursor.fetchone()
        
        # Lấy thông tin gia sư
        cursor.execute("SELECT * FROM GIASU WHERE MaGS = %s", (gd['MaGS'],))
        gs = cursor.fetchone()
        
        # Lấy danh sách lớp học liên quan đến giao dịch
        cursor.execute("SELECT * FROM LOPHOC WHERE MaGD = %s", (ma_gd,))
        ds_lh = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template("xem_gd_new.html", gd=gd, ph=ph, gs=gs, ds_lh=ds_lh)
        
    except Exception as e:
        flash(f"Lỗi khi xem thông tin giao dịch: {str(e)}", "danger")
        return redirect(url_for('qlgd'))

# Sửa thông tin giao dịch
@app.route("/sua_gd/<ma_gd>", methods=["GET", "POST"])
@login_required
def sua_gd(ma_gd):
    try:
        # Kết nối database
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Lấy thông tin giao dịch
        cursor.execute("SELECT * FROM GIAODICH WHERE MaGD = %s", (ma_gd,))
        gd = cursor.fetchone()
        
        if not gd:
            flash("Không tìm thấy giao dịch!", "danger")
            return redirect(url_for('qlgd'))
        
        if request.method == "POST":
            try:
                # Lấy dữ liệu từ form
                ngay_gd = request.form.get('ngayGD')
                ma_ph = request.form.get('maPH')
                ma_gs = request.form.get('maGS')
                phi_ph = float(request.form.get('phiPH'))
                phi_gs = float(request.form.get('phiGS'))
                
                print(f"Dữ liệu form: {ngay_gd}, {ma_ph}, {ma_gs}, {phi_ph}, {phi_gs}")
                
                # Kiểm tra dữ liệu
                if not ngay_gd or not ma_ph or not ma_gs:
                    flash("Vui lòng điền đầy đủ thông tin bắt buộc!", "danger")
                    return render_template("sua_gd_new.html", gd=gd)
                
                # Kiểm tra logic phí
                if phi_ph < phi_gs:
                    flash("Phí phụ huynh không được nhỏ hơn phí gia sư!", "danger")
                    return render_template("sua_gd_new.html", gd=gd)
                
                # Kiểm tra phụ huynh và gia sư có tồn tại không
                cursor.execute("SELECT * FROM PHUHUYNH WHERE MaPH = %s", (ma_ph,))
                if not cursor.fetchone():
                    flash("Mã phụ huynh không tồn tại trong hệ thống!", "danger")
                    return render_template("sua_gd_new.html", gd=gd)
                
                cursor.execute("SELECT * FROM GIASU WHERE MaGS = %s", (ma_gs,))
                if not cursor.fetchone():
                    flash("Mã gia sư không tồn tại trong hệ thống!", "danger")
                    return render_template("sua_gd_new.html", gd=gd)
                
                # Cập nhật thông tin giao dịch
                result = update_transaction(ma_gd, ngay_gd, ma_gs, ma_ph, phi_ph, phi_gs)
                
                if result:
                    flash("Đã cập nhật thông tin giao dịch thành công!", "success")
                    return redirect(url_for('xem_gd', ma_gd=ma_gd))
                else:
                    flash("Có lỗi xảy ra khi cập nhật giao dịch!", "danger")
                    return render_template("sua_gd_new.html", gd=gd)
            except Exception as e:
                print(f"Lỗi khi xử lý form: {str(e)}")
                flash(f"Lỗi khi xử lý form: {str(e)}", "danger")
                return render_template("sua_gd_new.html", gd=gd)
        
        cursor.close()
        conn.close()
        
        return render_template("sua_gd_new.html", gd=gd)
        
    except Exception as e:
        print(f"Lỗi khi sửa thông tin giao dịch: {str(e)}")
        flash(f"Lỗi khi sửa thông tin giao dịch: {str(e)}", "danger")
        return redirect(url_for('qlgd'))

# Xóa giao dịch
@app.route("/xoa_gd/<ma_gd>")
@login_required
def xoa_gd(ma_gd):
    try:
        # Kết nối database
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Kiểm tra giao dịch có tồn tại không
        cursor.execute("SELECT * FROM GIAODICH WHERE MaGD = %s", (ma_gd,))
        gd = cursor.fetchone()
        
        if not gd:
            flash("Không tìm thấy giao dịch!", "danger")
            return redirect(url_for('qlgd'))
        
        # Kiểm tra giao dịch có lớp học liên quan không
        cursor.execute("SELECT * FROM LOPHOC WHERE MaGD = %s", (ma_gd,))
        if cursor.fetchone():
            flash("Không thể xóa giao dịch này vì đã có lớp học liên quan!", "danger")
            return redirect(url_for('qlgd'))
        
        # Xóa giao dịch
        cursor.execute("DELETE FROM GIAODICH WHERE MaGD = %s", (ma_gd,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash("Đã xóa giao dịch thành công!", "success")
        return redirect(url_for('qlgd'))
        
    except Exception as e:
        flash(f"Lỗi khi xóa giao dịch: {str(e)}", "danger")
        return redirect(url_for('qlgd'))

# Tìm kiếm giao dịch
@app.route("/tim_gd")
@login_required
def tim_gd():
    try:
        # Lấy tham số tìm kiếm
        keyword = request.args.get('keyword', '')
        
        if keyword:
            # Kết nối database
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Tìm kiếm giao dịch
            query = """
                SELECT gd.*, ph.HoTen AS TenPH, gs.HoTen AS TenGS
                FROM GIAODICH gd
                LEFT JOIN PHUHUYNH ph ON gd.MaPH = ph.MaPH
                LEFT JOIN GIASU gs ON gd.MaGS = gs.MaGS
                WHERE gd.MaGD LIKE %s OR ph.HoTen LIKE %s OR gs.HoTen LIKE %s
            """
            like_keyword = f"%{keyword}%"
            cursor.execute(query, (like_keyword, like_keyword, like_keyword))
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
        else:
            results = []
        
        return render_template("tim_gd_new.html", results=results, keyword=keyword)
        
    except Exception as e:
        flash(f"Lỗi khi tìm kiếm giao dịch: {str(e)}", "danger")
        return render_template("tim_gd_new.html")

# Các route cũ - giữ lại để tương thích
@app.route("/ds_gd")
def ds_gd():
    return redirect(url_for("qlgd"))

@app.route("/tk_gd")
def tk_gd():
    return render_template("thong-ke-giao-dich.html")



"""
Quản lý lớp học
"""
# Thêm lớp học
@app.route("/them_lh", methods=["GET", "POST"])
def them_lh():
    if request.method == "POST":
        # Handle saving class data
        class_data = request.get_json()  # Get JSON data from the request
        
        # Nếu không có mã lớp học, hàm save_class_data sẽ tự động tạo
        result = save_class_data(class_data)
        
        if result:
            return jsonify({"success": True, "message": "Class data saved successfully!"})
        else:
            return jsonify({"success": False, "message": "Error saving class data!"}), 500
    
    # Lấy mã lớp học tiếp theo để hiển thị trong form
    next_id = get_next_lophoc_id()
    return render_template("them-moi-lop-hoc.html", next_id=next_id)  # For GET request, render the form


# Tìm lớp học
@app.route("/tim_lh", methods=["GET", "POST"]) 
def tim_lh():
    search_term = request.form.get("search_term", "")
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Perform the search query
    if search_term:
        query = f"""
        SELECT * FROM LOPHOC
        WHERE MaLop LIKE %s OR MonHoc LIKE %s
        """
        cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
    else:
        query = "SELECT * FROM LOPHOC"
        cursor.execute(query)
    
    classes = cursor.fetchall()
    connection.close()
    
    return render_template("tim-kiem-lop-hoc.html", classes=classes)


# Sửa lớp học
@app.route("/sua_lh", methods=["GET", "POST"])
def sua_lh():
    if request.method == "GET":
        # Lấy thông tin lớp học theo MaLop (ví dụ 'LH0001')
        class_info = get_class_info('LH0001')
        return render_template("sua-lop-hoc.html", class_info=class_info)
    
    if request.method == "POST":
        # Lấy dữ liệu từ form
        class_data = {
            'id': request.form['classId'],
            'subject': request.form['subject'],
            'grade': request.form['grade'],
            'schedule': request.form['schedule'],
            'location': request.form['location'],
        }
        
        # Cập nhật thông tin lớp học
        update_class_info(class_data)
        
        flash('Thông tin lớp học đã được cập nhật thành công!', 'success')
        return redirect(url_for('sua_lh'))


# Xem lớp học
@app.route('/ds_lh', methods=['GET', 'POST'])
def ds_lh():
    keyword = request.args.get('search', '')
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if keyword:
        query = "SELECT * FROM LOPHOC WHERE MonHoc LIKE %s OR CapHoc LIKE %s"
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
    else:
        cursor.execute("SELECT * FROM LOPHOC")

    ds_lop = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('danh-sach-lop-hoc.html', ds_lop=ds_lop)


# Xóa lớp học
@app.route("/xoa_lh", methods=['GET'])
def xoa_lh():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM LOPHOC")
    ds_lop = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("xoa-lop-hoc.html", ds_lop=ds_lop)

@app.route("/xoa_lh/<ma_lop>", methods=['POST'])
def xoa_lop_theo_ma(ma_lop):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM LOPHOC WHERE MaLop = %s", (ma_lop,))
        conn.commit()
        flash(f"Đã xóa lớp học {ma_lop}", "success")
    except Exception as e:
        flash(f"Lỗi xóa lớp học: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for("xoa_lh"))




if __name__ == "__main__":
    app.run(debug=True)