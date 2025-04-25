from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from database import benh_nhan
from database.bac_si import get_all_bac_si, get_bac_si_by_id, search_bac_si, create_bac_si, update_bac_si, delete_bac_si
from database.phieu_kham import get_all_phieu_kham, get_phieu_kham_by_id, search_phieu_kham, create_phieu_kham, update_phieu_kham, delete_phieu_kham
from database.lich_hen import get_all_lich_hen, get_lich_hen_by_id, search_lich_hen, create_lich_hen, update_lich_hen, delete_lich_hen
from database.dich_vu import get_all_dich_vu, get_dich_vu_by_id, search_dich_vu, create_dich_vu, update_dich_vu, delete_dich_vu
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
def bac_si_list():
    try:
        bac_si_list = get_all_bac_si()
        return render_template('bac_si.html', bac_si_list=bac_si_list)
    except Exception as e:
        flash(f'Lỗi khi tải danh sách bác sĩ: {str(e)}', 'error')
        return render_template('bac_si.html', bac_si_list=[])

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
                return redirect(url_for('bac_si_list'))
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
            try:
                ket_qua = search_bac_si(tu_khoa, loai_tim_kiem)
                if not ket_qua:
                    flash(f'Không tìm thấy bác sĩ nào phù hợp với từ khóa "{tu_khoa}"', 'info')
            except Exception as e:
                flash(f'Lỗi khi tìm kiếm bác sĩ: {str(e)}', 'error')
            
    return render_template('tim_kiem_bac_si.html', ket_qua=ket_qua)

# Chi tiết bác sĩ
@app.route('/bac-si/chi-tiet/<ma_bs>')
def chi_tiet_bac_si(ma_bs):
    bs = get_bac_si_by_id(ma_bs)
    if not bs:
        flash('Không tìm thấy bác sĩ', 'error')
        return redirect(url_for('bac_si_list'))
    return render_template('chi_tiet_bac_si.html', bac_si=bs)

# Chỉnh sửa bác sĩ
@app.route('/bac-si/chinh-sua/<ma_bs>', methods=['GET', 'POST'])
def chinh_sua_bac_si(ma_bs):
    bs = get_bac_si_by_id(ma_bs)
    if not bs:
        flash('Không tìm thấy bác sĩ', 'error')
        return redirect(url_for('bac_si_list'))
        
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

# Quản lý phiếu khám
@app.route('/phieu-kham')
def phieu_kham_list():
    try:
        phieu_kham_list = get_all_phieu_kham()
        return render_template('phieu_kham.html', phieu_kham_list=phieu_kham_list)
    except Exception as e:
        flash(f'Lỗi khi tải danh sách phiếu khám: {str(e)}', 'error')
        return render_template('phieu_kham.html', phieu_kham_list=[])

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
            try:
                ket_qua = search_phieu_kham(tu_khoa, loai_tim_kiem)
                if not ket_qua:
                    flash(f'Không tìm thấy phiếu khám nào phù hợp với từ khóa "{tu_khoa}"', 'info')
            except Exception as e:
                flash(f'Lỗi khi tìm kiếm phiếu khám: {str(e)}', 'error')
            
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

# Quản lý lịch hẹn
@app.route('/lich-hen')
def lich_hen_list():
    lich_hen_list = get_all_lich_hen()
    return render_template('lich_hen.html', lich_hen_list=lich_hen_list)

# Thêm mới lịch hẹn
@app.route('/lich-hen/them-moi', methods=['GET', 'POST'])
def them_moi_lich_hen():
    if request.method == 'POST':
        # Xử lý dữ liệu form khi submit
        ma_lich_hen = request.form.get('ma_lich_hen')
        ma_benh_nhan = request.form.get('ma_benh_nhan')
        ngay_hen = request.form.get('ngay_hen')
        trang_thai = request.form.get('trang_thai', 'Chưa khám')
        
        # Kiểm tra dữ liệu đầu vào
        if not ma_benh_nhan or not ngay_hen:
            flash('Vui lòng điền đầy đủ thông tin bắt buộc', 'error')
        else:
            # Lưu vào database
            ma_lh, result = create_lich_hen(
                ma_benh_nhan,
                ngay_hen,
                trang_thai,
                ma_lich_hen
            )
            
            if result:
                flash(f'Thêm lịch hẹn thành công với mã {ma_lh}!', 'success')
                return redirect(url_for('lich_hen_list'))
            else:
                flash('Có lỗi xảy ra khi thêm lịch hẹn', 'error')
                    
    # GET request - hiển thị form với mã lịch hẹn mới
    ma_lich_hen = get_next_lich_hen_id()
    benh_nhan_list = benh_nhan.get_all_benh_nhan()
    
    return render_template('them_moi_lich_hen.html', 
                          ma_lich_hen=ma_lich_hen,
                          benh_nhan_list=benh_nhan_list)

