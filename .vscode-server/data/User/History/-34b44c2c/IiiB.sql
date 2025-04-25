-- Tạo database
CREATE DATABASE IF NOT EXISTS QLPhongKhamNhaKhoa;
USE QLPhongKhamNhaKhoa;

-- Bảng BENHNHAN
CREATE TABLE IF NOT EXISTS BENHNHAN (
    MaBN CHAR(7) NOT NULL PRIMARY KEY COMMENT 'Mã bệnh nhân',
    HoTen VARCHAR(100) CHARACTER SET utf8mb4 NOT NULL COMMENT 'Họ tên bệnh nhân',
    NgaySinh DATE NULL COMMENT 'Ngày sinh',
    GioiTinh CHAR(10) NULL COMMENT 'Giới tính',
    Sdt CHAR(10) NOT NULL COMMENT 'Số điện thoại'
);

-- Bảng BACSI
CREATE TABLE IF NOT EXISTS BACSI (
    MaBS CHAR(10) NOT NULL PRIMARY KEY COMMENT 'Mã bác sĩ',
    HoTen VARCHAR(100) CHARACTER SET utf8mb4 NOT NULL COMMENT 'Họ tên bác sĩ',
    Sdt CHAR(10) NOT NULL COMMENT 'Số điện thoại'
);

-- Bảng DICHVU
CREATE TABLE IF NOT EXISTS DICHVU (
    MaDV CHAR(10) NOT NULL PRIMARY KEY COMMENT 'Mã dịch vụ',
    TenDV VARCHAR(100) CHARACTER SET utf8mb4 NOT NULL COMMENT 'Tên dịch vụ',
    Gia DECIMAL(18,2) NULL COMMENT 'Giá'
);

-- Bảng LICHHEN
CREATE TABLE IF NOT EXISTS LICHHEN (
    MaLH CHAR(7) NOT NULL PRIMARY KEY COMMENT 'Mã lịch hẹn',
    MaBN CHAR(7) NOT NULL COMMENT 'Mã bệnh nhân',
    NgayHen DATETIME NOT NULL COMMENT 'Ngày hẹn khám',
    TrangThai VARCHAR(50) CHARACTER SET utf8mb4 NULL COMMENT 'Trạng thái',
    FOREIGN KEY (MaBN) REFERENCES BENHNHAN(MaBN)
);

-- Bảng PHIEUKHAM
CREATE TABLE IF NOT EXISTS PHIEUKHAM (
    MaPK CHAR(10) NOT NULL PRIMARY KEY COMMENT 'Mã phiếu khám',
    MaBN CHAR(7) NOT NULL COMMENT 'Mã bệnh nhân',
    MaBS CHAR(10) NOT NULL COMMENT 'Mã bác sĩ',
    MaDV CHAR(10) NOT NULL COMMENT 'Mã dịch vụ',
    NgayKham DATETIME NULL COMMENT 'Ngày khám',
    ChanDoan VARCHAR(255) CHARACTER SET utf8mb4 NULL COMMENT 'Chẩn đoán',
    GhiChu VARCHAR(255) CHARACTER SET utf8mb4 NULL COMMENT 'Ghi chú',
    FOREIGN KEY (MaBN) REFERENCES BENHNHAN(MaBN),
    FOREIGN KEY (MaBS) REFERENCES BACSI(MaBS),
    FOREIGN KEY (MaDV) REFERENCES DICHVU(MaDV)
);

-- Thêm dữ liệu mẫu cho bảng BENHNHAN
INSERT INTO BENHNHAN (MaBN, HoTen, NgaySinh, GioiTinh, Sdt) VALUES
('BN00001', 'Nguyễn Thị Mai', '1992-03-10', 'Nữ', '0901122334'),
('BN00002', 'Trần Văn Hùng', '1985-11-22', 'Nam', '0912233445'),
('BN00003', 'Lê Hoàng Nam', '1990-06-15', 'Nam', '0923344556'),
('BN00004', 'Phạm Thị Hòa', '1996-01-30', 'Nữ', '0934455667'),
('BN00005', 'Hoàng Quốc Tuấn', '1988-08-08', 'Nam', '0945566778');

