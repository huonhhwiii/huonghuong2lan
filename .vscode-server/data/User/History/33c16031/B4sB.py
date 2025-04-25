from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from database import benh_nhan
from database.utils import get_next_benh_nhan_id, get_next_bac_si_id, get_next_dich_vu_id, get_next_lich_hen_id, get_next_phieu_kham_id
import datetime, json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# Quản lý bệnh nhân
@app.route('/benh-nhan')
def benh_nhan_list():
    benh_nhan_list = benh_nhan.get_all_benh_nhan()
    return render_template('benh_nhan.html', benh_nhan_list=benh_nhan_list)

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
        
        # Kiểm tra dữ liệu đầu vào
        if not ma_benh_nhan or not ho_ten or not so_dien_thoai:
            flash('Vui lòng điền đầy đủ thông tin bắt buộc', 'error')
        else:
            # Xử lý ngày sinh
            formatted_ngay_sinh = None
            if ngay_sinh:
                formatted_ngay_sinh = ngay_sinh  # Đã ở định dạng YYYY-MM-DD từ input type="date"
            
            # Lưu vào database
            ma_bn, result = benh_nhan.create_benh_nhan(
                ho_ten,
                so_dien_thoai,
                gioi_tinh,
                formatted_ngay_sinh,
                ma_benh_nhan
            )
            
            if result:
                flash(f'Thêm bệnh nhân thành công với mã {ma_bn}!', 'success')
                return redirect(url_for('benh_nhan_list'))
            else:
                flash('Có lỗi xảy ra khi thêm bệnh nhân', 'error')
                    
    # GET request - hiển thị form với mã bệnh nhân mới
    ma_benh_nhan = get_next_benh_nhan_id()
    return render_template('them_moi_benh_nhan.html', ma_benh_nhan=ma_benh_nhan)

# Tìm kiếm bệnh nhân
@app.route('/benh-nhan/tim-kiem', methods=['GET', 'POST'])
def tim_kiem_benh_nhan():
    # Dữ liệu mẫu cho kết quả tìm kiếm
    ket_qua = []

    if request.method == 'POST':
        tu_khoa = request.form.get('tu_khoa')
        loai_tim_kiem = request.form.get('loai_tim_kiem', 'ma_benh_nhan')
        
        if tu_khoa:
            ket_qua = benh_nhan.search_benh_nhan(tu_khoa, loai_tim_kiem)
            
    return render_template('tim_kiem_benh_nhan.html', ket_qua=ket_qua)

# Chi tiết bệnh nhân
@app.route('/benh-nhan/chi-tiet/<ma_bn>')
def chi_tiet_benh_nhan(ma_bn):
    bn = benh_nhan.get_benh_nhan_by_id(ma_bn)
    if not bn:
        flash('Không tìm thấy bệnh nhân', 'error')
        return redirect(url_for('benh_nhan_list'))
    return render_template('chi_tiet_benh_nhan.html', benh_nhan=bn)

# Chỉnh sửa bệnh nhân
@app.route('/benh-nhan/chinh-sua/<ma_bn>', methods=['GET', 'POST'])
def chinh_sua_benh_nhan(ma_bn):
    bn = benh_nhan.get_benh_nhan_by_id(ma_bn)
    if not bn:
        flash('Không tìm thấy bệnh nhân', 'error')
        return redirect(url_for('benh_nhan_list'))
        
    if request.method == 'POST':
        ho_ten = request.form.get('ho_ten')
        so_dien_thoai = request.form.get('so_dien_thoai')
        gioi_tinh = request.form.get('gioi_tinh')
        ngay_sinh = request.form.get('ngay_sinh')
        
        if not ho_ten or not so_dien_thoai:
            flash('Vui lòng điền đầy đủ thông tin bắt buộc', 'error')
        else:
            result = benh_nhan.update_benh_nhan(ma_bn, ho_ten, so_dien_thoai, gioi_tinh, ngay_sinh)
            if result:
                flash('Cập nhật thông tin bệnh nhân thành công!', 'success')
                return redirect(url_for('benh_nhan_list'))
            else:
                flash('Có lỗi xảy ra khi cập nhật thông tin bệnh nhân', 'error')
    
    return render_template('chinh_sua_benh_nhan.html', benh_nhan=bn)

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

# API endpoints
@app.route('/api/benh-nhan/<ma_bn>', methods=['GET'])
def api_get_benh_nhan(ma_bn):
    patient = benh_nhan.get_benh_nhan_by_id(ma_bn)
    if patient:
        return jsonify(patient)
    return jsonify({"error": "Không tìm thấy bệnh nhân"}), 404

@app.route('/api/benh-nhan/<ma_bn>', methods=['DELETE'])
def api_delete_benh_nhan(ma_bn):
    try:
        benh_nhan.delete_benh_nhan(ma_bn)
        return jsonify({"success": True, "message": "Xóa bệnh nhân thành công"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/benh-nhan/ma-moi', methods=['GET'])
def api_get_ma_benh_nhan_moi():
    # Lấy mã bệnh nhân mới nhất và tăng lên 1
    new_id = get_next_benh_nhan_id()
    return jsonify({"ma_benh_nhan": new_id})

# API để lấy mã mới cho các bảng khác
@app.route('/api/ma-moi/<loai>', methods=['GET'])
def api_get_ma_moi(loai):
    if loai == 'bac-si':
        return jsonify({"ma": get_next_bac_si_id()})
    elif loai == 'dich-vu':
        return jsonify({"ma": get_next_dich_vu_id()})
    elif loai == 'lich-hen':
        return jsonify({"ma": get_next_lich_hen_id()})
    elif loai == 'phieu-kham':
        return jsonify({"ma": get_next_phieu_kham_id()})
    else:
        return jsonify({"error": "Loại không hợp lệ"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)