# Tìm kiếm lịch hẹn
@app.route('/lich-hen/tim-kiem', methods=['GET', 'POST'])
def tim_kiem_lich_hen():
    # Dữ liệu mẫu cho kết quả tìm kiếm
    ket_qua = []

    if request.method == 'POST':
        tu_khoa = request.form.get('tu_khoa')
        loai_tim_kiem = request.form.get('loai_tim_kiem', 'ma_lich_hen')
        
        if tu_khoa:
            ket_qua = search_lich_hen(tu_khoa, loai_tim_kiem)
            
    return render_template('tim_kiem_lich_hen.html', ket_qua=ket_qua)

# Chi tiết lịch hẹn
@app.route('/lich-hen/chi-tiet/<ma_lh>')
def chi_tiet_lich_hen(ma_lh):
    lh = get_lich_hen_by_id(ma_lh)
    if not lh:
        flash('Không tìm thấy lịch hẹn', 'error')
        return redirect(url_for('lich_hen_list'))
    return render_template('chi_tiet_lich_hen.html', lich_hen=lh)

# Chỉnh sửa lịch hẹn
@app.route('/lich-hen/chinh-sua/<ma_lh>', methods=['GET', 'POST'])
def chinh_sua_lich_hen(ma_lh):
    # Lấy thông tin lịch hẹn
    lh = get_lich_hen_by_id(ma_lh)
    if not lh:
        flash('Không tìm thấy lịch hẹn', 'error')
        return redirect(url_for('lich_hen_list'))
    
    if request.method == 'POST':
        # Xử lý dữ liệu form khi submit
        ma_benh_nhan = request.form.get('ma_benh_nhan')
        ngay_hen = request.form.get('ngay_hen')
        trang_thai = request.form.get('trang_thai')
        
        # Kiểm tra dữ liệu đầu vào
        if not ma_benh_nhan or not ngay_hen:
            flash('Vui lòng điền đầy đủ thông tin bắt buộc', 'error')
        else:
            # Cập nhật vào database
            result = update_lich_hen(
                ma_lh,
                ma_benh_nhan,
                ngay_hen,
                trang_thai
            )
            
            if result:
                flash('Cập nhật lịch hẹn thành công!', 'success')
                return redirect(url_for('chi_tiet_lich_hen', ma_lh=ma_lh))
            else:
                flash('Có lỗi xảy ra khi cập nhật lịch hẹn', 'error')
    
    # Lấy danh sách bệnh nhân
    benh_nhan_list = benh_nhan.get_all_benh_nhan()
    
    return render_template('chinh_sua_lich_hen.html', 
                          lich_hen=lh,
                          benh_nhan_list=benh_nhan_list)

# Quản lý dịch vụ
@app.route('/dich-vu')
def dich_vu_list():
    dich_vu_list = get_all_dich_vu()
    return render_template('dich_vu.html', dich_vu_list=dich_vu_list)

# Thêm mới dịch vụ
@app.route('/dich-vu/them-moi', methods=['GET', 'POST'])
def them_moi_dich_vu():
    if request.method == 'POST':
        # Xử lý dữ liệu form khi submit
        ma_dv = request.form.get('ma_dv')
        ten_dv = request.form.get('ten_dv')
        gia = request.form.get('gia')
        
        # Kiểm tra dữ liệu đầu vào
        if not ten_dv:
            flash('Vui lòng điền đầy đủ tên dịch vụ', 'error')
        else:
            # Lưu vào database
            ma_dv, result = create_dich_vu(
                ten_dv,
                gia,
                ma_dv
            )
            
            if result:
                flash(f'Thêm dịch vụ thành công với mã {ma_dv}!', 'success')
                return redirect(url_for('dich_vu_list'))
            else:
                flash('Có lỗi xảy ra khi thêm dịch vụ', 'error')
                    
    # GET request - hiển thị form với mã dịch vụ mới
    ma_dv = get_next_dich_vu_id()
    
    return render_template('them_moi_dich_vu.html', ma_dv=ma_dv)

