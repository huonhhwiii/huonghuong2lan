import os
import re

# Đường dẫn đến thư mục templates
templates_dir = 'nhakhoaso/templates'

# Danh sách các file cần bỏ qua
skip_files = ['layout.html', 'sidebar.html']

# Pattern để tìm sidebar cũ
sidebar_pattern = re.compile(r'<div class="page-container">\s*<!-- Sidebar -->\s*<div class="sidebar">.*?</div>\s*<!-- Main content -->', re.DOTALL)

# Đếm số file đã cập nhật
updated_files = 0

# Duyệt qua tất cả các file trong thư mục templates
for filename in os.listdir(templates_dir):
    if filename.endswith('.html') and filename not in skip_files:
        file_path = os.path.join(templates_dir, filename)
        
        # Đọc nội dung file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Kiểm tra xem file có chứa sidebar cũ không
        if '<div class="page-container">' in content and '<!-- Sidebar -->' in content:
            # Xóa sidebar cũ
            new_content = sidebar_pattern.sub('', content)
            
            # Xóa thẻ div.main-content dư thừa nếu có
            new_content = new_content.replace('<div class="main-content">', '')
            new_content = new_content.replace('</div>\n</div>', '')
            
            # Ghi nội dung mới vào file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            updated_files += 1
            print(f"Đã cập nhật file: {filename}")

print(f"\nĐã cập nhật tổng cộng {updated_files} file template.")