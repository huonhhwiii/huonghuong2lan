import mysql.connector
connect = mysql.connector.connect(
    host='localhost',
    user='root',
    password='huong24052005',
    database='QuanLyGiaSu'
)
cursor = connect.cursor()
cursor.execute("INSERT INTO GIASU (MaGS, HoTen, SoDT, BangCap, MonDay, KinhNghiem) VALUES
('GS00001', N'Nguyễn Văn An', '0981111222', N'SV ĐH Bách Khoa Hà Nội', N'Toán', N'2 năm kinh nghiệm dạy Toán cấp 2, giúp học sinh cải thiện tư duy logic'),
('GS00002', N'Trần Thị Bích', '0973333444', N'SV ĐH Ngoại Thương', N'Anh văn', N'1.5 năm dạy Anh văn giao tiếp cho học sinh cấp 3, luyện phát âm chuẩn'),
('GS00003', N'Phạm Minh Cường', '0915555666', N'SV ĐH Sư phạm Hà Nội', N'Ngữ văn', N'3 năm dạy kèm môn Văn, chuyên ôn thi vào lớp 10'),
('GS00004', N'Lê Thị Dung', '0907777888', N'SV ĐH Y Hà Nội', N'Hóa học', N'2 năm dạy Hóa lớp 10-12, có phương pháp ghi nhớ công thức hiệu quả'),
('GS00005', N'Hoàng Văn Đông', '0921111222', N'SV CNTT - ĐH Quốc Gia Hà Nội', N'Tin học', N'4 năm kinh nghiệm lập trình Python, từng làm trợ giảng khóa lập trình online'),
('GS00006', N'Đặng Thị Hà', '0933333444', N'SV ĐH Kinh tế Quốc dân', N'Toán', N'1 năm dạy kèm Toán cấp 2, giúp học sinh yếu cải thiện điểm số'),
('GS00007', N'Vũ Quang Huy', '0944444555', N'GV Toán - ĐH Sư phạm Hà Nội', N'Toán', N'5 năm kinh nghiệm dạy Toán cấp 3, ôn thi đại học'),
('GS00008', N'Nguyễn Mai Linh', '0955555666', N'SV ĐH Hà Nội', N'Anh văn', N'2 năm kinh nghiệm dạy IELTS, học sinh đạt 6.5+'),
('GS00009', N'Bùi Mạnh Tiến', '0966666777', N'SV ĐH Xây Dựng', N'Vật lý', N'1 năm kinh nghiệm dạy Lý cấp 3, chuyên bài tập thực hành'),
('GS00010', N'Phan Thu Hằng', '0977777888', N'SV ĐH Ngoại Ngữ', N'Anh văn', N'2.5 năm dạy Tiếng Anh trẻ em, giúp học sinh phát âm chuẩn hơn'),
('GS00011', N'Tạ Minh Khôi', '0988888999', N'SV ĐH Giao thông Vận tải', N'Toán', N'1 năm dạy Toán cấp 2, giúp học sinh cải thiện tư duy logic'),
('GS00012', N'Nguyễn Thị Lan', '0999999000', N'SV ĐH Khoa học Tự nhiên', N'Hóa học', N'2 năm kinh nghiệm dạy Hóa ôn thi đại học, có phương pháp mẹo hiệu quả'),
('GS00013', N'Phạm Văn Nam', '0912123456', N'GV tự do', N'Vật lý', N'5 năm kinh nghiệm dạy Lý online và offline, ôn thi đại học'),
('GS00014', N'Hoàng Thị Oanh', '0923234567', N'SV ĐH Bách Khoa Hà Nội', N'Toán', N'3 năm kinh nghiệm gia sư Toán cho học sinh cấp 2 và 3'),
('GS00015', N'Đinh Văn Phong', '0934345678', N'SV ĐH Công nghệ - ĐHQGHN', N'Tin học', N'2 năm giảng dạy lập trình C++, Java cho sinh viên năm nhất'),
('GS00016', N'Lương Hoàng Quân', '0945456789', N'SV ĐH Sư phạm Hà Nội', N'Ngữ văn', N'1.5 năm kèm cặp học sinh mất gốc Văn lớp 8-9'),
('GS00017', N'Nguyễn Thu Quỳnh', '0956567890', N'SV ĐH Ngoại Thương', N'Anh văn', N'2 năm kinh nghiệm dạy IELTS, học sinh đạt band 6.5+'),
('GS00018', N'Trịnh Văn Sơn', '0967678901', N'GV Vật lý - ĐH Sư phạm Hà Nội', N'Vật lý', N'4 năm kinh nghiệm dạy Lý chuyên sâu, ôn thi đại học'),
('GS00019', N'Ngô Thị Trang', '0978789012', N'SV ĐH Kinh tế Quốc dân', N'Toán', N'2 năm dạy kèm toán cấp 1 và cấp 2, áp dụng phương pháp tư duy nhanh'),
('GS00020', N'Bùi Văn Việt', '0989890123', N'SV Hóa học - ĐH KHTN', N'Hóa học', N'5 năm kinh nghiệm dạy luyện thi Hóa cấp 3, phương pháp học dễ nhớ');
")
cursor.close()
connect.close()

