from flask import Flask, render_template,redirect, request, url_for, flash, jsonify
from help import *

app = Flask(__name__)
app.secret_key = 'n7_super_secret_key_123'


# Trang chu
@app.route("/")
def trangchu():
    return render_template("trangchu.html")

# Trang quan ly phu huynh
@app.route("/qlph")
def qlph():
    return render_template("qlph.html")

# Trang quan ly gia su
@app.route("/qlgs")
def qlgs():
    return render_template("qlgs.html")

# Trang quan ly giao dich
@app.route("/glgd")
def qlgd():
    return render_template("qlgd.html")

# Trang quan ly lop hoc
@app.route("/qllh")
def qllh():
    return render_template("qllh.html")


"""
Quản lý phụ huynh
"""
# Thêm phụ huynh
@app.route("/them_ph", methods = ["GET", "POST"])
def them_ph():
    if request.method == "POST":
        # Lấy mã phụ huynh từ form, nếu không có sẽ tự động tạo trong hàm insert_parent
        parent_id = request.form.get("parentId", "")
        full_name = request.form["fullName"]
        address = request.form["address"]
        phone = request.form["phone"]
        requirements = request.form["requirements"]

        if insert_parent(parent_id, full_name, address, phone, requirements):
            flash("Đã thêm phụ huynh thành công!", "success")
        else:
            flash("Có lỗi xảy ra khi thêm phụ huynh.", "danger")

        return redirect(url_for("them_ph"))

    # Lấy mã phụ huynh tiếp theo để hiển thị trong form
    next_id = get_next_phuhuynh_id()
    return render_template("them-moi-phu-huynh.html", next_id=next_id)


# Tìm kiếm phụ huynh
@app.route("/tim_ph", methods=['GET', 'POST'])
def tim_ph():
    if request.method == 'POST':
        keyword = request.form.get('search_keyword', '')
        results = search_parent(keyword)  # Call the search function
        return render_template('tim-kiem-phu-huynh.html', results=results)
    return render_template('tim-kiem-phu-huynh.html', results=[])

# Sửa phụ huynh
@app.route("/sua_ph", methods=["GET", "POST"])
def sua_ph():
    if request.method == "POST":
        # Get data from the form submission
        ma_phu_huynh = request.form['parentId']
        ho_ten = request.form['parentName']
        so_dien_thoai = request.form['phone']
        yeu_cau = request.form['requirements']
        dia_chi = request.form['address']

        # Update the parent's data
        success = update_parent(ma_phu_huynh, ho_ten, dia_chi, so_dien_thoai, yeu_cau)
        
        if success:
            flash('Thông tin phụ huynh đã được cập nhật!', 'success')
            return redirect(url_for('sua_ph', success=True))
        else:
            flash('Cập nhật không thành công!', 'error')
            return redirect(url_for('sua_ph', success=False))

    # If it's a GET request, fetch the parent information to display in the form
    parent_id = request.args.get('parent_id', None)
    parent = None
    if parent_id:
        results = search_parent(parent_id)
        if results:
            parent = results[0]  # Get the first result (assuming ID is unique)
    
    return render_template("sua-phu-huynh.html", parent=parent)

# Xem phụ huynh
@app.route("/ds_ph")
def ds_ph():
    # Fetch parent data from the database using the function from help.py
    parents = get_parent_list()
    return render_template("danh-sach-phu-huynh.html", parents=parents)

# Xóa phụ huynh
@app.route("/xoa_ph")
def xoa_ph():
    parents = get_parent_list()
    return render_template("xoa-phu-huynh.html", parents=parents)
@app.route("/xoa_ph/<maph>", methods=["GET"])
def delete_parent_route(maph):
    delete_parent(maph)
    return redirect(url_for("xoa_ph"))



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