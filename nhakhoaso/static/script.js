document.addEventListener('DOMContentLoaded', function() {
    // Hiệu ứng khi hover vào các card dịch vụ
    const serviceCards = document.querySelectorAll('.service-card');
    
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
        });
        
        // Thêm sự kiện click để chuyển đến trang tương ứng
        card.addEventListener('click', function() {
            const link = this.getAttribute('data-link');
            if (link) {
                window.location.href = link;
            }
        });
    });
    
    // Hiệu ứng cuộn mượt cho các liên kết
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Xử lý sự kiện khi người dùng nhấp vào tiêu đề của thanh điều hướng
    const sidebarTitles = document.querySelectorAll('.sidebar-title');
    
    sidebarTitles.forEach(title => {
        title.addEventListener('click', function() {
            // Tìm menu liên quan đến tiêu đề này
            const menu = this.nextElementSibling;
            if (menu && menu.classList.contains('sidebar-menu')) {
                // Tìm liên kết đầu tiên trong menu
                const firstLink = menu.querySelector('a');
                if (firstLink) {
                    // Chuyển đến trang của liên kết đầu tiên
                    window.location.href = firstLink.getAttribute('href');
                }
            }
        });
        
        // Thêm cursor pointer để hiển thị rằng tiêu đề có thể nhấp vào
        title.style.cursor = 'pointer';
    });
});