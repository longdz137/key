from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests
import json, re
import os
import socket
import threading
import queue
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime

# Thiết lập logging với UTF-8
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("reg_tiktok.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Khóa để bảo vệ truy cập vào tài nguyên chia sẻ
proxy_lock = threading.Lock()
file_lock = threading.Lock()

Domain = [
    'nguyenhoang', 'tranthanhhai', 'leminhkhanh', 'phamthanhdat', 'hoangtrungnghia', 
    'dangphucanh', 'vothithu', 'phanquanghuy', 'huynhngocmai', 'dothanhlong', 
    'buivananh', 'hothithao', 'ngominhhai', 'duongduckhanh', 'lythanhvinh', 
    'nguyenthithuy', 'tranvandung', 'lehoangnam', 'phamthithao', 'hoangminhchau', 
    'dangquangvinh', 'vovanthang', 'phanthingoc', 'huynhvanlong', 'dothithu', 
    'buiquanghuy', 'hovanmai', 'ngothanhdat', 'duongthithuy', 'lyvandung', 
    'nguyenhoanganh', 'tranminhhai', 'lethanhkhanh', 'phamvandat', 'hoangthithu', 
    'dangminhchau', 'vothanhvinh', 'phanquanghuy', 'huynhthithao', 'dovanlong', 
    'buithithuy', 'hovananh', 'ngothanhdat', 'duongminhhai', 'lythanhkhanh', 
    'nguyenvandung', 'tranhoangnam', 'lethithao', 'phamminhchau', 'hoangquangvinh', 
    'dangvanthang', 'vothithu', 'phanvandung', 'huynhhoanganh', 'dothanhdat', 
    'buiminhhai', 'hothanhkhanh', 'ngovananh', 'duongthithuy', 'lyhoangnam', 
    'nguyenthithao', 'tranminhchau', 'lequangvinh', 'phamvanthang', 'hoangthithu', 
    'dangvandung', 'vohoanganh', 'phanthanhdat', 'huynhminhhai', 'dothanhkhanh', 
    'buivananh', 'hothithuy', 'ngominhchau', 'duongquangvinh', 'lyvanthang', 
    'nguyenthithu', 'tranvandung', 'lehoanganh', 'phamthanhdat', 'hoangminhhai', 
    'dangthanhkhanh', 'vovananh', 'phanthithuy', 'huynhhoangnam', 'dothithao', 
    'buiminhchau', 'hoquangvinh', 'ngovanthang', 'duongthithu', 'lyvandung', 
    'nguyenminhlong', 'tranthanhvy', 'leductri', 'phamngocyen', 'hoangthanhbinh', 
    'dangthithao', 'vominhhung', 'phanvanphong', 'huynhthanhson', 'dothithuy', 
    'buiquangnam', 'hovanhoa', 'ngothanhlinh', 'duongminhtam', 'lythanhphuc', 
    'nguyenvanquan', 'tranthithu', 'lehoangduy', 'phamminhkhanh', 'hoangthanhthu', 
    'dangvanvinh', 'vothanhngoc', 'phanquangdung', 'huynhthithuy', 'dovananh', 
    'buithanhhai', 'hothanhdat', 'ngominhchau', 'duongthanhvinh', 'lyvanthang', 
    'nguyenthithu', 'tranvandung', 'lehoanganh', 'phamthanhdat', 'hoangminhhai', 
    'dangthanhkhanh', 'vovananh', 'phanthithuy', 'huynhhoangnam', 'dothithao', 
    'buiminhchau', 'hoquangvinh', 'ngovanthang', 'duongthithu', 'lyvandung', 
    'nguyenhoanganh', 'tranminhhai', 'lethanhkhanh', 'phamvandat', 'hoangthithu'
]

passw = [
'explanation1', 'hypothesize1', 'combination1', 'personality1', 'calculation1', 'destination1', 'exploration1', 'architecture1', 'university1', 'consequence1', 'possibility1', 'organization1', 'considerable1', 'protectional1', 'environment1', 'transmission1', 'measurement1', 'presentation1', 'exaggeration1', 'concentration1', 'examination1', 'illustration1', 'optimization1', 'contribution1', 'determination1', 'announcement1', 'capabilities1', 'publication1', 'observation1', 'registration1', 'expectations1', 'introduction1', 'transparency1', 'arrangement1', 'exploitation1', 'installation1', 'preparation1', 'coordination1', 'manipulation1', 'participation1', 'qualifications1', 'recognition1', 'subscription1', 'contradiction1', 'modification1', 'transmission1', 'manufacturing1', 'configuration1', 'specialities1', 'appreciation1', 'authentication1', 'collaboration1', 'communication1', 'demonstration1', 'documentation1', 'experimentation1', 'identification1', 'implementation1', 'intervention1', 'justification1', 'mathematician1', 'multiplication1', 'notification1', 'perspiration1', 'preoccupation1', 'rehabilitation1', 'representation1', 'restructuring1', 'satisfaction1', 'simplification1', 'specification1', 'stabilization1', 'standardization1', 'subordination1', 'substantiation1', 'transportation1', 'transvaluation1', 'verification1', 'visualization1', 'accommodation1', 'accountability1', 'appropriation1', 'centralization1', 'characterization1', 'confrontation1', 'congratulation1', 'decentralization1', 'determination1', 'differentiation1', 'digitalization1', 'diversification1', 'elaboration1', 'generalization1', 'harmonization1', 'instrumentation1', 'international1', 'misrepresentation1',
'explanation2', 'hypothesize2', 'combination2', 'personality2', 'calculation2', 'destination2', 'exploration2', 'architecture2', 'university2', 'consequence2', 'possibility2', 'organization2', 'considerable2', 'protectional2', 'environment2', 'transmission2', 'measurement2', 'presentation2', 'exaggeration2', 'concentration2', 'examination2', 'illustration2', 'optimization2', 'contribution2', 'determination2', 'announcement2', 'capabilities2', 'publication2', 'observation2', 'registration2', 'expectations2', 'introduction2', 'transparency2', 'arrangement2', 'exploitation2', 'installation2', 'preparation2', 'coordination2', 'manipulation2', 'participation2', 'qualifications2', 'recognition2', 'subscription2', 'contradiction2', 'modification2', 'transmission2', 'manufacturing2', 'configuration2', 'specialities2', 'appreciation2', 'authentication2', 'collaboration2', 'communication2', 'demonstration2', 'documentation2', 'experimentation2', 'identification2', 'implementation2', 'intervention2', 'justification2', 'mathematician2', 'multiplication2', 'notification2', 'perspiration2', 'preoccupation2', 'rehabilitation2', 'representation2', 'restructuring2', 'satisfaction2', 'simplification2', 'specification2', 'stabilization2', 'standardization2', 'subordination2', 'substantiation2', 'transportation2', 'transvaluation2', 'verification2', 'visualization2', 'accommodation2', 'accountability2', 'appropriation2', 'centralization2', 'characterization2', 'confrontation2', 'congratulation2', 'decentralization2', 'determination2', 'differentiation2', 'digitalization2', 'diversification2', 'elaboration2', 'generalization2', 'harmonization2', 'instrumentation2', 'international2', 'misrepresentation2',
'explanation3', 'hypothesize3', 'combination3', 'personality3', 'calculation3', 'destination3', 'exploration3', 'architecture3', 'university3', 'consequence3', 'possibility3', 'organization3', 'considerable3', 'protectional3', 'environment3', 'transmission3', 'measurement3', 'presentation3', 'exaggeration3', 'concentration3', 'examination3', 'illustration3', 'optimization3', 'contribution3', 'determination3', 'announcement3', 'capabilities3', 'publication3', 'observation3', 'registration3', 'expectations3', 'introduction3'
]

# Hàm đánh dấu proxy không hoạt động
def mark_proxy_as_failed(failed_proxy):
    proxy_file = 'proxy.txt'
    if os.path.exists(proxy_file):
        try:
            # Đọc tất cả các dòng từ file
            with open(proxy_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            # Mở file để ghi lại
            with open(proxy_file, 'w', encoding='utf-8') as file:
                for line in lines:
                    if line.strip() == failed_proxy:
                        # Đánh dấu proxy không hoạt động bằng "#FAILED: "
                        file.write(f"#FAILED: {line}")
                    else:
                        file.write(line)
                        
            print(f"Đã đánh dấu proxy không hoạt động: {failed_proxy}")
        except Exception as e:
            print(f"Lỗi khi cập nhật file proxy: {str(e)}")
            
# Hàm kiểm tra proxy có hoạt động không
def check_proxy(proxy):
    try:
        # Phân tích cú pháp proxy
        proxy_parts = proxy.split(':')
        
        if len(proxy_parts) >= 2:
            ip = proxy_parts[0]
            port = int(proxy_parts[1])
            
            # Thử kết nối socket đơn giản để kiểm tra kết nối
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)  # Timeout 3 giây
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                print(f"Proxy {proxy} hoạt động tốt")
                return True
            else:
                print(f"Proxy {proxy} không phản hồi")
                # Đánh dấu proxy không hoạt động
                mark_proxy_as_failed(proxy)
                return False
        else:
            print(f"Định dạng proxy không hợp lệ: {proxy}")
            mark_proxy_as_failed(proxy)
            return False
    except Exception as e:
        print(f"Lỗi khi kiểm tra proxy {proxy}: {str(e)}")
        # Đánh dấu proxy không hoạt động
        mark_proxy_as_failed(proxy)
        return False

# Hàm đọc proxy từ file
def get_proxy():
    proxy_file = 'proxy.txt'
    proxies = []
    
    # Kiểm tra xem file proxy có tồn tại không
    if os.path.exists(proxy_file):
        try:
            with open(proxy_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    # Bỏ qua comment và dòng trống
                    if line and not line.startswith('#'):
                        proxies.append(line)
            
            if proxies:
                # Thử các proxy cho đến khi tìm thấy một proxy hoạt động
                random.shuffle(proxies)  # Xáo trộn danh sách proxy
                for proxy in proxies:
                    if check_proxy(proxy):
                        return proxy
                
                print("Không tìm thấy proxy nào hoạt động")
                return None
        except Exception as e:
            print(f"Lỗi khi đọc file proxy: {str(e)}")
    
    # Trả về None nếu không có proxy
    return None

def domains():
    headers = {
        'Referer': 'https://mail.tm/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }
    domain =[]
    domains= requests.get('https://api.mail.tm/domains', headers=headers).json()
    if 'hydra:member' in domains:
        domain= domains['hydra:member'][0]['domain']
        return domain
    else:
        print('Lỗi khi lấy domain')
        return None
    
def stard():
    print('Đang Get Domains')
    Domains=domains()
    print(f'Đã gét Domain : {Domains}')
    time.sleep(3)
    try:
        random_Domain = random.choice(Domain)
        random_word = random.choice(passw)
        random_number = random.randint(156, 168953)    
        DOMAINUSER=f'{random_Domain}{random_number}'
        PASSUSER=f'{random_word}{random_number}'
        headers = {
            'Referer': 'https://mail.tm/',
        }
        json_data = {
            'address': f'{DOMAINUSER}@{Domains}',
            'password': f'{PASSUSER}',
        }
        response = requests.post('https://api.mail.tm/accounts', headers=headers, json=json_data)
        response_data = response.json()
        if 'address'and'id' in response_data:
            DOMAINUSER=str(DOMAINUSER+'@'+Domains)
            return DOMAINUSER,PASSUSER
        else:
            print("ID not found in response.")
            return 0
    except:
        return 0

def mxn():
    global verification_code
    global emailtm
    global emailtmpass
    
    base_url = "https://api.mail.tm"
    token_url = f"{base_url}/token"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "address": emailtm,
        "password": emailtmpass,
    }

    # Gửi yêu cầu POST
    response = requests.post(token_url, headers=headers, data=json.dumps(payload))

    # Xử lý phản hồi
    if response.status_code in [200, 201]:
        token_data = response.json()
        token = token_data.get("token")
        print(f"Token: {token}")
    else:
        print(f"Lỗi: {response.status_code} - {response.text}")

    # Thiết lập URL và headers
    base_url = "https://api.mail.tm"
    messages_url = f"{base_url}/messages?page=1"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Lấy danh sách tin nhắn
    response = requests.get(messages_url, headers=headers)

    if response.status_code == 200:
        messages_data = response.json()
        messages = messages_data.get("hydra:member", [])
        
        if messages:
            # Xác định tin nhắn mới nhất
            latest_message = messages[0]
            message_id = latest_message["id"]
            
            #  Lấy chi tiết tin nhắn
            message_url = f"{base_url}/messages/{message_id}"
            message_response = requests.get(message_url, headers=headers)
            
            if message_response.status_code == 200:
                message_details = message_response.json()
                message_text = message_details.get("text", "")
                
                # Trích xuất mã xác minh bằng regex
                match = re.search(r'\b\d{6}\b', message_text)  # Tìm chuỗi 6 chữ số
                if match:
                    verification_code = match.group(0)
                    print(verification_code)  
                    return verification_code
            
                else:
                    print("Không tìm thấy mã xác minh trong nội dung tin nhắn.")
                    return 0
            else:
                print(f"Lỗi khi lấy chi tiết tin nhắn: {message_response.status_code} - {message_response.text}")
                return 0
        else:
            print("Không có tin nhắn nào.")
            return 0
    else:
        print(f"Lỗi khi lấy danh sách tin nhắn: {response.status_code} - {response.text}")
        return 0

# Hàm ghi log proxy đã sử dụng
def log_proxy_usage(proxy, success=True):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_file = os.path.join(log_dir, 'proxy_log.txt')
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILED"
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} | {status} | Proxy: {proxy}\n")

# Hàm hiển thị thống kê proxy
def print_proxy_stats():
    log_file = os.path.join('logs', 'proxy_log.txt')
    if not os.path.exists(log_file):
        print("Chưa có thống kê proxy")
        return
        
    success_count = 0
    failed_count = 0
    proxy_stats = {}
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    parts = line.strip().split(' | ')
                    if len(parts) >= 3:
                        status = parts[1]
                        proxy_info = parts[2].replace('Proxy: ', '')
                        
                        if proxy_info not in proxy_stats:
                            proxy_stats[proxy_info] = {'success': 0, 'failed': 0}
                            
                        if status == 'SUCCESS':
                            proxy_stats[proxy_info]['success'] += 1
                            success_count += 1
                        elif status == 'FAILED':
                            proxy_stats[proxy_info]['failed'] += 1
                            failed_count += 1
                            
        print("\n===== PROXY STATS =====")
        print(f"Tổng số lần sử dụng proxy thành công: {success_count}")
        print(f"Tổng số lần sử dụng proxy thất bại: {failed_count}")
        print("\nThống kê chi tiết:")
        
        for proxy, stats in proxy_stats.items():
            total = stats['success'] + stats['failed']
            success_rate = (stats['success'] / total) * 100 if total > 0 else 0
            print(f"Proxy: {proxy} - Thành công: {stats['success']}, Thất bại: {stats['failed']}, Tỉ lệ thành công: {success_rate:.2f}%")
            
        print("======================\n")
    except Exception as e:
        print(f"Lỗi khi đọc thống kê proxy: {str(e)}")

# Lớp Worker để xử lý từng luồng đăng ký
class TiktokRegWorker:
    def __init__(self, worker_id, proxy_queue):
        self.worker_id = worker_id
        self.proxy_queue = proxy_queue
        self.logger = logging.getLogger(f"Worker-{worker_id}")
        self.emailtm = ""
        self.emailtmpass = ""
        self.verification_code = ""
        self.driver = None
        self.proxy_used = None
        
    def log(self, message):
        self.logger.info(f"[Worker-{self.worker_id}] {message}")
        
    def mark_proxy_as_failed(self, failed_proxy):
        with proxy_lock:
            proxy_file = 'proxy.txt'
            if os.path.exists(proxy_file):
                try:
                    # Đọc tất cả các dòng từ file
                    with open(proxy_file, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        
                    # Mở file để ghi lại
                    with open(proxy_file, 'w', encoding='utf-8') as file:
                        for line in lines:
                            if line.strip() == failed_proxy:
                                # Đánh dấu proxy không hoạt động bằng "#FAILED: "
                                file.write(f"#FAILED: {line}")
                            else:
                                file.write(line)
                                
                    self.log(f"Đã đánh dấu proxy không hoạt động: {failed_proxy}")
                except Exception as e:
                    self.log(f"Lỗi khi cập nhật file proxy: {str(e)}")
    
    def check_proxy(self, proxy):
        try:
            # Phân tích cú pháp proxy
            proxy_parts = proxy.split(':')
            
            if len(proxy_parts) >= 2:
                ip = proxy_parts[0]
                port = int(proxy_parts[1])
                
                # Thử kết nối socket đơn giản để kiểm tra kết nối
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)  # Timeout 3 giây
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    self.log(f"Proxy {proxy} hoạt động tốt")
                    return True
                else:
                    self.log(f"Proxy {proxy} không phản hồi")
                    # Đánh dấu proxy không hoạt động
                    self.mark_proxy_as_failed(proxy)
                    return False
            else:
                self.log(f"Định dạng proxy không hợp lệ: {proxy}")
                self.mark_proxy_as_failed(proxy)
                return False
        except Exception as e:
            self.log(f"Lỗi khi kiểm tra proxy {proxy}: {str(e)}")
            # Đánh dấu proxy không hoạt động
            self.mark_proxy_as_failed(proxy)
            return False
    
    def get_proxy(self):
        try:
            # Lấy proxy từ hàng đợi
            proxy = self.proxy_queue.get(block=False)
            if self.check_proxy(proxy):
                return proxy
            else:
                # Nếu proxy không hoạt động, thêm lại vào cuối hàng đợi
                self.proxy_queue.put(proxy)
                return None
        except queue.Empty:
            self.log("Hàng đợi proxy trống")
            return None
        
    def log_proxy_usage(self, proxy, success=True):
        with file_lock:
            log_dir = 'logs'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
                
            log_file = os.path.join(log_dir, 'proxy_log.txt')
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            status = "SUCCESS" if success else "FAILED"
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} | {status} | Proxy: {proxy} | Worker: {self.worker_id}\n")

    def domains(self):
        headers = {
            'Referer': 'https://mail.tm/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        }
        domain = []
        domains = requests.get('https://api.mail.tm/domains', headers=headers).json()
        
        if 'hydra:member' in domains:
            domain = domains['hydra:member'][0]['domain']
            return domain
        else:
            self.log('Lỗi khi lấy domain')
            return None
            
    def stard(self):
        self.log('Đang Get Domains')
        Domains = self.domains()
        self.log(f'Đã gét Domain : {Domains}')
        time.sleep(3)
        try:
            random_Domain = random.choice(Domain)
            random_word = random.choice(passw)
            random_number = random.randint(156, 168953)    
            DOMAINUSER = f'{random_Domain}{random_number}'
            PASSUSER = f'{random_word}{random_number}'
            headers = {
                'Referer': 'https://mail.tm/',
            }
            json_data = {
                'address': f'{DOMAINUSER}@{Domains}',
                'password': f'{PASSUSER}',
            }
            response = requests.post('https://api.mail.tm/accounts', headers=headers, json=json_data)
            response_data = response.json()
            if 'address' and 'id' in response_data:
                DOMAINUSER = str(DOMAINUSER + '@' + Domains)
                return DOMAINUSER, PASSUSER
            else:
                self.log("ID not found in response.")
                return 0
        except:
            return 0
            
    def mxn(self):
        base_url = "https://api.mail.tm"
        token_url = f"{base_url}/token"
        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "address": self.emailtm,
            "password": self.emailtmpass,
        }

        # Gửi yêu cầu POST
        response = requests.post(token_url, headers=headers, data=json.dumps(payload))

        # Xử lý phản hồi
        if response.status_code in [200, 201]:
            token_data = response.json()
            token = token_data.get("token")
            self.log(f"Token: {token}")
        else:
            self.log(f"Lỗi: {response.status_code} - {response.text}")
            return 0

        # Thiết lập URL và headers
        messages_url = f"{base_url}/messages?page=1"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Lấy danh sách tin nhắn
        response = requests.get(messages_url, headers=headers)

        if response.status_code == 200:
            messages_data = response.json()
            messages = messages_data.get("hydra:member", [])
            
            if messages:
                # Xác định tin nhắn mới nhất
                latest_message = messages[0]
                message_id = latest_message["id"]
                
                #  Lấy chi tiết tin nhắn
                message_url = f"{base_url}/messages/{message_id}"
                message_response = requests.get(message_url, headers=headers)
                
                if message_response.status_code == 200:
                    message_details = message_response.json()
                    message_text = message_details.get("text", "")
                    
                    # Trích xuất mã xác minh bằng regex
                    match = re.search(r'\b\d{6}\b', message_text)  # Tìm chuỗi 6 chữ số
                    if match:
                        self.verification_code = match.group(0)
                        self.log(f"Mã xác minh: {self.verification_code}")  
                        return self.verification_code
                
                    else:
                        self.log("Không tìm thấy mã xác minh trong nội dung tin nhắn.")
                        return 0
                else:
                    self.log(f"Lỗi khi lấy chi tiết tin nhắn: {message_response.status_code} - {message_response.text}")
                    return 0
            else:
                self.log("Không có tin nhắn nào.")
                return 0
        else:
            self.log(f"Lỗi khi lấy danh sách tin nhắn: {response.status_code} - {response.text}")
            return 0
            
    def save_account(self, email, email_pass, tiktok_pass):
        with file_lock:
            with open('TK.txt', "a", encoding='utf-8') as file:
                file.write(f"{email}|{email_pass} | pass tiktk: {tiktok_pass} | Worker: {self.worker_id}\n")
                
    def run(self):
        try:
            self.log(f"Bắt đầu quá trình đăng ký tài khoản TikTok")
            
            # Set up Chrome options to hide automation signs
            options = ChromeOptions()
            # Disable automation detection features
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            # Set a realistic user-agent to mimic a normal browser
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

            # Thêm proxy nếu có
            proxy = self.get_proxy()
            if proxy:
                self.log(f"Sử dụng proxy: {proxy}")
                self.proxy_used = proxy
                try:
                    # Kiểm tra xem proxy có định dạng xác thực không (ip:port:username:password)
                    proxy_parts = proxy.split(':')
                    if len(proxy_parts) == 4:
                        # Proxy có xác thực
                        ip, port, username, password = proxy_parts
                        proxy_url = f"{ip}:{port}"
                        # Thêm thông tin xác thực
                        options.add_argument(f'--proxy-server={proxy_url}')
                        
                        # Thiết lập plugin để xác thực proxy
                        manifest_json = """
                        {
                            "version": "1.0.0",
                            "manifest_version": 2,
                            "name": "Chrome Proxy",
                            "permissions": [
                                "proxy",
                                "tabs",
                                "unlimitedStorage",
                                "storage",
                                "webRequest",
                                "webRequestBlocking"
                            ],
                            "background": {
                                "scripts": ["background.js"]
                            }
                        }
                        """
                        
                        background_js = """
                        var config = {
                            mode: "fixed_servers",
                            rules: {
                                singleProxy: {
                                    scheme: "http",
                                    host: "%s",
                                    port: %s
                                },
                                bypassList: ["localhost"]
                            }
                        };

                        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                        function callbackFn(details) {
                            return {
                                authCredentials: {
                                    username: "%s",
                                    password: "%s"
                                }
                            };
                        }

                        chrome.webRequest.onAuthRequired.addListener(
                            callbackFn,
                            {urls: ["<all_urls>"]},
                            ['blocking']
                        );
                        """ % (ip, port, username, password)
                        
                        plugin_dir = f'proxy_auth_plugin_{self.worker_id}'
                        if not os.path.exists(plugin_dir):
                            os.makedirs(plugin_dir)
                            
                        with open(os.path.join(plugin_dir, "manifest.json"), "w", encoding='utf-8') as f:
                            f.write(manifest_json)
                            
                        with open(os.path.join(plugin_dir, "background.js"), "w", encoding='utf-8') as f:
                            f.write(background_js)
                            
                        options.add_argument(f'--load-extension={os.path.abspath(plugin_dir)}')
                    else:
                        # Proxy không có xác thực
                        options.add_argument(f'--proxy-server={proxy}')
                    
                    # Ghi log proxy đã sử dụng
                    self.log_proxy_usage(proxy, success=True)
                except Exception as e:
                    self.log(f"Lỗi khi cấu hình proxy: {str(e)}")
                    self.log_proxy_usage(proxy, success=False)
                    # Đưa proxy này trở lại hàng đợi để thử lại sau
                    self.proxy_queue.put(proxy)
                    return False
            else:
                self.log("Không sử dụng proxy")

            # Additional options to make the browser behave naturally
            options.add_argument("--window-size=300,1000")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            # Launch Chrome with the configured options
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)

            taoenail = self.stard()
            while True: 
                if taoenail == 0:
                    taoenail = self.stard()
                else:
                    break    

            self.emailtm = taoenail[0]
            self.emailtmpass = taoenail[1]
            passtiktok = 'skytik12345@'
            
            # Hide the 'webdriver' property that Google checks
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Bắt đầu
            self.driver.get("https://www.tiktok.com/signup")
            time.sleep(3)

            # Đợi trang web tải để kiểm tra xem proxy có hoạt động không
            if "tiktok.com" not in self.driver.current_url:
                self.log("Proxy không hoạt động, đang thử proxy khác...")
                # Ghi log proxy không hoạt động
                if self.proxy_used:
                    self.log_proxy_usage(self.proxy_used, success=False)
                    self.mark_proxy_as_failed(self.proxy_used)
                    # Đưa proxy trở lại hàng đợi
                    self.proxy_queue.put(self.proxy_used)
                if self.driver:
                    self.driver.quit()
                return False

            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[1]/div/div[2]/div[2]').click()

            # Thang
            time.sleep(3)
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[2]/div[1]/div[1]').click()
            self.driver.find_element(By.ID, 'Month-options-item-6').click()
            # Ngay
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[2]/div[2]/div[1]').click()
            self.driver.find_element(By.ID, 'Day-options-item-5').click()
            # Nam
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[2]/div[3]/div[1]').click()
            h = self.driver.find_element(By.ID, 'Year-options-item-22')
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", h)
            h.click()
            time.sleep(2)
            # Click email
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[4]/a').click()
            time.sleep(2)
            EMAILTIK = self.driver.find_element(By.NAME, 'email').send_keys(f'{self.emailtm}')

            PASSTOK = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[6]/div/input').send_keys(f'{passtiktok}')

            time.sleep(2)
            # LAY MA
            send_code_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-e2e='send-code-button']"))
            )
            send_code_btn.click()
            send_code_btn.click()
            self.log("Đã click vào nút 'Send code'")
            # Nex
            time.sleep(20)
            code = self.mxn()
            while True:
                if code == 0:
                    code = self.mxn()
                else:
                    break

            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[7]/div[1]/div/input').send_keys(f'{self.verification_code}')
            time.sleep(2)
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/button').click()
            time.sleep(10)
            # Wait a few seconds to confirm login success
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[3]').click()
            self.save_account(self.emailtm, self.emailtmpass, passtiktok)
            self.log('Đăng ký tài khoản thành công')
            time.sleep(10)
            self.log("Login successful!")
            
            # Nếu đã hoàn thành thành công và đã sử dụng proxy, ghi log thành công
            if self.proxy_used:
                self.log_proxy_usage(self.proxy_used, success=True)
                # Đưa proxy trở lại hàng đợi để các luồng khác có thể sử dụng
                self.proxy_queue.put(self.proxy_used)
            
            if self.driver:
                self.driver.quit()
                
            return True

        except Exception as e:
            self.log(f'Error: {str(e)}')
            # Nếu có lỗi và đã sử dụng proxy, ghi log lỗi
            if self.proxy_used:
                self.log_proxy_usage(self.proxy_used, success=False)
                # Đưa proxy trở lại hàng đợi
                self.proxy_queue.put(self.proxy_used)
                
            if self.driver:
                self.driver.quit()
                
            self.log('Đã xảy ra lỗi, quá trình đăng ký thất bại')
            return False

