/**
 * Hệ thống hộp thoại xác nhận xóa
 * File này cung cấp hộp thoại xác nhận xóa tùy chỉnh thay thế cho confirm() mặc định
 */

// Tạo và thêm HTML cho modal xác nhận xóa vào body
document.addEventListener('DOMContentLoaded', function() {
    // Tạo container cho modal
    const modalContainer = document.createElement('div');
    modalContainer.id = 'delete-confirmation-modal';
    modalContainer.className = 'modal-container';
    modalContainer.style.display = 'none';
    
    // Tạo nội dung modal
    modalContainer.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>Xác nhận xóa</h3>
                <span class="close-modal">&times;</span>
            </div>
            <div class="modal-body">
                <p id="delete-confirmation-message">Bạn có chắc chắn muốn xóa mục này?</p>
            </div>
            <div class="modal-footer">
                <button id="cancel-delete" class="btn btn-secondary">Hủy</button>
                <button id="confirm-delete" class="btn btn-danger">Xóa</button>
            </div>
        </div>
    `;
    
    // Thêm modal vào body
    document.body.appendChild(modalContainer);
    
    // Thêm CSS cho modal
    const modalStyle = document.createElement('style');
    modalStyle.textContent = `
        .modal-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .modal-content {
            background-color: white;
            border-radius: 8px;
            width: 400px;
            max-width: 90%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            animation: modalFadeIn 0.3s;
        }
        
        @keyframes modalFadeIn {
            from {opacity: 0; transform: translateY(-20px);}
            to {opacity: 1; transform: translateY(0);}
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .modal-header h3 {
            margin: 0;
            color: #333;
            font-size: 18px;
        }
        
        .close-modal {
            font-size: 24px;
            font-weight: bold;
            cursor: pointer;
            color: #888;
        }
        
        .close-modal:hover {
            color: #333;
        }
        
        .modal-body {
            padding: 20px;
            color: #333;
        }
        
        .modal-footer {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            padding: 15px 20px;
            border-top: 1px solid #e0e0e0;
        }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        
        .btn-secondary {
            background-color: #e0e0e0;
            color: #333;
        }
        
        .btn-danger {
            background-color: #dc3545;
            color: white;
        }
        
        .btn-secondary:hover {
            background-color: #d0d0d0;
        }
        
        .btn-danger:hover {
            background-color: #c82333;
        }
    `;
    
    document.head.appendChild(modalStyle);
    
    // Lấy các phần tử modal
    const modal = document.getElementById('delete-confirmation-modal');
    const closeBtn = modal.querySelector('.close-modal');
    const cancelBtn = document.getElementById('cancel-delete');
    const confirmBtn = document.getElementById('confirm-delete');
    
    // Đóng modal khi nhấp vào nút đóng
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    // Đóng modal khi nhấp vào nút hủy
    cancelBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    // Đóng modal khi nhấp vào bên ngoài modal
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});

/**
 * Hiển thị hộp thoại xác nhận xóa
 * @param {string} message - Thông báo xác nhận
 * @param {Function} onConfirm - Hàm callback khi người dùng xác nhận xóa
 */
function showDeleteConfirmation(message, onConfirm) {
    // Lấy các phần tử modal
    const modal = document.getElementById('delete-confirmation-modal');
    const messageElement = document.getElementById('delete-confirmation-message');
    const confirmBtn = document.getElementById('confirm-delete');
    
    // Cập nhật thông báo
    messageElement.textContent = message || 'Bạn có chắc chắn muốn xóa mục này?';
    
    // Hiển thị modal
    modal.style.display = 'flex';
    
    // Xóa event listener cũ (nếu có)
    const newConfirmBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
    
    // Thêm event listener mới
    newConfirmBtn.addEventListener('click', function() {
        modal.style.display = 'none';
        if (typeof onConfirm === 'function') {
            onConfirm();
        }
    });
}

// Hàm xóa bệnh nhân
function deletePatient(maBN) {
    showDeleteConfirmation(`Bạn có chắc chắn muốn xóa bệnh nhân này?`, function() {
        // Gọi API xóa bệnh nhân
        fetch(`/api/benh-nhan/${maBN}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Xóa dòng khỏi bảng
                const row = document.getElementById(`benh-nhan-${maBN}`);
                if (row) {
                    row.remove();
                    
                    // Kiểm tra nếu không còn bệnh nhân nào, hiển thị thông báo
                    const tbody = document.querySelector('.data-table tbody');
                    const remainingRows = tbody.querySelectorAll('tr:not(.no-data-row)');
                    
                    if (remainingRows.length === 0) {
                        tbody.innerHTML = `
                        <tr class="no-data-row">
                            <td colspan="8" class="text-center">
                                <div class="no-data">
                                    <i class="fas fa-database"></i>
                                    <p>Chưa có dữ liệu bệnh nhân</p>
                                    <a href="/benh-nhan/them-moi" class="btn">
                                        <i class="fas fa-plus"></i> Thêm bệnh nhân mới
                                    </a>
                                </div>
                            </td>
                        </tr>
                        `;
                    }
                }
                
                alert('Xóa bệnh nhân thành công!');
            } else {
                alert('Lỗi: ' + (data.message || 'Không thể xóa bệnh nhân'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã xảy ra lỗi khi xóa bệnh nhân: ' + error.message);
        });
    });
}

