from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# Quản lý bệnh nhân
@app.route('/benh-nhan')
def benh_nhan():
    return render_template('benh_nhan.html')

# Thêm mới bệnh nhân
@app.route('/benh-nhan/them-moi', methods=['GET', 'POST'])
def them_moi_benh_nhan():
    if request.method == 'POST':
        # Xử lý dữ liệu form khi submit
        ma_benh_nhan = request.form.get('ma_benh_nhan')
        ho_ten = request.form.get('ho_ten')
        so_dien_thoai = request.form.get('so_dien_thoai')
        gioi_tinh = request.form.get('gioi_tinh')
        ngay_sinh = request.form.get('ngay_sinh')
        
        # Kiểm tra dữ liệu
        if not ma_benh_nhan or not ho_ten or not so_dien_thoai:
            flash('Vui lòng điền đầy đủ thông tin bắt buộc', 'error')
        else:
            # Xử lý lưu dữ liệu vào database (sẽ thêm sau)
            flash('Thêm bệnh nhân thành công!', 'success')
            return redirect(url_for('benh_nhan'))
    
    return render_template('them_moi_benh_nhan.html')

# Quản lý bác sĩ
@app.route('/bac-si')
def bac_si():
    return render_template('bac_si.html')

# Quản lý phiếu khám
@app.route('/phieu-kham')
def phieu_kham():
    return render_template('phieu_kham.html')

# Quản lý lịch hẹn
@app.route('/lich-hen')
def lich_hen():
    return render_template('lich_hen.html')

# Quản lý dịch vụ
@app.route('/dich-vu')
def dich_vu():
    return render_template('dich_vu.html')

# Quản lý thanh toán
@app.route('/thanh-toan')
def thanh_toan():
    return render_template('thanh_toan.html')

# Báo cáo và thống kê
@app.route('/bao-cao')
def bao_cao():
    return render_template('bao_cao.html')

if __name__ == '__main__':
    app.run(debug=True)