from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'ql_benh_nhan')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Secret key for flash messages
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

@app.route('/')
def home():
    return render_template('add_patient.html')

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        # Get form data
        ma_bn = request.form['ma_bn']
        ho_ten = request.form['ho_ten']
        ngay_sinh = request.form['ngay_sinh']
        gioi_tinh = request.form['gioi_tinh']
        so_dien_thoai = request.form['so_dien_thoai']
        
        # Validate required fields
        if not ma_bn or not ho_ten or not ngay_sinh or not so_dien_thoai:
            flash('Vui lòng điền đầy đủ các trường bắt buộc (*)', 'error')
            return redirect(url_for('add_patient'))
        
        try:
            # Insert into database
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO benh_nhan (ma_bn, ho_ten, ngay_sinh, gioi_tinh, so_dien_thoai) VALUES (%s, %s, %s, %s, %s)",
                (ma_bn, ho_ten, ngay_sinh, gioi_tinh, so_dien_thoai)
            )
            mysql.connection.commit()
            cur.close()
            
            flash('Thêm bệnh nhân thành công!', 'success')
            return redirect(url_for('add_patient'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Lỗi khi thêm bệnh nhân: {str(e)}', 'error')
    
    return render_template('add_patient.html')

if __name__ == '__main__':
    app.run(debug=True)