# Tìm kiếm dịch vụ
@app.route('/dich-vu/tim-kiem', methods=['GET', 'POST'])
def tim_kiem_dich_vu():
    # Dữ liệu mẫu cho kết quả tìm kiếm
    ket_qua = []

    if request.method == 'POST':
        tu_khoa = request.form.get('tu_khoa')
        loai_tim_kiem = request.form.get('loai_tim_kiem', 'ma_dv')
        
        if tu_khoa:
            ket_qua = search_dich_vu(tu_khoa, loai_tim_kiem)
            
    return render_template('tim_kiem_dich_vu.html', ket_qua=ket_qua)

# Chi tiết dịch vụ
@app.route('/dich-vu/chi-tiet/<ma_dv>')
def chi_tiet_dich_vu(ma_dv):
    dv = get_dich_vu_by_id(ma_dv)
    if not dv:
        flash('Không tìm thấy dịch vụ', 'error')
        return redirect(url_for('dich_vu_list'))
    return render_template('chi_tiet_dich_vu.html', dich_vu=dv)

# Chỉnh sửa dịch vụ
@app.route('/dich-vu/chinh-sua/<ma_dv>', methods=['GET', 'POST'])
def chinh_sua_dich_vu(ma_dv):
    # Lấy thông tin dịch vụ
    dv = get_dich_vu_by_id(ma_dv)
    if not dv:
        flash('Không tìm thấy dịch vụ', 'error')
        return redirect(url_for('dich_vu_list'))
    
    if request.method == 'POST':
        # Xử lý dữ liệu form khi submit
        ten_dv = request.form.get('ten_dv')
        gia = request.form.get('gia')
        
        # Kiểm tra dữ liệu đầu vào
        if not ten_dv:
            flash('Vui lòng điền đầy đủ tên dịch vụ', 'error')
        else:
            # Cập nhật vào database
            result = update_dich_vu(
                ma_dv,
                ten_dv,
                gia
            )
            
            if result:
                flash('Cập nhật dịch vụ thành công!', 'success')
                return redirect(url_for('chi_tiet_dich_vu', ma_dv=ma_dv))
            else:
                flash('Có lỗi xảy ra khi cập nhật dịch vụ', 'error')
    
    return render_template('chinh_sua_dich_vu.html', dich_vu=dv)

# Chức năng thanh toán đã bị xóa

# Báo cáo và thống kê
@app.route('/bao-cao')
def bao_cao():
    # Lấy thống kê tổng quan
    tong_benh_nhan = len(benh_nhan.get_all_benh_nhan())
    tong_dich_vu = len(get_all_dich_vu())
    tong_lich_hen = len(get_all_lich_hen())
    
    # Dữ liệu mẫu cho biểu đồ
    dich_vu_labels = []
    dich_vu_data = []
    benh_nhan_labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12']
    benh_nhan_data = [10, 15, 8, 12, 20, 18, 25, 22, 30, 28, 35, 40]
    doanh_thu_labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12']
    doanh_thu_data = [5000000, 7500000, 4000000, 6000000, 10000000, 9000000, 12500000, 11000000, 15000000, 14000000, 17500000, 20000000]
    
    # Lấy dữ liệu dịch vụ
    dich_vu_list = get_all_dich_vu()
    for dv in dich_vu_list:
        dich_vu_labels.append(dv['TenDV'])
        dich_vu_data.append(20)  # Giả lập số lượng
    
    # Tổng doanh thu
    tong_doanh_thu = sum(doanh_thu_data)
    
    return render_template('bao_cao.html', 
                          tong_benh_nhan=tong_benh_nhan,
                          tong_dich_vu=tong_dich_vu,
                          tong_lich_hen=tong_lich_hen,
                          tong_doanh_thu=tong_doanh_thu,
                          dich_vu_labels=dich_vu_labels,
                          dich_vu_data=dich_vu_data,
                          benh_nhan_labels=benh_nhan_labels,
                          benh_nhan_data=benh_nhan_data,
                          doanh_thu_labels=doanh_thu_labels,
                          doanh_thu_data=doanh_thu_data)

