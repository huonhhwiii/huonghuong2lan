import mysql.connector

connect = mysql.connector.connect(
    host='localhost',
    user='root',
    password='huong24052005',
    database='QuanLyGiaSu'
)

cursor = connect.cursor()

cursor.execute("""
INSERT INTO LOPHOC (MaLop, MonHoc, CapHoc, LichHoc, DiaDiem, MaGD) VALUES
('LH00001', 'Toán', 'Lớp 9', '2024-03-05', 'Tại nhà PH', 'GD00001'),
('LH00002', 'Anh văn', 'Lớp 8', '2024-03-10', 'Online', 'GD00002'),
('LH00003', 'Vật lý', 'Lớp 11', '2024-03-14', 'Tại nhà PH', 'GD00003'),
('LH00004', 'Hóa học', 'Lớp 10', '2024-03-20', 'Tại nhà PH', 'GD00004'),
('LH00005', 'Toán', 'Lớp 12', '2024-03-25', 'Online', 'GD00005'),
('LH00006', 'Ngữ văn', 'Lớp 9', '2024-03-30', 'Tại nhà PH', 'GD00006'),
('LH00007', 'Anh văn', 'Lớp 5', '2024-04-05', 'Online', 'GD00007'),
('LH00008', 'Toán', 'Lớp 6', '2024-04-12', 'Tại nhà PH', 'GD00008'),
('LH00009', 'Vật lý', 'Lớp 12', '2024-04-17', 'Online', 'GD00009'),
('LH00010', 'Hóa học', 'Lớp 8', '2024-04-23', 'Tại nhà PH', 'GD00010'),
('LH00011', 'Toán', 'Lớp 5', '2024-04-28', 'Online', 'GD00011'),
('LH00012', 'Ngữ văn', 'Lớp 12', '2024-05-03', 'Tại nhà PH', 'GD00012'),
('LH00013', 'Anh văn', 'Lớp 7', '2024-05-08', 'Online', 'GD00013'),
('LH00014', 'Toán', 'Lớp 10', '2024-05-15', 'Tại nhà PH', 'GD00014'),
('LH00015', 'Vật lý', 'Lớp 9', '2024-05-20', 'Online', 'GD00015'),
('LH00016', 'Hóa học', 'Lớp 11', '2024-05-25', 'Tại nhà PH', 'GD00016'),
('LH00017', 'Tin học', 'Lập trình Python', '2024-05-30', 'Online', 'GD00017'),
('LH00018', 'Anh văn', 'Lớp 10', '2024-06-06', 'Tại nhà PH', 'GD00018'),
('LH00019', 'Toán', 'Lớp 4', '2024-06-12', 'Tại nhà PH', 'GD00019'),
('LH00020', 'Ngữ văn', 'Lớp 6', '2024-06-19', 'Online', 'GD00020');
""")

connect.commit()
cursor.close()
connect.close()
