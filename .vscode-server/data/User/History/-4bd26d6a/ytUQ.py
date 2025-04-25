import mysql.connector

connect = mysql.connector.connect(
    host='localhost',
    user='root',
    password='huong24052005',
    database='QuanLyGiaSu'
)

cursor = connect.cursor()

cursor.execute("""
INSERT INTO GIASU (MaGS, HoTen, SoDT, BangCap, MonDay, KinhNghiem) VALUES
('GS00001', 'Nguyễn Văn An', '0981111222', 'SV ĐH Bách Khoa Hà Nội', 'Toán', '2 năm kinh nghiệm dạy Toán cấp 2, giúp học sinh cải thiện tư duy logic'),
('GS00002', 'Trần Thị Bích', '0973333444', 'SV ĐH Ngoại Thương', 'Anh văn', '1.5 năm dạy Anh văn giao tiếp cho học sinh cấp 3, luyện phát âm chuẩn'),
('GS00003', 'Phạm Minh Cường', '0915555666', 'SV ĐH Sư phạm Hà Nội', 'Ngữ văn', '3 năm dạy kèm môn Văn, chuyên ôn thi vào lớp 10'),
('GS00004', 'Lê Thị Dung', '0907777888', 'SV ĐH Y Hà Nội', 'Hóa học', '2 năm dạy Hóa lớp 10-12, có phương pháp ghi nhớ công thức hiệu quả'),
('GS00005', 'Hoàng Văn Đông', '0921111222', 'SV CNTT - ĐH Quốc Gia Hà Nội', 'Tin học', '4 năm kinh nghiệm lập trình Python, từng làm trợ giảng khóa lập trình online'),
('GS00006', 'Đặng Thị Hà', '0933333444', 'SV ĐH Kinh tế Quốc dân', 'Toán', '1 năm dạy kèm Toán cấp 2, giúp học sinh yếu cải thiện điểm số'),
('GS00007', 'Vũ Quang Huy', '0944444555', 'GV Toán - ĐH Sư phạm Hà Nội', 'Toán', '5 năm kinh nghiệm dạy Toán cấp 3, ôn thi đại học'),
('GS00008', 'Nguyễn Mai Linh', '0955555666', 'SV ĐH Hà Nội', 'Anh văn', '2 năm kinh nghiệm dạy IELTS, học sinh đạt 6.5+'),
('GS00009', 'Bùi Mạnh Tiến', '0966666777', 'SV ĐH Xây Dựng', 'Vật lý', '1 năm kinh nghiệm dạy Lý cấp 3, chuyên bài tập thực hành'),
('GS00010', 'Phan Thu Hằng', '0977777888', 'SV ĐH Ngoại Ngữ', 'Anh văn', '2.5 năm dạy Tiếng Anh trẻ em, giúp học sinh phát âm chuẩn hơn'),
('GS00011', 'Tạ Minh Khôi', '0988888999', 'SV ĐH Giao thông Vận tải', 'Toán', '1 năm dạy Toán cấp 2, giúp học sinh cải thiện tư duy logic'),
('GS00012', 'Nguyễn Thị Lan', '0999999000', 'SV ĐH Khoa học Tự nhiên', 'Hóa học', '2 năm kinh nghiệm dạy Hóa ôn thi đại học, có phương pháp mẹo hiệu quả'),
('GS00013', 'Phạm Văn Nam', '0912123456', 'GV tự do', 'Vật lý', '5 năm kinh nghiệm dạy Lý online và offline, ôn thi đại học'),
('GS00014', 'Hoàng Thị Oanh', '0923234567', 'SV ĐH Bách Khoa Hà Nội', 'Toán', '3 năm kinh nghiệm gia sư Toán cho học sinh cấp 2 và 3'),
('GS00015', 'Đinh Văn Phong', '0934345678', 'SV ĐH Công nghệ - ĐHQGHN', 'Tin học', '2 năm giảng dạy lập trình C++, Java cho sinh viên năm nhất'),
('GS00016', 'Lương Hoàng Quân', '0945456789', 'SV ĐH Sư phạm Hà Nội', 'Ngữ văn', '1.5 năm kèm cặp học sinh mất gốc Văn lớp 8-9'),
('GS00017', 'Nguyễn Thu Quỳnh', '0956567890', 'SV ĐH Ngoại Thương', 'Anh văn', '2 năm kinh nghiệm dạy IELTS, học sinh đạt band 6.5+'),
('GS00018', 'Trịnh Văn Sơn', '0967678901', 'GV Vật lý - ĐH Sư phạm Hà Nội', 'Vật lý', '4 năm kinh nghiệm dạy Lý chuyên sâu, ôn thi đại học'),
('GS00019', 'Ngô Thị Trang', '0978789012', 'SV ĐH Kinh tế Quốc dân', 'Toán', '2 năm dạy kèm toán cấp 1 và cấp 2, áp dụng phương pháp tư duy nhanh'),
('GS00020', 'Bùi Văn Việt', '0989890123', 'SV Hóa học - ĐH KHTN', 'Hóa học', '5 năm kinh nghiệm dạy luyện thi Hóa cấp 3, phương pháp học dễ nhớ');
""")

connect.commit()
cursor.close()
connect.close()
