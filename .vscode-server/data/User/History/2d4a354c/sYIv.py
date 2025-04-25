from flask import Flask, render_template,redirect, request

app = Flask(__name__)


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
#Quản lý phụ huynh
@app.route("/them_ph")
def them_ph():
    return render_template("them-moi-phu-huynh.html")

@app.route("/sua_ph")
def sua_ph():
    return render_template("sua-phu-huynh.html")

@app.route("/tim_ph")
def tim_ph():
    return render_template("tim-kiem-phu-huynh.html")

@app.route("/ds_ph")
def ds_ph():
    return render_template("danh-sach-phu-huynh.html")

@app.route("/xoa_ph")
def xoa_ph():
    return render_template("xoa-phu-huynh.html")

#Quản lý gia sư
@app.route("/them_gs")
def them_gs():
    return render_template("them-moi-gia-su.html")

@app.route("/sua_gs")
def sua_gs():
    return render_template("sua-gia-su.html")

@app.route("/tim_gs")
def tim_gs():
    return render_template("tim-kiem-gia-su.html")

@app.route("/ds_gs")
def ds_gs():
    return render_template("danh-sach-gia-su.html")

@app.route("/xoa_gs")
def xoa_gs():
    return render_template("xoa-gia-su.html")

#Quản lý giao dịch
@app.route("/them_gd")
def them_gd():
    return render_template("them-moi-giao-dich.html")

@app.route("/sua_gd")
def sua_gd():
    return render_template("sua-giao-dich.html")

@app.route("/tim_gd")
def tim_gd():
    return render_template("tim-kiem-giao-dich.html")

@app.route("/ds_gd")
def ds_gd():
    return render_template("danh-sach-giao-dich.html")

@app.route("/xoa_gd")
def xoa_gd():
    return render_template("xoa-giao-dich.html")

@app.route("/tk_gd")
def tk_gd():
    return render_template("thong-ke-dich.html")

#Quản lý lớp học
#Quản lý gia sư
@app.route("/them_lh")
def them_lh():
    return render_template("them-moi-lop-hoc.html")

@app.route("/sua_lh")
def sua_lh():
    return render_template("sua-lop-hoc.html")

@app.route("/tim_lh")
def tim_lh():
    return render_template("tim-kiem-lop-hoc.html")

@app.route("/ds_lh")
def ds_lh():
    return render_template("danh-sach-lop-hoc.html")

@app.route("/xoa_lh")
def xoa_lh():
    return render_template("xoa-lop-hoc.html")
