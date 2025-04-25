import mysql.connector

connect = mysql.connector.connect(
    host='localhost',
    user='root',
    password='huong24052005',
    database='QuanLyGiaSu'
)

cursor = connect.cursor()

cursor.execute("""
INSERT INTO PHUHUYNH (MaPH, HoTen, SoDT, DiaChi, YeuCau) VALUES
('PH00001', N'Nguyễn Thị Mai', '0981000001', N'Cầu Giấy', N'Tìm gia sư Toán lớp 9 ôn thi vào 10, con làm bài nhanh nhưng hay sai lỗi nhỏ'),
('PH00002', N'Hoàng Văn Dũng', '0972000002', N'Đống Đa', N'Cần gia sư Anh văn lớp 8, con nghe hiểu kém, cần cải thiện phản xạ giao tiếp'),
('PH00003', N'Phạm Minh Hải', '0963000003', N'Thanh Xuân', N'Gia sư Lý lớp 11, con yếu phần dòng điện xoay chiều, cần ôn chắc để thi HK2'),
('PH00004', N'Bùi Thị Lan', '0954000004', N'Hai Bà Trưng', N'Tìm gia sư Hóa lớp 10, con học cơ bản ổn nhưng làm bài tập chưa vững'),
('PH00005', N'Vũ Quang Minh', '0945000005', N'Cầu Giấy', N'Gia sư Toán lớp 12 ôn thi đại học, con cần luyện đề nhiều hơn'),
('PH00006', N'Lê Thị Hương', '0936000006', N'Đống Đa', N'Tìm gia sư Văn lớp 9, con viết bài thiếu ý, cần rèn kỹ năng lập dàn ý'),
('PH00007', N'Trần Văn Hậu', '0927000007', N'Thanh Xuân', N'Gia sư Anh văn lớp 5, con cần ôn thi Cambridge Flyers'),
('PH00008', N'Nguyễn Thị Oanh', '0918000008', N'Hai Bà Trưng', N'Tìm gia sư Toán lớp 6, con chưa quen cách trình bày bài tự luận'),
('PH00009', N'Hoàng Minh Tuấn', '0909000009', N'Cầu Giấy', N'Gia sư Lý lớp 12, ôn thi ĐH, con làm trắc nghiệm sai nhiều do nhầm công thức'),
('PH00010', N'Phan Thị Ngọc', '0990000010', N'Đống Đa', N'Cần gia sư Hóa lớp 8, con hay quên lý thuyết, cần phương pháp ghi nhớ tốt hơn'),
('PH00011', N'Tạ Văn Sơn', '0981100011', N'Thanh Xuân', N'Tìm gia sư Toán lớp 5, con hay nhầm phép tính, cần ôn kỹ các dạng bài cơ bản'),
('PH00012', N'Nguyễn Thu Trang', '0972200012', N'Hai Bà Trưng', N'Gia sư Văn lớp 12 ôn thi đại học, con yếu phần nghị luận văn học'),
('PH00013', N'Bùi Thị Thanh', '0963300013', N'Cầu Giấy', N'Gia sư Anh văn lớp 7, con phát âm chưa chuẩn, cần cải thiện kỹ năng nói'),
('PH00014', N'Đỗ Quang Hải', '0954400014', N'Đống Đa', N'Tìm gia sư Toán lớp 10, con mất gốc Hình học, cần học từ cơ bản'),
('PH00015', N'Lương Thị Nhung', '0945500015', N'Thanh Xuân', N'Gia sư Lý lớp 9, con cần luyện tập nhiều bài tập nhiệt học'),
('PH00016', N'Phạm Văn Thịnh', '0936600016', N'Hai Bà Trưng', N'Gia sư Hóa lớp 11, con yếu phần điện phân, cần luyện bài tập nhiều hơn'),
('PH00017', N'Ngô Minh Đức', '0927700017', N'Cầu Giấy', N'Gia sư Tin học, con muốn học lập trình Python cơ bản'),
('PH00018', N'Hoàng Thu Hương', '0918800018', N'Đống Đa', N'Tìm gia sư Anh văn lớp 10, con cần ôn thi IELTS mục tiêu 5.5'),
('PH00019', N'Trịnh Văn Hùng', '0909900019', N'Thanh Xuân', N'Cần gia sư Toán lớp 4, con chậm tiếp thu, cần phương pháp dạy dễ hiểu'),
('PH00020', N'Bùi Thị Phương', '0990000020', N'Hai Bà Trưng', N'Gia sư Văn lớp 6, con chưa biết cách viết bài cảm thụ văn học'),
('PH00021', N'Nguyễn Văn Thắng', '0982111121', N'Cầu Giấy', N'Cần gia sư Toán lớp 3, con chưa nắm chắc bảng cửu chương'),
('PH00022', N'Lê Thị Hồng', '0973222222', N'Đống Đa', N'Tìm gia sư Văn lớp 7, con viết bài chưa có cảm xúc, điểm kiểm tra chỉ khoảng 6-7'),
('PH00023', N'Bùi Minh Tuấn', '0964333323', N'Thanh Xuân', N'Gia sư Anh văn lớp 9, con học ngữ pháp khá nhưng kém phần nghe nói'),
('PH00024', N'Trần Thị Thanh', '0955444424', N'Hai Bà Trưng', N'Cần gia sư Lý lớp 11, con yếu phần dao động cơ, sợ môn này'),
('PH00025', N'Phạm Văn Hoàng', '0946555525', N'Cầu Giấy', N'Gia sư Hóa lớp 8, con không nhớ bảng tuần hoàn, cần phương pháp học dễ nhớ'),
('PH00026', N'Ngô Thị Lan', '0937666626', N'Đống Đa', N'Tìm gia sư Toán lớp 6, con cần làm quen với toán tư duy cấp 2'),
('PH00027', N'Hoàng Minh Phúc', '0928777727', N'Thanh Xuân', N'Cần gia sư Tin học, con muốn học lập trình Scratch để thi học sinh giỏi'),
('PH00028', N'Vũ Quang Lâm', '0919888828', N'Hai Bà Trưng', N'Gia sư Toán lớp 12, con cần ôn thi khối A, làm đề nhưng hay sai câu khó'),
('PH00029', N'Đào Thị Hương', '0909999929', N'Cầu Giấy', N'Tìm gia sư Tiếng Anh lớp 5, con đang ôn thi Movers nhưng thiếu từ vựng'),
('PH00030', N'Tạ Văn Minh', '0990000030', N'Đống Đa', N'Cần gia sư Văn lớp 12, con làm bài dài dòng, chưa biết cách viết súc tích');
""")

connect.commit()
cursor.close()
connect.close()