# Hàm chính của chương trình
def main():
    # Hiển thị thông tin về chức năng proxy và đa luồng
    print("=== REG TIKTOK VỚI HỖ TRỢ PROXY VÀ ĐA LUỒNG FREE ===")
    print("- Proxy sẽ được đọc từ file proxy.txt")
    print("- Nếu file không tồn tại hoặc không có proxy nào, chương trình sẽ chạy không dùng proxy")
    print("- Proxy không hoạt động sẽ được đánh dấu trong file proxy.txt")
    print("- Thống kê proxy được lưu trong thư mục logs/proxy_log.txt")
    print("- Chương trình sẽ chạy đa luồng để đăng ký nhiều tài khoản cùng lúc")
    print("- TÁC GIẢ: NVL MEDIA x SKY LUXURY MEDIA")
    print("====================================\n")
    
    # Tạo thư mục logs nếu chưa tồn tại
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Đọc danh sách proxy từ file
    proxy_list = []
    proxy_file = 'proxy.txt'
    if os.path.exists(proxy_file):
        try:
            with open(proxy_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    # Bỏ qua comment và dòng trống
                    if line and not line.startswith('#'):
                        proxy_list.append(line)
            
            if proxy_list:
                print(f"Đã đọc được {len(proxy_list)} proxy từ file")
                random.shuffle(proxy_list)  # Xáo trộn danh sách proxy
        except Exception as e:
            print(f"Lỗi khi đọc file proxy: {str(e)}")
    
    # Tạo hàng đợi proxy
    proxy_queue = queue.Queue()
    for proxy in proxy_list:
        proxy_queue.put(proxy)
    
    # Yêu cầu người dùng nhập số lượng luồng
    try:
        num_threads = int(input("Nhập số lượng luồng (mặc định là 1): ") or "1")
        if num_threads < 1:
            num_threads = 1
    except ValueError:
        print("Giá trị không hợp lệ, sử dụng mặc định là 1 luồng")
        num_threads = 1
    
    # Yêu cầu người dùng nhập số lượng tài khoản cần tạo
    try:
        num_accounts = int(input("Nhập số lượng tài khoản cần tạo (mặc định là 1): ") or "1")
        if num_accounts < 1:
            num_accounts = 1
    except ValueError:
        print("Giá trị không hợp lệ, sử dụng mặc định là 1 tài khoản")
        num_accounts = 1
    
    # Thông báo số lượng luồng và tài khoản
    print(f"\nBắt đầu chạy với {num_threads} luồng để tạo {num_accounts} tài khoản")
    
    # Sử dụng ThreadPoolExecutor để quản lý các luồng
    successful_accounts = 0
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Danh sách các future (tương lai) để theo dõi kết quả
        futures = []
        
        # Tạo và bắt đầu các worker
        for i in range(num_accounts):
            worker = TiktokRegWorker(i+1, proxy_queue)
            future = executor.submit(worker.run)
            futures.append(future)
        
        # Đợi và xử lý kết quả
        for future in futures:
            try:
                result = future.result()
                if result:
                    successful_accounts += 1
            except Exception as e:
                print(f"Luồng gặp lỗi: {str(e)}")
    
    # Hiển thị kết quả cuối cùng
    print("\n====== KẾT QUẢ ======")
    print(f"Tổng số tài khoản đã tạo thành công: {successful_accounts}/{num_accounts}")
    print(f"Tỷ lệ thành công: {(successful_accounts/num_accounts)*100:.2f}%")
    print("=====================\n")
    
    # Hiển thị thống kê proxy
    print_proxy_stats()

# Bắt đầu chương trình
if __name__ == "__main__":
    main()