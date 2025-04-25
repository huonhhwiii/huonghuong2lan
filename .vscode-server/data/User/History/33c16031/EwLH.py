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