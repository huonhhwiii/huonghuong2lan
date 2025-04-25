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

# Trang quan ly giao dich
@app.route("/qlgd")
@login_required
def qlgd():
    try:
        # Lấy danh sách giao dịch từ cơ sở dữ liệu
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Lấy danh sách giao dịch kèm theo tên phụ huynh và gia sư
        query = """
            SELECT gd.*, ph.HoTen AS TenPH, gs.HoTen AS TenGS
            FROM GIAODICH gd
            LEFT JOIN PHUHUYNH ph ON gd.MaPH = ph.MaPH
            LEFT JOIN GIASU gs ON gd.MaGS = gs.MaGS
        """
        cursor.execute(query)
        ds_gd = cursor.fetchall()
        
        # Đếm số lượng giao dịch theo trạng thái
        cursor.execute("SELECT COUNT(*) FROM GIAODICH WHERE TrangThai = 'completed'")
        completed_transactions = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM GIAODICH WHERE TrangThai = 'pending'")
        pending_transactions = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM GIAODICH WHERE TrangThai = 'cancelled'")
        cancelled_transactions = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return render_template("qlgd_new.html", 
                              ds_gd=ds_gd,
                              total_transactions=len(ds_gd),
                              completed_transactions=completed_transactions,
                              pending_transactions=pending_transactions,
                              cancelled_transactions=cancelled_transactions)
    except Exception as e:
        print(f"Lỗi khi lấy danh sách giao dịch: {e}")
        flash("Có lỗi xảy ra khi tải danh sách giao dịch", "danger")
        return render_template("qlgd_new.html", ds_gd=[])

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
            email = request.form.get('email')
            trang_thai = request.form.get('trangThai')
            ghi_chu = request.form.get('ghiChu')
            
            # Kiểm tra dữ liệu
            if not ho_ten or not so_dt or not dia_chi:
                flash("Vui lòng điền đầy đủ thông tin bắt buộc!", "danger")
                return render_template("them_ph_new.html")
            
            # Kết nối database và thêm phụ huynh
            conn = get_connection()
            cursor = conn.cursor()
            
            # Tạo mã phụ huynh tự động (PH + số ngẫu nhiên)
            import random
            ma_ph = f"PH{random.randint(1000, 9999)}"
            
            # Kiểm tra mã đã tồn tại chưa
            cursor.execute("SELECT COUNT(*) FROM PHUHUYNH WHERE MaPH = %s", (ma_ph,))
            if cursor.fetchone()[0] > 0:
                ma_ph = f"PH{random.randint(10000, 99999)}"
            
            # Thêm phụ huynh mới
            query = """
                INSERT INTO PHUHUYNH (MaPH, HoTen, SoDT, DiaChi, Email, TrangThai, GhiChu)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (ma_ph, ho_ten, so_dt, dia_chi, email, trang_thai, ghi_chu))
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
        status = request.args.get('status', 'all')
        
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
            query += " AND (HoTen LIKE %s OR SoDT LIKE %s OR DiaChi LIKE %s OR Email LIKE %s)"
            params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
        else:
            query += f" AND {field} LIKE %s"
            params.append(f"%{keyword}%")
        
        # Lọc theo trạng thái
        if status != 'all':
            query += " AND TrangThai = %s"
            params.append(status)
        
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
            email = request.form.get('email')
            trang_thai = request.form.get('trangThai')
            ghi_chu = request.form.get('ghiChu')
            
            # Kiểm tra dữ liệu
            if not ho_ten or not so_dt or not dia_chi:
                flash("Vui lòng điền đầy đủ thông tin bắt buộc!", "danger")
                return render_template("sua_ph_new.html", ph=ph)
            
            # Cập nhật thông tin phụ huynh
            query = """
                UPDATE PHUHUYNH
                SET HoTen = %s, SoDT = %s, DiaChi = %s, Email = %s, TrangThai = %s, GhiChu = %s
                WHERE MaPH = %s
            """
            cursor.execute(query, (ho_ten, so_dt, dia_chi, email, trang_thai, ghi_chu, ma_ph))
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
Quản lý gia sư
"""
# Thêm gia sư
@app.route("/them_gs")
def them_gs():
    next_id = get_next_giasu_id()
    return render_template("them-moi-gia-su.html", next_id=next_id)

@app.route("/luu_gs", methods=["POST"])
def luu_gs():
    try:
        ma_gs = request.form["tutorId"]
        ho_ten = request.form["fullName"]
        sdt = request.form["phone"]
        bang_cap = request.form.get("qualification", "")
        mon_day = request.form.get("subject", "")
        kinh_nghiem = request.form.get("experience", "")
        
        insert_giasu(ma_gs, ho_ten, sdt, bang_cap, mon_day, kinh_nghiem)
        flash("Thêm gia sư thành công!", "success")
        return redirect(url_for("them_gs"))
    except Exception as e:
        flash(f"Lỗi khi thêm gia sư: {str(e)}", "error")
        return redirect(url_for("them_gs"))
    

# Tìm gia sư
@app.route("/tim_gs", methods=["GET"])
def tim_gs():
    search_term = request.args.get("q", "")
    tutors = search_tutors(search_term) if search_term else []
    return render_template("tim-kiem-gia-su.html", tutors=tutors, search_term=search_term)