# Báo cáo dịch vụ
@app.route('/bao-cao/dich-vu', methods=['GET', 'POST'])
def bao_cao_dich_vu():
    # Lấy dữ liệu từ form
    tu_ngay = request.form.get('tu_ngay', datetime.datetime.now().replace(day=1).strftime('%Y-%m-%d'))
    den_ngay = request.form.get('den_ngay', datetime.datetime.now().strftime('%Y-%m-%d'))
    loai_bao_cao = request.form.get('loai_bao_cao', 'all')
    
    # Dữ liệu mẫu cho báo cáo
    tong_dich_vu = 150
    dich_vu_moi = 30
    dich_vu_pho_bien = 120
    ty_le_su_dung = 80.0
    
    # Dữ liệu mẫu cho biểu đồ
    dich_vu_labels = []
    dich_vu_data = []
    
    # Lấy dữ liệu dịch vụ
    dich_vu_list = get_all_dich_vu()
    for dv in dich_vu_list:
        dich_vu_labels.append(dv['TenDV'])
        dich_vu_data.append(20)  # Giả lập số lượng
    
    # Dữ liệu mẫu cho bảng
    dich_vu_theo_thoi_gian = [
        {'ThoiGian': 'T1/2023', 'TongSo': 10, 'DichVuMoi': 2, 'DichVuPho': 8, 'TyLeSuDung': 80.0},
        {'ThoiGian': 'T2/2023', 'TongSo': 15, 'DichVuMoi': 3, 'DichVuPho': 12, 'TyLeSuDung': 80.0},
        {'ThoiGian': 'T3/2023', 'TongSo': 12, 'DichVuMoi': 2, 'DichVuPho': 10, 'TyLeSuDung': 83.3},
        {'ThoiGian': 'T4/2023', 'TongSo': 18, 'DichVuMoi': 4, 'DichVuPho': 14, 'TyLeSuDung': 77.8},
        {'ThoiGian': 'T5/2023', 'TongSo': 20, 'DichVuMoi': 5, 'DichVuPho': 15, 'TyLeSuDung': 75.0},
        {'ThoiGian': 'T6/2023', 'TongSo': 25, 'DichVuMoi': 5, 'DichVuPho': 20, 'TyLeSuDung': 80.0},
    ]
    
    # Dữ liệu cho biểu đồ xu hướng
    thoi_gian_labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
    tong_so_data = [10, 15, 12, 18, 20, 25]
    dich_vu_moi_data = [2, 3, 2, 4, 5, 5]
    dich_vu_pho_bien_data = [8, 12, 10, 14, 15, 20]
    
    # Dữ liệu cho biểu đồ giá
    gia_labels = ['<500k', '500k-1M', '1M-2M', '2M-5M', '>5M']
    gia_data = [10, 25, 40, 15, 10]
    
    return render_template('bao_cao_dich_vu.html',
                          tu_ngay=tu_ngay,
                          den_ngay=den_ngay,
                          loai_bao_cao=loai_bao_cao,
                          tong_dich_vu=tong_dich_vu,
                          dich_vu_moi=dich_vu_moi,
                          dich_vu_pho_bien=dich_vu_pho_bien,
                          ty_le_su_dung=ty_le_su_dung,
                          dich_vu_labels=json.dumps(dich_vu_labels),
                          dich_vu_data=json.dumps(dich_vu_data),
                          dich_vu_theo_thoi_gian=dich_vu_theo_thoi_gian,
                          thoi_gian_labels=json.dumps(thoi_gian_labels),
                          tong_so_data=json.dumps(tong_so_data),
                          dich_vu_moi_data=json.dumps(dich_vu_moi_data),
                          dich_vu_pho_bien_data=json.dumps(dich_vu_pho_bien_data),
                          gia_labels=json.dumps(gia_labels),
                          gia_data=json.dumps(gia_data))

