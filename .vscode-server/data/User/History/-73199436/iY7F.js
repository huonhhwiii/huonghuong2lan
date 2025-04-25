document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const form = document.getElementById('patientForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            let valid = true;
            
            // Check required fields
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = 'red';
                } else {
                    field.style.borderColor = '';
                }
            });
            
            // Phone number validation
            const phoneField = document.getElementById('so_dien_thoai');
            if (phoneField && !/^\d{10,15}$/.test(phoneField.value.trim())) {
                valid = false;
                phoneField.style.borderColor = 'red';
                alert('Số điện thoại phải có từ 10 đến 15 chữ số');
            }
            
            // Patient ID validation (10 characters)
            const patientIdField = document.getElementById('ma_bn');
            if (patientIdField && patientIdField.value.trim().length !== 10) {
                valid = false;
                patientIdField.style.borderColor = 'red';
                alert('Mã bệnh nhân phải có đúng 10 ký tự');
            }
            
            if (!valid) {
                e.preventDefault();
                alert('Vui lòng kiểm tra lại thông tin nhập');
            }
        });
    }
    
    // Auto-generate patient code if needed
    const patientCodeField = document.getElementById('ma_bn');
    if (patientCodeField) {
        patientCodeField.addEventListener('focus', function() {
            if (!this.value) {
                // Generate a simple code (you can enhance this)
                const timestamp = new Date().getTime().toString().slice(-10);
                this.value = 'BN' + timestamp;
            }
        });
    }
});