# Sửa gia sư
@app.route("/sua_gs", methods=["GET", "POST"])
def sua_gs():
    if request.method == "POST":
        # Get data from the form submission
        ma_gia_su = request.form['tutorId']
        ho_ten = request.form['Name']
        so_dien_thoai = request.form['phone']
        bang_cap = request.form['qualification']
        mon_day = request.form['subject']
        kinh_nghiem = request.form['exp']

        # Update the parent's data
        success = update_tutor(ma_gia_su, ho_ten, so_dien_thoai, bang_cap, mon_day, kinh_nghiem)
        
        if success:
            flash('Thông tin phụ huynh đã được cập nhật!', 'success')
            return redirect(url_for('sua_gs', success=True))
        else:
            flash('Cập nhật không thành công!', 'error')
            return redirect(url_for('sua_gs', success=False))

    # If it's a GET request, fetch the parent information to display in the form
    tutor_id = request.args.get('tutor_id', None)
    tutor = None
    if tutor_id:
        results = search_tutors(tutor_id)
        if results:
            tutor = results[0]  # Get the first result (assuming ID is unique)
    
    return render_template("sua-gia-su.html", tutor=tutor)


# Xem gia sư
@app.route("/ds_gs")
def ds_gs():
    # Fetch parent data from the database using the function from help.py
    tutors = get_tutor_list()
    return render_template("danh-sach-gia-su.html", tutors=tutors)


# Xóa gia sư
@app.route("/xoa_gs")
def xoa_gs():
    tutors = get_tutor_list()
    return render_template("xoa-gia-su.html", tutors = tutors)
@app.route("/xoa_gs/<maph>", methods=["GET"])
def delete_tutor_route(maph):
    delete_tutor(maph)
    return redirect(url_for("xoa_gs"))



"""
Quản lý giao dịch
"""
# Thêm giao dịch
@app.route("/them_gd", methods=['GET', 'POST'])
def them_gd():
    if request.method == 'POST':
        try:
            # Lấy mã giao dịch từ form, nếu không có sẽ tự động tạo trong hàm insert_giao_dich
            maGD = request.form.get('maGD', '')
            ngayGD = request.form['ngayGD']
            phiGS = float(request.form['phiGS'])
            phiPH = float(request.form['phiPH'])
            maPH = request.form['maPH']
            maGS = request.form['maGS']

            # Check basic logic
            if phiPH < phiGS:
                flash("Phí phụ huynh không được nhỏ hơn phí gia sư!", "danger")
                return redirect(url_for('them_gd'))

            # Insert to database và nhận lại mã giao dịch đã tạo
            created_maGD = insert_giao_dich(maGD, ngayGD, phiGS, phiPH, maPH, maGS)
            flash(f"Thêm giao dịch thành công với mã: {created_maGD}!", "success")
            return redirect(url_for('them_gd'))
        except Exception as e:
            print("Lỗi khi thêm giao dịch:", e)
            flash("Đã xảy ra lỗi khi thêm giao dịch!", "danger")
            return redirect(url_for('them_gd'))

    # Lấy mã giao dịch tiếp theo để hiển thị trong form
    next_id = get_next_giaodich_id()
    return render_template("them-moi-giao-dich.html", next_id=next_id)


# Tìm kiếm giao dịch
@app.route("/tim_gd", methods=['GET'])
def tim_gd():
    keyword = request.args.get('search', '')
    if keyword:
        transactions = search_transactions(keyword)
    else:
        transactions = get_all_transactions()
    return render_template("tim-kiem-giao-dich.html", transactions=transactions, search=keyword)

# Sửa giao dịch
@app.route("/sua_gd", methods=["GET", "POST"])
def sua_gd():
    if request.method == "POST":
        MaGD = request.form["MaGD"]
        NgayGD = request.form["NgayGD"]
        MaGS = request.form["MaGS"]
        MaPH = request.form["MaPH"]
        PhiPH = request.form["SoTien"]  # HTML name="SoTien" thực ra là phí phụ huynh
        PhiGS = request.form["TutorFee"]

        if float(PhiPH) < float(PhiGS):
            flash("❌ Phí phụ huynh không được nhỏ hơn phí gia sư!", "error")
            return redirect(url_for("sua_gd", MaGD=MaGD))  # flash + reload form

        try:
            update_transaction(MaGD, NgayGD, MaGS, MaPH, PhiPH, PhiGS)
            print("Cập nhật thành công!")
            return redirect(f"/sua_gd?MaGD={MaGD}")  # ✅ redirect to same edit page
        except Exception as e:
            print("Lỗi khi cập nhật giao dịch:", e)
            return redirect(f"/sua_gd?MaGD={MaGD}")  # redirect even if error

    # GET request
    MaGD = request.args.get("MaGD", "GD00001")
    gd = get_transaction_by_id(MaGD)
    return render_template("sua-giao-dich.html", gd=gd)


# Xem giao dịch
@app.route("/ds_gd")
def ds_gd():
    danh_sach = get_all_giao_dich()  # Gọi từ help.py
    return render_template("danh-sach-giao-dich.html", danh_sach_gd=danh_sach)


# Xóa giao dịch
@app.route("/xoa_gd", methods=["GET", "POST"])
def xoa_gd():
    if request.method == "POST":
        transaction_id = request.form.get("delete")
        if transaction_id:
            delete_transaction(transaction_id)
            return redirect(url_for("xoa_gd"))
    
    # Get list of transactions from the database
    transactions = get_transactions()
    return render_template("xoa-giao-dich.html", transactions=transactions)

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