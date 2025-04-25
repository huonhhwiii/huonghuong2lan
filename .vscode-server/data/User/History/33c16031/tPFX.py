from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from database import benh_nhan
from database.bac_si import get_all_bac_si, get_bac_si_by_id, search_bac_si, create_bac_si, update_bac_si, delete_bac_si
from database.phieu_kham import get_all_phieu_kham, get_phieu_kham_by_id, search_phieu_kham, create_phieu_kham, update_phieu_kham, delete_phieu_kham
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
def bac_si_page():
    doctors_list = get_all_bac_si()
    return render_template('bac_si.html', bac_si_list=doctors_list)

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

# Route bác sĩ đã được định nghĩa ở trên

# Thêm mới bác sĩ
@app.route('/bac-si/them-moi', methods=['GET', 'POST'])
def them_moi_bac_si():
    if request.method == 'POST':
        # Xử lý dữ liệu form khi submit
        ma_bac_si = request.form.get('ma_bac_si')
        ho_ten = request.form.get('ho_ten')
        so_dien_thoai = request.form.get('so_dien_thoai')
        
        # Kiểm tra dữ liệu đầu vào
        if not ma_bac_si or not ho_ten or not so_dien_thoai:
            flash('Vui lòng điền đầy đủ thông tin bắt buộc', 'error')
        else:
            # Lưu vào database
            ma_bs, result = create_bac_si(
                ho_ten,
                so_dien_thoai,
                ma_bac_si
            )
            
            if result:
                flash(f'Thêm bác sĩ thành công với mã {ma_bs}!', 'success')
                return redirect(url_for('bac_si_page'))
            else:
                flash('Có lỗi xảy ra khi thêm bác sĩ', 'error')
                    
    # GET request - hiển thị form với mã bác sĩ mới
    ma_bac_si = get_next_bac_si_id()
    return render_template('them_moi_bac_si.html', ma_bac_si=ma_bac_si)

# Tìm kiếm bác sĩ
@app.route('/bac-si/tim-kiem', methods=['GET', 'POST'])
def tim_kiem_bac_si():
    # Dữ liệu mẫu cho kết quả tìm kiếm
    ket_qua = []

    if request.method == 'POST':
        tu_khoa = request.form.get('tu_khoa')
        loai_tim_kiem = request.form.get('loai_tim_kiem', 'ma_bac_si')
        
        if tu_khoa:
            ket_qua = search_bac_si(tu_khoa, loai_tim_kiem)
            
    return render_template('tim_kiem_bac_si.html', ket_qua=ket_qua)

# Chi tiết bác sĩ
@app.route('/bac-si/chi-tiet/<ma_bs>')
def chi_tiet_bac_si(ma_bs):
    bs = get_bac_si_by_id(ma_bs)
    if not bs:
        flash('Không tìm thấy bác sĩ', 'error')
        return redirect(url_for('bac_si_page'))
    return render_template('chi_tiet_bac_si.html', bac_si=bs)

# Chỉnh sửa bác sĩ
@app.route('/bac-si/chinh-sua/<ma_bs>', methods=['GET', 'POST'])
def chinh_sua_bac_si(ma_bs):
    bs = get_bac_si_by_id(ma_bs)
    if not bs:
        flash('Không tìm thấy bác sĩ', 'error')
        return redirect(url_for('bac_si_page'))
        
    if request.method == 'POST':
        ho_ten = request.form.get('ho_ten')
        so_dien_thoai = request.form.get('so_dien_thoai')
        
        if not ho_ten or not so_dien_thoai:
            flash('Vui lòng điền đầy đủ thông tin bắt buộc', 'error')
        else:
            result = update_bac_si(ma_bs, ho_ten, so_dien_thoai)
            if result:
                flash('Cập nhật thông tin bác sĩ thành công!', 'success')
                return redirect(url_for('chi_tiet_bac_si', ma_bs=ma_bs))
            else:
                flash('Có lỗi xảy ra khi cập nhật thông tin bác sĩ', 'error')
    
    return render_template('chinh_sua_bac_si.html', bac_si=bs)

