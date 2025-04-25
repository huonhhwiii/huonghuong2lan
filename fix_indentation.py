import os
import re

# Đường dẫn đến thư mục templates
templates_dir = 'nhakhoaso/templates'

# Danh sách các file cần bỏ qua
skip_files = ['layout.html', 'sidebar.html']

# Pattern để tìm các thẻ div với thụt lề không đúng
indentation_pattern = re.compile(r'(\s{8,})<div', re.MULTILINE)
indentation_pattern2 = re.compile(r'(\s{8,})<table', re.MULTILINE)
indentation_pattern3 = re.compile(r'(\s{8,})<thead', re.MULTILINE)
indentation_pattern4 = re.compile(r'(\s{8,})<tbody', re.MULTILINE)
indentation_pattern5 = re.compile(r'(\s{8,})<tr', re.MULTILINE)
indentation_pattern6 = re.compile(r'(\s{8,})<td', re.MULTILINE)
indentation_pattern7 = re.compile(r'(\s{8,})<th', re.MULTILINE)
indentation_pattern8 = re.compile(r'(\s{8,})</div>', re.MULTILINE)
indentation_pattern9 = re.compile(r'(\s{8,})</table>', re.MULTILINE)
indentation_pattern10 = re.compile(r'(\s{8,})</thead>', re.MULTILINE)
indentation_pattern11 = re.compile(r'(\s{8,})</tbody>', re.MULTILINE)
indentation_pattern12 = re.compile(r'(\s{8,})</tr>', re.MULTILINE)
indentation_pattern13 = re.compile(r'(\s{8,})</td>', re.MULTILINE)
indentation_pattern14 = re.compile(r'(\s{8,})</th>', re.MULTILINE)

# Đếm số file đã cập nhật
updated_files = 0

# Duyệt qua tất cả các file trong thư mục templates
for filename in os.listdir(templates_dir):
    if filename.endswith('.html') and filename not in skip_files:
        file_path = os.path.join(templates_dir, filename)
        
        # Đọc nội dung file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Lưu nội dung ban đầu để so sánh sau khi sửa
        original_content = content
        
        # Sửa thụt lề cho các thẻ div
        content = indentation_pattern.sub(r'<div', content)
        content = indentation_pattern2.sub(r'<table', content)
        content = indentation_pattern3.sub(r'<thead', content)
        content = indentation_pattern4.sub(r'<tbody', content)
        content = indentation_pattern5.sub(r'<tr', content)
        content = indentation_pattern6.sub(r'<td', content)
        content = indentation_pattern7.sub(r'<th', content)
        content = indentation_pattern8.sub(r'</div>', content)
        content = indentation_pattern9.sub(r'</table>', content)
        content = indentation_pattern10.sub(r'</thead>', content)
        content = indentation_pattern11.sub(r'</tbody>', content)
        content = indentation_pattern12.sub(r'</tr>', content)
        content = indentation_pattern13.sub(r'</td>', content)
        content = indentation_pattern14.sub(r'</th>', content)
        
        # Nếu nội dung đã thay đổi, ghi lại vào file
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            updated_files += 1
            print(f"Đã sửa file: {filename}")

print(f"\nĐã sửa tổng cộng {updated_files} file template.")