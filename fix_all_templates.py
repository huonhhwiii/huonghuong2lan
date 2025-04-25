import os
import re

# Đường dẫn đến thư mục templates
templates_dir = 'nhakhoaso/templates'

# Danh sách các file cần bỏ qua
skip_files = ['layout.html', 'sidebar.html']

# Đếm số file đã cập nhật
updated_files = 0

# Duyệt qua tất cả các file trong thư mục templates
for filename in os.listdir(templates_dir):
    if filename.endswith('.html') and filename not in skip_files:
        file_path = os.path.join(templates_dir, filename)
        
        # Đọc nội dung file
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Lưu nội dung ban đầu để so sánh sau khi sửa
        original_lines = lines.copy()
        
        # Xóa các dòng trống liên tiếp
        new_lines = []
        prev_line_empty = False
        for line in lines:
            is_empty = line.strip() == ''
            if not (is_empty and prev_line_empty):
                new_lines.append(line)
            prev_line_empty = is_empty
        
        # Nếu nội dung đã thay đổi, ghi lại vào file
        if new_lines != original_lines:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(new_lines)
            
            updated_files += 1
            print(f"Đã sửa file: {filename}")

print(f"\nĐã sửa tổng cộng {updated_files} file template.")