# API xóa bác sĩ
@app.route('/api/bac-si/<ma_bs>', methods=['DELETE'])
def api_delete_bac_si(ma_bs):
    try:
        delete_bac_si(ma_bs)
        return jsonify({"success": True, "message": "Xóa bác sĩ thành công"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/bac-si/ma-moi', methods=['GET'])
def api_get_ma_bac_si_moi():
    # Lấy mã bác sĩ mới nhất và tăng lên 1
    new_id = get_next_bac_si_id()
    return jsonify({"ma_bac_si": new_id})

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

# Quản lý phiếu khám
@app.route('/phieu-kham')
def phieu_kham_list():
    phieu_kham_list = get_all_phieu_kham()
    return render_template('phieu_kham.html', phieu_kham_list=phieu_kham_list)

# Thêm mới phiếu khám
@app.route('/phieu-kham/them-moi', methods=['GET', 'POST'])
def them_moi_phieu_kham():
    if request.method == 'POST':
        # Xử lý dữ liệu form khi submit
        ma_phieu_kham = request.form.get('ma_phieu_kham')
        ma_benh_nhan = request.form.get('ma_benh_nhan')
        ma_bac_si = request.form.get('ma_bac_si')
        ma_dich_vu = request.form.get('ma_dich_vu')
        chan_doan = request.form.get('chan_doan')
        ghi_chu = request.form.get('ghi_chu')
        ngay_kham = request.form.get('ngay_kham')
        
        # Kiểm tra dữ liệu đầu vào
        if not ma_benh_nhan or not ma_bac_si or not ma_dich_vu:
            flash('Vui lòng điền đầy đủ thông tin bắt buộc', 'error')
        else:
            # Lưu vào database
            ma_pk, result = create_phieu_kham(
                ma_benh_nhan,
                ma_bac_si,
                ma_dich_vu,
                chan_doan,
                ghi_chu,
                ma_phieu_kham,
                ngay_kham
            )
            
            if result:
                flash(f'Thêm phiếu khám thành công với mã {ma_pk}!', 'success')
                return redirect(url_for('phieu_kham_list'))
            else:
                flash('Có lỗi xảy ra khi thêm phiếu khám', 'error')
                    
    # GET request - hiển thị form với mã phiếu khám mới
    ma_phieu_kham = get_next_phieu_kham_id()
    benh_nhan_list = benh_nhan.get_all_benh_nhan()
    bac_si_list = get_all_bac_si()
    
    # Lấy danh sách dịch vụ
    from database.db import execute_query
    dich_vu_list = execute_query("SELECT * FROM DICHVU", fetch=True)
    
    return render_template('them_moi_phieu_kham.html', 
                          ma_phieu_kham=ma_phieu_kham,
                          benh_nhan_list=benh_nhan_list,
                          bac_si_list=bac_si_list,
                          dich_vu_list=dich_vu_list)

# Tìm kiếm phiếu khám
@app.route('/phieu-kham/tim-kiem', methods=['GET', 'POST'])
def tim_kiem_phieu_kham():
    # Dữ liệu mẫu cho kết quả tìm kiếm
    ket_qua = []

    if request.method == 'POST':
        tu_khoa = request.form.get('tu_khoa')
        loai_tim_kiem = request.form.get('loai_tim_kiem', 'ma_phieu_kham')
        
        if tu_khoa:
            ket_qua = search_phieu_kham(tu_khoa, loai_tim_kiem)
            
    return render_template('tim_kiem_phieu_kham.html', ket_qua=ket_qua)

# Chi tiết phiếu khám
@app.route('/phieu-kham/chi-tiet/<ma_pk>')
def chi_tiet_phieu_kham(ma_pk):
    pk = get_phieu_kham_by_id(ma_pk)
    if not pk:
        flash('Không tìm thấy phiếu khám', 'error')
        return redirect(url_for('phieu_kham_list'))
    return render_template('chi_tiet_phieu_kham.html', phieu_kham=pk)

# Chỉnh sửa phiếu khám
@app.route('/phieu-kham/chinh-sua/<ma_pk>', methods=['GET', 'POST'])
def chinh_sua_phieu_kham(ma_pk):
    # Lấy thông tin phiếu khám
    pk = get_phieu_kham_by_id(ma_pk)
    if not pk:
        flash('Không tìm thấy phiếu khám', 'error')
        return redirect(url_for('phieu_kham_list'))
    
    if request.method == 'POST':
        # Xử lý dữ liệu form khi submit
        ma_benh_nhan = request.form.get('ma_benh_nhan')
        ma_bac_si = request.form.get('ma_bac_si')
        ma_dich_vu = request.form.get('ma_dich_vu')
        chan_doan = request.form.get('chan_doan')
        ghi_chu = request.form.get('ghi_chu')
        ngay_kham = request.form.get('ngay_kham')
        
        # Kiểm tra dữ liệu đầu vào
        if not ma_benh_nhan or not ma_bac_si or not ma_dich_vu:
            flash('Vui lòng điền đầy đủ thông tin bắt buộc', 'error')
        else:
            # Cập nhật vào database
            result = update_phieu_kham(
                ma_pk,
                ma_benh_nhan,
                ma_bac_si,
                ma_dich_vu,
                chan_doan,
                ghi_chu,
                ngay_kham
            )
            
            if result:
                flash('Cập nhật phiếu khám thành công!', 'success')
                return redirect(url_for('chi_tiet_phieu_kham', ma_pk=ma_pk))
            else:
                flash('Có lỗi xảy ra khi cập nhật phiếu khám', 'error')
    
    # Lấy danh sách bệnh nhân, bác sĩ và dịch vụ
    benh_nhan_list = benh_nhan.get_all_benh_nhan()
    bac_si_list = get_all_bac_si()
    
    # Lấy danh sách dịch vụ
    from database.db import execute_query
    dich_vu_list = execute_query("SELECT * FROM DICHVU", fetch=True)
    
    return render_template('chinh_sua_phieu_kham.html', 
                          phieu_kham=pk,
                          benh_nhan_list=benh_nhan_list,
                          bac_si_list=bac_si_list,
                          dich_vu_list=dich_vu_list)

# API xóa phiếu khám
@app.route('/api/phieu-kham/<ma_pk>', methods=['DELETE'])
def api_delete_phieu_kham(ma_pk):
    try:
        result = delete_phieu_kham(ma_pk)
        if not result:
            return jsonify({"success": False, "message": "Không tìm thấy phiếu khám hoặc có lỗi xảy ra"}), 404
        return jsonify({"success": True, "message": "Xóa phiếu khám thành công"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)