-- Thêm dữ liệu mẫu cho bảng BACSI
INSERT INTO BACSI (MaBS, HoTen, Sdt) VALUES
('BS00000001', 'Nguyễn Văn An', '0912345678'),
('BS00000002', 'Trần Thị Bình', '0987654321'),
('BS00000003', 'Lê Văn Cường', '0909090909'),
('BS00000004', 'Phạm Thị Dung', '0934567890'),
('BS00000005', 'Đỗ Văn Hải', '0945123456'),
('BS00000006', 'Vũ Thị Hạnh', '0956781234'),
('BS00000007', 'Lê Quốc Hưng', '0967894321'),
('BS00000008', 'Nguyễn Minh Tâm', '0978912345'),
('BS00000009', 'Trịnh Hữu Thắng', '0981234567'),
('BS00000010', 'Hoàng Lan Anh', '0992345678');

-- Thêm dữ liệu mẫu cho bảng DICHVU
INSERT INTO DICHVU (MaDV, TenDV, Gia) VALUES
('DV00000001', 'Khám răng định kỳ', 150000),
('DV00000002', 'Nhổ răng khôn', 500000),
('DV00000003', 'Tẩy trắng răng', 700000),
('DV00000004', 'Trám răng thẩm mỹ', 300000),
('DV00000005', 'Niềng răng chỉnh nha', 25000000);

-- Thêm dữ liệu mẫu cho bảng LICHHEN
INSERT INTO LICHHEN (MaLH, MaBN, NgayHen, TrangThai) VALUES
('LH00001', 'BN00001', '2025-04-20 09:00:00', 'Chưa khám'),
('LH00002', 'BN00002', '2025-04-21 10:00:00', 'Đã khám'),
('LH00003', 'BN00003', '2025-04-22 14:00:00', 'Chưa khám'),
('LH00004', 'BN00004', '2025-04-23 08:30:00', 'Đã khám'),
('LH00005', 'BN00005', '2025-04-24 13:30:00', 'Chưa khám'),
('LH00006', 'BN00001', '2025-04-25 15:00:00', 'Đã huỷ'),
('LH00007', 'BN00003', '2025-04-26 10:30:00', 'Đã huỷ'),
('LH00008', 'BN00004', '2025-04-27 16:45:00', 'Đã huỷ');

-- Thêm dữ liệu mẫu cho bảng PHIEUKHAM
INSERT INTO PHIEUKHAM (MaPK, MaBN, MaBS, MaDV, NgayKham, ChanDoan, GhiChu) VALUES
('PK00001', 'BN00001', 'BS00000001', 'DV00000001', '2025-04-20 09:30:00', 'Viêm nướu nhẹ', 'Được tư vấn chăm sóc răng và khám định kỳ'),
('PK00002', 'BN00002', 'BS00000002', 'DV00000002', '2025-04-21 10:30:00', 'Răng khôn mọc lệch', 'Đã nhổ răng khôn và kê thuốc giảm đau'),
('PK00003', 'BN00003', 'BS00000003', 'DV00000003', '2025-04-22 14:30:00', 'Răng ố vàng', 'Thực hiện tẩy trắng răng theo yêu cầu'),
('PK00004', 'BN00004', 'BS00000004', 'DV00000004', '2025-04-23 08:45:00', 'Sâu răng nhẹ', 'Trám răng thẩm mỹ để phục hồi hình dạng răng'),
('PK00005', 'BN00005', 'BS00000005', 'DV00000005', '2025-04-24 13:45:00', 'Răng mọc lệch', 'Chỉ định niềng răng chỉnh nha trong 12 tháng');