// Hàm xóa bác sĩ
function deleteDoctor(maBS) {
    showDeleteConfirmation(`Bạn có chắc chắn muốn xóa bác sĩ này?`, function() {
        // Gọi API xóa bác sĩ
        fetch(`/api/bac-si/${maBS}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Xóa dòng khỏi bảng
                const row = document.getElementById(`bac-si-${maBS}`);
                if (row) {
                    row.remove();
                    
                    // Kiểm tra nếu không còn bác sĩ nào, hiển thị thông báo
                    const tbody = document.querySelector('.data-table tbody');
                    const remainingRows = tbody.querySelectorAll('tr:not(.no-data-row)');
                    
                    if (remainingRows.length === 0) {
                        tbody.innerHTML = `
                        <tr class="no-data-row">
                            <td colspan="4" class="text-center">
                                <div class="no-data">
                                    <i class="fas fa-database"></i>
                                    <p>Chưa có dữ liệu bác sĩ</p>
                                    <a href="/bac-si/them-moi" class="btn">
                                        <i class="fas fa-plus"></i> Thêm bác sĩ mới
                                    </a>
                                </div>
                            </td>
                        </tr>
                        `;
                    }
                }
                
                alert('Xóa bác sĩ thành công!');
            } else {
                alert('Lỗi: ' + (data.message || 'Không thể xóa bác sĩ'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã xảy ra lỗi khi xóa bác sĩ: ' + error.message);
        });
    });
}

// Hàm xóa phiếu khám
function deletePhieuKham(maPK) {
    showDeleteConfirmation(`Bạn có chắc chắn muốn xóa phiếu khám này?`, function() {
        // Gọi API xóa phiếu khám
        fetch(`/api/phieu-kham/${maPK}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Lỗi kết nối máy chủ');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Xóa dòng khỏi bảng
                const row = document.getElementById(`phieu-kham-${maPK}`);
                if (row) {
                    row.remove();
                    
                    // Kiểm tra nếu không còn phiếu khám nào, hiển thị thông báo
                    const tbody = document.querySelector('.data-table tbody');
                    const remainingRows = tbody.querySelectorAll('tr:not(.no-data-row)');
                    
                    if (remainingRows.length === 0) {
                        tbody.innerHTML = `
                        <tr class="no-data-row">
                            <td colspan="8" class="text-center">
                                <div class="no-data">
                                    <i class="fas fa-database"></i>
                                    <p>Chưa có dữ liệu phiếu khám</p>
                                    <a href="/phieu-kham/them-moi" class="btn">
                                        <i class="fas fa-plus"></i> Tạo phiếu khám mới
                                    </a>
                                </div>
                            </td>
                        </tr>
                        `;
                    }
                }
                
                alert('Xóa phiếu khám thành công!');
            } else {
                alert('Lỗi: ' + (data.message || 'Không thể xóa phiếu khám'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã xảy ra lỗi khi xóa phiếu khám: ' + error.message);
        });
    });
}

// Hàm xóa lịch hẹn
function deleteLichHen(maLH) {
    showDeleteConfirmation(`Bạn có chắc chắn muốn xóa lịch hẹn này?`, function() {
        // Gọi API xóa lịch hẹn
        fetch(`/api/lich-hen/${maLH}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Xóa dòng khỏi bảng
                const row = document.getElementById(`lich-hen-${maLH}`);
                if (row) {
                    row.remove();
                    
                    // Kiểm tra nếu không còn lịch hẹn nào, hiển thị thông báo
                    const tbody = document.querySelector('.data-table tbody');
                    const remainingRows = tbody.querySelectorAll('tr:not(.no-data-row)');
                    
                    if (remainingRows.length === 0) {
                        tbody.innerHTML = `
                        <tr class="no-data-row">
                            <td colspan="8" class="text-center">
                                <div class="no-data">
                                    <i class="fas fa-database"></i>
                                    <p>Chưa có dữ liệu lịch hẹn</p>
                                    <a href="/lich-hen/them-moi" class="btn">
                                        <i class="fas fa-plus"></i> Tạo lịch hẹn mới
                                    </a>
                                </div>
                            </td>
                        </tr>
                        `;
                    }
                }
                
                alert('Xóa lịch hẹn thành công!');
            } else {
                alert('Lỗi: ' + (data.message || 'Không thể xóa lịch hẹn'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã xảy ra lỗi khi xóa lịch hẹn: ' + error.message);
        });
    });
}

// Hàm xóa dịch vụ
function deleteDichVu(maDV) {
    showDeleteConfirmation(`Bạn có chắc chắn muốn xóa dịch vụ này?`, function() {
        // Gọi API xóa dịch vụ
        fetch(`/api/dich-vu/${maDV}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Xóa dòng khỏi bảng
                const row = document.getElementById(`dich-vu-${maDV}`);
                if (row) {
                    row.remove();
                    
                    // Kiểm tra nếu không còn dịch vụ nào, hiển thị thông báo
                    const tbody = document.querySelector('.data-table tbody');
                    const remainingRows = tbody.querySelectorAll('tr:not(.no-data-row)');
                    
                    if (remainingRows.length === 0) {
                        tbody.innerHTML = `
                        <tr class="no-data-row">
                            <td colspan="4" class="text-center">
                                <div class="no-data">
                                    <i class="fas fa-database"></i>
                                    <p>Chưa có dữ liệu dịch vụ</p>
                                    <a href="/dich-vu/them-moi" class="btn">
                                        <i class="fas fa-plus"></i> Thêm dịch vụ mới
                                    </a>
                                </div>
                            </td>
                        </tr>
                        `;
                    }
                }
                
                alert('Xóa dịch vụ thành công!');
            } else {
                alert('Lỗi: ' + (data.message || 'Không thể xóa dịch vụ'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã xảy ra lỗi khi xóa dịch vụ: ' + error.message);
        });
    });
}