# Báo cáo bệnh nhân
@app.route('/bao-cao/benh-nhan', methods=['GET', 'POST'])
def bao_cao_benh_nhan():
    # Lấy dữ liệu từ form
    tu_ngay = request.form.get('tu_ngay', datetime.datetime.now().replace(day=1).strftime('%Y-%m-%d'))
    den_ngay = request.form.get('den_ngay', datetime.datetime.now().strftime('%Y-%m-%d'))
    loai_bao_cao = request.form.get('loai_bao_cao', 'all')
    
    # Dữ liệu mẫu cho báo cáo
    tong_benh_nhan = 200
    benh_nhan_moi = 50
    benh_nhan_quay_lai = 150
    ty_le_quay_lai = 75.0
    
    # Dữ liệu mẫu cho bảng
    benh_nhan_theo_thoi_gian = [
        {'ThoiGian': 'T1/2023', 'TongSo': 20, 'BenhNhanMoi': 5, 'BenhNhanQuayLai': 15, 'TyLeQuayLai': 75.0},
        {'ThoiGian': 'T2/2023', 'TongSo': 25, 'BenhNhanMoi': 8, 'BenhNhanQuayLai': 17, 'TyLeQuayLai': 68.0},
        {'ThoiGian': 'T3/2023', 'TongSo': 30, 'BenhNhanMoi': 10, 'BenhNhanQuayLai': 20, 'TyLeQuayLai': 66.7},
        {'ThoiGian': 'T4/2023', 'TongSo': 35, 'BenhNhanMoi': 7, 'BenhNhanQuayLai': 28, 'TyLeQuayLai': 80.0},
        {'ThoiGian': 'T5/2023', 'TongSo': 40, 'BenhNhanMoi': 10, 'BenhNhanQuayLai': 30, 'TyLeQuayLai': 75.0},
        {'ThoiGian': 'T6/2023', 'TongSo': 50, 'BenhNhanMoi': 10, 'BenhNhanQuayLai': 40, 'TyLeQuayLai': 80.0},
    ]
    
    # Dữ liệu cho biểu đồ xu hướng
    thoi_gian_labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
    tong_so_data = [20, 25, 30, 35, 40, 50]
    benh_nhan_moi_data = [5, 8, 10, 7, 10, 10]
    benh_nhan_quay_lai_data = [15, 17, 20, 28, 30, 40]
    
    # Dữ liệu cho biểu đồ phân bố theo độ tuổi
    benh_nhan_theo_tuoi = [
        {'NhomTuoi': '<18', 'SoLuong': 20, 'TyLe': 10.0},
        {'NhomTuoi': '18-30', 'SoLuong': 40, 'TyLe': 20.0},
        {'NhomTuoi': '31-45', 'SoLuong': 60, 'TyLe': 30.0},
        {'NhomTuoi': '46-60', 'SoLuong': 50, 'TyLe': 25.0},
        {'NhomTuoi': '>60', 'SoLuong': 30, 'TyLe': 15.0},
    ]
    
    nhom_tuoi_labels = ['<18', '18-30', '31-45', '46-60', '>60']
    nhom_tuoi_data = [20, 40, 60, 50, 30]
    
    # Dữ liệu cho biểu đồ phân bố theo giới tính
    benh_nhan_theo_gioi_tinh = [
        {'GioiTinh': 'Nam', 'SoLuong': 90, 'TyLe': 45.0},
        {'GioiTinh': 'Nữ', 'SoLuong': 110, 'TyLe': 55.0},
    ]
    
    gioi_tinh_labels = ['Nam', 'Nữ']
    gioi_tinh_data = [90, 110]
    
    return render_template('bao_cao_benh_nhan.html',
                          tu_ngay=tu_ngay,
                          den_ngay=den_ngay,
                          loai_bao_cao=loai_bao_cao,
                          tong_benh_nhan=tong_benh_nhan,
                          benh_nhan_moi=benh_nhan_moi,
                          benh_nhan_quay_lai=benh_nhan_quay_lai,
                          ty_le_quay_lai=ty_le_quay_lai,
                          benh_nhan_theo_thoi_gian=benh_nhan_theo_thoi_gian,
                          thoi_gian_labels=json.dumps(thoi_gian_labels),
                          tong_so_data=json.dumps(tong_so_data),
                          benh_nhan_moi_data=json.dumps(benh_nhan_moi_data),
                          benh_nhan_quay_lai_data=json.dumps(benh_nhan_quay_lai_data),
                          benh_nhan_theo_tuoi=benh_nhan_theo_tuoi,
                          nhom_tuoi_labels=json.dumps(nhom_tuoi_labels),
                          nhom_tuoi_data=json.dumps(nhom_tuoi_data),
                          benh_nhan_theo_gioi_tinh=benh_nhan_theo_gioi_tinh,
                          gioi_tinh_labels=json.dumps(gioi_tinh_labels),
                          gioi_tinh_data=json.dumps(gioi_tinh_data))

