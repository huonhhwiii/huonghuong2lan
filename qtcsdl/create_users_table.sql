-- Tạo bảng NGUOIDUNG nếu chưa tồn tại
CREATE TABLE IF NOT EXISTS NGUOIDUNG (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    ho_ten VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    quyen VARCHAR(20) DEFAULT 'user',
    ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Thêm tài khoản admin mặc định (mật khẩu: admin123)
-- Lưu ý: Trong môi trường thực tế, mật khẩu nên được mã hóa
INSERT INTO NGUOIDUNG (username, password, ho_ten, quyen) 
VALUES ('admin', 'admin123', 'Quản trị viên', 'admin');

-- Thêm một số tài khoản người dùng mẫu
INSERT INTO NGUOIDUNG (username, password, ho_ten) 
VALUES ('user1', 'user123', 'Người dùng 1');

INSERT INTO NGUOIDUNG (username, password, ho_ten) 
VALUES ('user2', 'user123', 'Người dùng 2');