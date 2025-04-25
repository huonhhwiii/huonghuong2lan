import os
import re

# Đường dẫn đến thư mục templates
templates_dir = 'nhakhoaso/templates'

# Danh sách các file cần bỏ qua
skip_files = ['layout.html', 'sidebar.html']

# Pattern để tìm các thẻ div đóng dư thừa ở cuối file
closing_divs_pattern = re.compile(r'\s*</div>\s*</div>\s*{% endblock %}', re.DOTALL)

# Pattern để tìm các thẻ div.page-container và div.sidebar
page_container_pattern = re.compile(r'<div class="page-container">\s*<!-- Sidebar -->\s*<div class="sidebar">.*?</div>\s*<!-- Main content -->', re.DOTALL)

# Pattern để tìm các thẻ endblock dư thừa
multiple_endblock_pattern = re.compile(r'{% endblock %}\s*{% endblock %}', re.DOTALL)

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
        
        # Xóa các thẻ div đóng dư thừa
        content = closing_divs_pattern.sub('{% endblock %}', content)
        
        # Xóa các thẻ div.page-container và div.sidebar
        if page_container_pattern.search(content):
            content = page_container_pattern.sub('', content)
        
        # Xóa các thẻ div.main-content dư thừa
        content = content.replace('<div class="main-content">', '')
        
        # Xóa các thẻ div đóng dư thừa
        content = content.replace('</div>\n</div>\n{% endblock %}', '{% endblock %}')
        content = content.replace('</div>\n</div>{% endblock %}', '{% endblock %}')
        
        # Xóa các thẻ endblock dư thừa
        content = multiple_endblock_pattern.sub('{% endblock %}', content)
        
        # Nếu nội dung đã thay đổi, ghi lại vào file
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            updated_files += 1
            print(f"Đã sửa file: {filename}")

print(f"\nĐã sửa tổng cộng {updated_files} file template.")