# Báo cáo doanh thu
@app.route('/bao-cao/doanh-thu', methods=['GET', 'POST'])
def bao_cao_doanh_thu():
    # Lấy dữ liệu từ form
    tu_ngay = request.form.get('tu_ngay', datetime.datetime.now().replace(day=1).strftime('%Y-%m-%d'))
    den_ngay = request.form.get('den_ngay', datetime.datetime.now().strftime('%Y-%m-%d'))
    loai_bao_cao = request.form.get('loai_bao_cao', 'all')
    
    # Dữ liệu mẫu cho báo cáo
    tong_doanh_thu = 150000000
    doanh_thu_trung_binh_ngay = 5000000
    doanh_thu_trung_binh_thang = 150000000
    # so_hoa_don đã bị xóa vì liên quan đến chức năng thanh toán
    
    # Dữ liệu mẫu cho bảng
    doanh_thu_theo_thoi_gian = [
        {'ThoiGian': 'T1/2023', 'DoanhThu': 20000000, 'SoLuong': 40, 'TyLe': 13.33},
        {'ThoiGian': 'T2/2023', 'DoanhThu': 25000000, 'SoLuong': 50, 'TyLe': 16.67},
        {'ThoiGian': 'T3/2023', 'DoanhThu': 22000000, 'SoLuong': 45, 'TyLe': 14.67},
        {'ThoiGian': 'T4/2023', 'DoanhThu': 28000000, 'SoLuong': 55, 'TyLe': 18.67},
        {'ThoiGian': 'T5/2023', 'DoanhThu': 30000000, 'SoLuong': 60, 'TyLe': 20.00},
        {'ThoiGian': 'T6/2023', 'DoanhThu': 25000000, 'SoLuong': 50, 'TyLe': 16.67},
    ]
    
    # Dữ liệu cho biểu đồ xu hướng
    thoi_gian_labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
    doanh_thu_data = [20000000, 25000000, 22000000, 28000000, 30000000, 25000000]
    # so_hoa_don_data đã bị xóa vì liên quan đến chức năng thanh toán
    
    # Dữ liệu cho biểu đồ doanh thu theo dịch vụ
    dich_vu_labels = ['Khám răng định kỳ', 'Nhổ răng khôn', 'Tẩy trắng răng', 'Trám răng thẩm mỹ', 'Niềng răng chỉnh nha']
    dich_vu_data = [15000000, 25000000, 35000000, 30000000, 45000000]
    
    # Dữ liệu cho biểu đồ doanh thu theo bác sĩ
    bac_si_labels = ['BS. Nguyễn Văn An', 'BS. Trần Thị Bình', 'BS. Lê Văn Cường', 'BS. Phạm Thị Dung', 'BS. Đỗ Văn Hải']
    bac_si_data = [30000000, 35000000, 25000000, 40000000, 20000000]
    
    # Dữ liệu doanh thu theo bác sĩ
    doanh_thu_theo_bac_si = [
        {'MaBS': 'BS00000001', 'TenBS': 'Nguyễn Văn An', 'SoLuong': 60, 'DoanhThu': 30000000, 'TyLe': 20.00},
        {'MaBS': 'BS00000002', 'TenBS': 'Trần Thị Bình', 'SoLuong': 70, 'DoanhThu': 35000000, 'TyLe': 23.33},
        {'MaBS': 'BS00000003', 'TenBS': 'Lê Văn Cường', 'SoLuong': 50, 'DoanhThu': 25000000, 'TyLe': 16.67},
        {'MaBS': 'BS00000004', 'TenBS': 'Phạm Thị Dung', 'SoLuong': 80, 'DoanhThu': 40000000, 'TyLe': 26.67},
        {'MaBS': 'BS00000005', 'TenBS': 'Đỗ Văn Hải', 'SoLuong': 40, 'DoanhThu': 20000000, 'TyLe': 13.33},
    ]
    
    # Dữ liệu doanh thu theo dịch vụ
    doanh_thu_theo_dich_vu = [
        {'MaDV': 'DV00000001', 'TenDV': 'Khám răng định kỳ', 'SoLuong': 100, 'DoanhThu': 15000000, 'TyLe': 10.00},
        {'MaDV': 'DV00000002', 'TenDV': 'Nhổ răng khôn', 'SoLuong': 50, 'DoanhThu': 25000000, 'TyLe': 16.67},
        {'MaDV': 'DV00000003', 'TenDV': 'Tẩy trắng răng', 'SoLuong': 50, 'DoanhThu': 35000000, 'TyLe': 23.33},
        {'MaDV': 'DV00000004', 'TenDV': 'Trám răng thẩm mỹ', 'SoLuong': 100, 'DoanhThu': 30000000, 'TyLe': 20.00},
        {'MaDV': 'DV00000005', 'TenDV': 'Niềng răng chỉnh nha', 'SoLuong': 18, 'DoanhThu': 45000000, 'TyLe': 30.00},
    ]
    
    # Tổng số lượng dịch vụ
    tong_dich_vu = 300
    tong_so_luong_dich_vu = 318
    
    return render_template('bao_cao_doanh_thu.html',
                          tu_ngay=tu_ngay,
                          den_ngay=den_ngay,
                          loai_bao_cao=loai_bao_cao,
                          tong_doanh_thu=tong_doanh_thu,
                          doanh_thu_trung_binh_ngay=doanh_thu_trung_binh_ngay,
                          doanh_thu_trung_binh_thang=doanh_thu_trung_binh_thang,
                          doanh_thu_trung_binh=doanh_thu_trung_binh_ngay,
                          doanh_thu_cao_nhat=30000000,
                          tong_dich_vu=tong_dich_vu,
                          tong_so_luong_dich_vu=tong_so_luong_dich_vu,
                          doanh_thu_theo_thoi_gian=doanh_thu_theo_thoi_gian,
                          doanh_thu_theo_bac_si=doanh_thu_theo_bac_si,
                          doanh_thu_theo_dich_vu=doanh_thu_theo_dich_vu,
                          thoi_gian_labels=json.dumps(thoi_gian_labels),
                          doanh_thu_data=json.dumps(doanh_thu_data),
                          dich_vu_labels=json.dumps(dich_vu_labels),
                          dich_vu_data=json.dumps(dich_vu_data),
                          bac_si_labels=json.dumps(bac_si_labels),
                          bac_si_data=json.dumps(bac_si_data),
                          pttt_labels=json.dumps(['Tiền mặt', 'Thẻ ngân hàng', 'Chuyển khoản', 'Ví điện tử']),
                          pttt_data=json.dumps([60000000, 40000000, 30000000, 20000000]))

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

