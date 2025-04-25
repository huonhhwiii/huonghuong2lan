import os
import re

# Đường dẫn đến thư mục templates
templates_dir = 'nhakhoaso/templates'

# Danh sách các file cần bỏ qua
skip_files = ['layout.html', 'sidebar.html']

# Pattern để tìm các thẻ div đóng dư thừa ở cuối file
closing_divs_pattern = re.compile(r'\s*</div>\s*</div>\s*{% endblock %}', re.DOTALL)

# Đếm số file đã cập nhật
updated_files = 0

# Duyệt qua tất cả các file trong thư mục templates
for filename in os.listdir(templates_dir):
    if filename.endswith('.html') and filename not in skip_files:
        file_path = os.path.join(templates_dir, filename)
        
        # Đọc nội dung file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Kiểm tra xem file có chứa các thẻ div đóng dư thừa không
        if closing_divs_pattern.search(content):
            # Xóa các thẻ div đóng dư thừa
            new_content = closing_divs_pattern.sub('{% endblock %}', content)
            
            # Ghi nội dung mới vào file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            updated_files += 1
            print(f"Đã sửa file: {filename}")

print(f"\nĐã sửa tổng cộng {updated_files} file template.")