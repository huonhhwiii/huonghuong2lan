from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Cấu hình MySQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'benhnhan_db')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key')

mysql = MySQL(app)

# Tạo bảng bệnh nhân nếu chưa tồn tại
def create_table():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS benh_nhan (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ma_benh_nhan VARCHAR(20) NOT NULL UNIQUE,
                ho_ten VARCHAR(100) NOT NULL,
                ngay_sinh DATE,
                gioi_tinh VARCHAR(10),
                so_dien_thoai VARCHAR(15) NOT NULL,
                dia_chi TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        mysql.connection.commit()
        cur.close()

create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/them-moi-benh-nhan', methods=['GET', 'POST'])
def them_moi_benh_nhan():
    if request.method == 'POST':
        ma_benh_nhan = request.form['ma_benh_nhan']
        ho_ten = request.form['ho_ten']
        ngay_sinh = request.form['ngay_sinh']
        gioi_tinh = request.form['gioi_tinh']
        so_dien_thoai = request.form['so_dien_thoai']
        dia_chi = request.form['dia_chi']
        
        try:
            cur = mysql.connection.cursor()
            cur.execute('''
                INSERT INTO benh_nhan (ma_benh_nhan, ho_ten, ngay_sinh, gioi_tinh, so_dien_thoai, dia_chi)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (ma_benh_nhan, ho_ten, ngay_sinh, gioi_tinh, so_dien_thoai, dia_chi))
            mysql.connection.commit()
            cur.close()
            flash('Thêm bệnh nhân thành công!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Lỗi khi thêm bệnh nhân: {str(e)}', 'danger')
    
    return render_template('them_moi_benh_nhan.html')

if __name__ == '__main__':
    app.run(debug=True)