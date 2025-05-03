// Dữ liệu nhiệm vụ (trong thực tế nên lưu trên server)
let tasks = {
    "https://yeumoney.com/BWq9l": { key: "anhcodedz1235", reward: 100 },
    "https://yeumoney.com/wr--U": { key: "anhcodedz1223", reward: 100 },
    "https://yeumoney.com/GG2eLN": { key: "anhcodeyeuem", reward: 100 },
    "https://yeumoney.com/9qV-db": { key: "anhcodedz1354", reward: 100 },
    "https://yeumoney.com/iCv-DF2": { key: "anhcodekeycuoihaha", reward: 100 }
};

// Admin credentials (trong thực tế nên xác thực qua backend)
const ADMIN_CREDENTIALS = {
    username: "admin",
    password: "admin123"
};

// Hiển thị danh sách nhiệm vụ
function renderTaskList() {
    const taskList = document.getElementById('task-list');
    if (!taskList) return;
    
    taskList.innerHTML = '';
    
    let index = 1;
    for (const [link, task] of Object.entries(tasks)) {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${index}</td>
            <td>${link}</td>
            <td>${task.key}</td>
            <td>${task.reward} VNĐ</td>
            <td>
                <button class="danger" onclick="removeTask('${link}')">Xóa</button>
            </td>
        `;
        
        taskList.appendChild(row);
        index++;
    }
}

// Mở tab
function openTab(tabId) {
    // Ẩn tất cả các tab
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Hiển thị tab được chọn
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}

// Lấy key xác nhận cho người dùng
function getConfirmationKey() {
    const userId = document.getElementById('user-id').value.trim();
    const taskLink = document.getElementById('task-link').value.trim();
    const resultDiv = document.getElementById('user-result');
    
    // Kiểm tra input
    if (!userId || !taskLink) {
        showResult('Vui lòng điền đầy đủ ID Telegram và Link nhiệm vụ', 'error', 'user-result');
        return;
    }
    
    // Kiểm tra ID Telegram
    if (isNaN(userId) || userId.length < 5) {
        showResult('ID Telegram không hợp lệ', 'error', 'user-result');
        return;
    }
    
    // Kiểm tra link nhiệm vụ
    let foundTask = null;
    for (const [link, task] of Object.entries(tasks)) {
        if (taskLink.includes(link)) {
            foundTask = task;
            break;
        }
    }
    
    if (!foundTask) {
        showResult('Link nhiệm vụ không hợp lệ hoặc không tồn tại', 'error', 'user-result');
        return;
    }
    
    // Tạo key xác nhận
    const timestamp = Math.floor(Date.now() / 1000);
    const confirmationKey = `${foundTask.key}-${userId}-${timestamp}`;
    
    // Hiển thị key
    document.getElementById('confirmation-key').value = confirmationKey;
    document.getElementById('key-section').classList.remove('hidden');
    
    showResult(`✅ Key xác nhận đã được tạo! Bạn sẽ nhận được ${foundTask.reward} VNĐ khi xác nhận với bot.`, 'success', 'user-result');
}

// Sao chép key
function copyKey() {
    const keyInput = document.getElementById('confirmation-key');
    keyInput.select();
    document.execCommand('copy');
    
    // Hiển thị thông báo
    const originalText = keyInput.value;
    keyInput.value = "Đã sao chép!";
    setTimeout(() => {
        keyInput.value = originalText;
    }, 2000);
    
    showResult('Key đã được sao chép vào clipboard!', 'info', 'user-result');
}

// Gửi key về Telegram (giả lập)
function sendToTelegram() {
    const key = document.getElementById('confirmation-key').value;
    showResult(`Mở Telegram và gửi lệnh: <code>/nhapkey ${key}</code> cho bot`, 'info', 'user-result');
}

// Đăng nhập admin
function adminLogin() {
    const username = document.getElementById('admin-username').value.trim();
    const password = document.getElementById('admin-password').value.trim();
    
    if (username === ADMIN_CREDENTIALS.username && password === ADMIN_CREDENTIALS.password) {
        document.getElementById('admin-panel').classList.remove('hidden');
        showResult('Đăng nhập thành công!', 'success', 'admin-login-result');
        renderTaskList();
    } else {
        showResult('Sai tài khoản hoặc mật khẩu', 'error', 'admin-login-result');
    }
}

// Thêm nhiệm vụ mới
function addNewTask() {
    const link = document.getElementById('new-task-link').value.trim();
    const key = document.getElementById('new-task-key').value.trim();
    const reward = parseInt(document.getElementById('task-reward').value);
    
    if (!link || !key) {
        showResult('Vui lòng điền đầy đủ link và key', 'error', 'admin-result');
        return;
    }
    
    if (link in tasks) {
        showResult('Link nhiệm vụ đã tồn tại', 'error', 'admin-result');
        return;
    }
    
    tasks[link] = { key, reward };
    renderTaskList();
    
    // Reset form
    document.getElementById('new-task-link').value = '';
    document.getElementById('new-task-key').value = '';
    
    showResult('Đã thêm nhiệm vụ mới thành công!', 'success', 'admin-result');
}

// Xóa nhiệm vụ
function removeTask(link) {
    if (confirm(`Bạn có chắc muốn xóa nhiệm vụ:\n${link}`)) {
        delete tasks[link];
        renderTaskList();
        showResult('Đã xóa nhiệm vụ thành công', 'success', 'admin-result');
    }
}

// Reset danh sách nhiệm vụ
function resetTaskList() {
    if (confirm('Bạn có chắc muốn RESET toàn bộ danh sách nhiệm vụ?')) {
        tasks = {};
        renderTaskList();
        showResult('Đã reset danh sách nhiệm vụ', 'info', 'admin-result');
    }
}

// Xem thống kê người dùng (giả lập)
function viewUserStats() {
    showResult('Chức năng này cần kết nối với cơ sở dữ liệu phía server', 'info', 'admin-result');
}

// Xuất dữ liệu người dùng (giả lập)
function exportUserData() {
    showResult('Chức năng này cần kết nối với cơ sở dữ liệu phía server', 'info', 'admin-result');
}

// Hiển thị kết quả
function showResult(message, type, target) {
    const resultDiv = document.getElementById(target);
    if (!resultDiv) return;
    
    resultDiv.innerHTML = message;
    resultDiv.className = 'result ' + type;
    resultDiv.style.display = 'block';
    
    // Tự động ẩn thông báo sau 5 giây
    setTimeout(() => {
        resultDiv.style.display = 'none';
    }, 5000);
}

// Khởi tạo
document.addEventListener('DOMContentLoaded', function() {
    renderTaskList();
});