# API xóa bác sĩ
@app.route('/api/bac-si/<ma_bs>', methods=['DELETE'])
def api_delete_bac_si(ma_bs):
    try:
        # Kiểm tra xem bác sĩ có tồn tại không
        bac_si = get_bac_si_by_id(ma_bs)
        if not bac_si:
            return jsonify({"success": False, "message": "Không tìm thấy bác sĩ"}), 404
            
        # Thực hiện xóa bác sĩ
        delete_bac_si(ma_bs)
        return jsonify({"success": True, "message": "Xóa bác sĩ thành công"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/bac-si/ma-moi', methods=['GET'])
def api_get_ma_bac_si_moi():
    # Lấy mã bác sĩ mới nhất và tăng lên 1
    new_id = get_next_bac_si_id()
    return jsonify({"ma_bac_si": new_id})

# API xóa phiếu khám
@app.route('/api/phieu-kham/<ma_pk>', methods=['DELETE'])
def api_delete_phieu_kham(ma_pk):
    try:
        delete_phieu_kham(ma_pk)
        return jsonify({"success": True, "message": "Xóa phiếu khám thành công"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# API xóa lịch hẹn
@app.route('/api/lich-hen/<ma_lh>', methods=['DELETE'])
def api_delete_lich_hen(ma_lh):
    try:
        delete_lich_hen(ma_lh)
        return jsonify({"success": True, "message": "Xóa lịch hẹn thành công"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# API xóa dịch vụ
@app.route('/api/dich-vu/<ma_dv>', methods=['DELETE'])
def api_delete_dich_vu(ma_dv):
    try:
        delete_dich_vu(ma_dv)
        return jsonify({"success": True, "message": "Xóa dịch vụ thành công"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

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