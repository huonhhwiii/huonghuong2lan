document.addEventListener('DOMContentLoaded', function() {
    // Auto-generate patient ID when page loads
    generatePatientId();

    // Form validation
    const form = document.getElementById('patientForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
            }
        });
    }

    // Reset button clears the form and regenerates patient ID
    const resetBtn = document.querySelector('.btn-reset');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            setTimeout(generatePatientId, 0);
        });
    }
});

function generatePatientId() {
    const patientIdField = document.getElementById('ma_bn');
    if (patientIdField && !patientIdField.value) {
        // Generate a 10-character patient ID starting with BN
        const randomPart = Math.random().toString(36).substring(2, 10).toUpperCase();
        patientIdField.value = 'BN' + randomPart;
    }
}

function validateForm() {
    let isValid = true;
    const form = document.getElementById('patientForm');

    // Validate patient ID (10 characters)
    const patientId = document.getElementById('ma_bn');
    if (patientId.value.length !== 10) {
        showError(patientId, 'Mã bệnh nhân phải có đúng 10 ký tự');
        isValid = false;
    } else {
        clearError(patientId);
    }

    // Validate name (not empty)
    const name = document.getElementById('ho_ten');
    if (name.value.trim() === '') {
        showError(name, 'Vui lòng nhập họ tên bệnh nhân');
        isValid = false;
    } else {
        clearError(name);
    }

    // Validate birth date (not empty)
    const birthDate = document.getElementById('ngay_sinh');
    if (birthDate.value === '') {
        showError(birthDate, 'Vui lòng chọn ngày sinh');
        isValid = false;
    } else {
        clearError(birthDate);
    }

    // Validate phone number (10-15 digits)
    const phone = document.getElementById('so_dien_thoai');
    const phoneRegex = /^\d{10,15}$/;
    if (!phoneRegex.test(phone.value)) {
        showError(phone, 'Số điện thoại phải có từ 10 đến 15 chữ số');
        isValid = false;
    } else {
        clearError(phone);
    }

    return isValid;
}

function showError(field, message) {
    const formGroup = field.closest('.form-group');
    if (!formGroup) return;

    // Remove existing error if any
    clearError(field);

    // Add error class
    field.classList.add('error');

    // Create error message element
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    errorElement.style.color = '#e74c3c';
    errorElement.style.fontSize = '0.85rem';
    errorElement.style.marginTop = '0.3rem';

    // Insert after the field
    field.insertAdjacentElement('afterend', errorElement);
}

function clearError(field) {
    const formGroup = field.closest('.form-group');
    if (!formGroup) return;

    // Remove error class
    field.classList.remove('error');

    // Remove error message if exists
    const errorMessage = formGroup.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}