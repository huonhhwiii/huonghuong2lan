import mysql.connector

connect = mysql.connector.connect(
    host='localhost',
    user='root',
    password='huong24052005',
    database='QuanLyGiaSu'
)

cursor = connect.cursor()

cursor.execute("""
NSERT INTO PHUHUYNH (MaPH, HoTen, SoDT, DiaChi, YeuCau) VALUES
('PH00001', 'Nguyễn Thị Mai', '0981000001', 'Cầu Giấy', 'Tìm gia sư Toán lớp 9 ôn thi vào 10, con làm bài nhanh nhưng hay sai lỗi nhỏ'),
('PH00002', 'Hoàng Văn Dũng', '0972000002', 'Đống Đa', 'Cần gia sư Anh văn lớp 8, con nghe hiểu kém, cần cải thiện phản xạ giao tiếp'),
('PH00003', 'Phạm Minh Hải', '0963000003', 'Thanh Xuân', 'Gia sư Lý lớp 11, con yếu phần dòng điện xoay chiều, cần ôn chắc để thi HK2'),
('PH00004', I'Bùi Thị Lan', '0954000004', 'Hai Bà Trưng', 'Tìm gia sư Hóa lớp 10, con học cơ bản ổn nhưng làm bài tập chưa vững'),
('PH00005', 'Vũ Quang Minh', '0945000005', 'Cầu Giấy', 'Gia sư Toán lớp 12 ôn thi đại học, con cần luyện đề nhiều hơn'),
('PH00006', 'Lê Thị Hương', '0936000006', 'Đống Đa', 'Tìm gia sư Văn lớp 9, con viết bài thiếu ý, cần rèn kỹ năng lập dàn ý'),
('PH00007', 'Trần Văn Hậu', '0927000007', 'Thanh Xuân', 'Gia sư Anh văn lớp 5, con cần ôn thi Cambridge Flyers'),
('PH00008', 'Nguyễn Thị Oanh', '0918000008', 'Hai Bà Trưng', 'Tìm gia sư Toán lớp 6, con chưa quen cách trình bày bài tự luận'),
('PH00009', 'Hoàng Minh Tuấn', '0909000009', 'Cầu Giấy', 'Gia sư Lý lớp 12, ôn thi ĐH, con làm trắc nghiệm sai nhiều do nhầm công thức'),
('PH00010', 'Phan Thị Ngọc', '0990000010', 'Đống Đa', 'Cần gia sư Hóa lớp 8, con hay quên lý thuyết, cần phương pháp ghi nhớ tốt hơn'),
('PH00011', 'Tạ Văn Sơn', '0981100011', 'Thanh Xuân', 'Tìm gia sư Toán lớp 5, con hay nhầm phép tính, cần ôn kỹ các dạng bài cơ bản'),
('PH00012', 'Nguyễn Thu Trang', '0972200012', 'Hai Bà Trưng', 'Gia sư Văn lớp 12 ôn thi đại học, con yếu phần nghị luận văn học'),
('PH00013', 'Bùi Thị Thanh', '0963300013', 'Cầu Giấy', 'Gia sư Anh văn lớp 7, con phát âm chưa chuẩn, cần cải thiện kỹ năng nói'),
('PH00014', 'Đỗ Quang Hải', '0954400014', 'Đống Đa', 'Tìm gia sư Toán lớp 10, con mất gốc Hình học, cần học từ cơ bản'),
('PH00015', 'Lương Thị Nhung', '0945500015', 'Thanh Xuân', 'Gia sư Lý lớp 9, con cần luyện tập nhiều bài tập nhiệt học'),
('PH00016', 'Phạm Văn Thịnh', '0936600016', 'Hai Bà Trưng', 'Gia sư Hóa lớp 11, con yếu phần điện phân, cần luyện bài tập nhiều hơn'),
('PH00017', 'Ngô Minh Đức', '0927700017', 'Cầu Giấy', 'Gia sư Tin học, con muốn học lập trình Python cơ bản'),
('PH00018', 'Hoàng Thu Hương', '0918800018', 'Đống Đa', 'Tìm gia sư Anh văn lớp 10, con cần ôn thi IELTS mục tiêu 5.5'),
('PH00019', 'Trịnh Văn Hùng', '0909900019', 'Thanh Xuân', 'Cần gia sư Toán lớp 4, con chậm tiếp thu, cần phương pháp dạy dễ hiểu'),
('PH00020', 'Bùi Thị Phương', '0990000020', 'Hai Bà Trưng', 'Gia sư Văn lớp 6, con chưa biết cách viết bài cảm thụ văn học'),
('PH00021', 'Nguyễn Văn Thắng', '0982111121', 'Cầu Giấy', 'Cần gia sư Toán lớp 3, con chưa nắm chắc bảng cửu chương'),
('PH00022', 'Lê Thị Hồng', '0973222222', 'Đống Đa', 'Tìm gia sư Văn lớp 7, con viết bài chưa có cảm xúc, điểm kiểm tra chỉ khoảng 6-7'),
('PH00023', 'Bùi Minh Tuấn', '0964333323', 'Thanh Xuân', 'Gia sư Anh văn lớp 9, con học ngữ pháp khá nhưng kém phần nghe nói'),
('PH00024', 'Trần Thị Thanh', '0955444424', 'Hai Bà Trưng', 'Cần gia sư Lý lớp 11, con yếu phần dao động cơ, sợ môn này'),
('PH00025', 'Phạm Văn Hoàng', '0946555525', 'Cầu Giấy', 'Gia sư Hóa lớp 8, con không nhớ bảng tuần hoàn, cần phương pháp học dễ nhớ'),
('PH00026', 'Ngô Thị Lan', '0937666626', 'Đống Đa', 'Tìm gia sư Toán lớp 6, con cần làm quen với toán tư duy cấp 2'),
('PH00027', 'Hoàng Minh Phúc', '0928777727', 'Thanh Xuân', 'Cần gia sư Tin học, con muốn học lập trình Scratch để thi học sinh giỏi'),
('PH00028', 'Vũ Quang Lâm', '0919888828', 'Hai Bà Trưng', 'Gia sư Toán lớp 12, con cần ôn thi khối A, làm đề nhưng hay sai câu khó'),
('PH00029', 'Đào Thị Hương', '0909999929', 'Cầu Giấy', 'Tìm gia sư Tiếng Anh lớp 5, con đang ôn thi Movers nhưng thiếu từ vựng'),
('PH00030', 'Tạ Văn Minh', '0990000030', 'Đống Đa', 'Cần gia sư Văn lớp 12, con làm bài dài dòng, chưa biết cách viết súc tích');
""")

connect.commit()
cursor.close()
connect.close()
