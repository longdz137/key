import requests
import os
import time
import random
import sys
import json
import base64
import hashlib
import socket
import socks
from threading import Thread, Lock, Semaphore
from pystyle import Colors, Colorate, Center, Box, Write, System
from fake_useragent import UserAgent
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor
import cloudscraper
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Khởi tạo
init(autoreset=True)
System.Title("Công Cụ Spam NGL VIP ULTIMATE")

class UltimateNGLSender:
    def __init__(self):
        self.lock = Lock()
        self.semaphore = Semaphore(15)  # Giới hạn luồng đồng thời
        self.session = self._init_session()
        self.sent_count = 0
        self.failed_count = 0
        self.running = True
        self.proxies = []
        self.ua = UserAgent()
        self.config = self._load_config()
        self.version = "1.9.9"
        self.driver = None
        self.captcha_solver = None
        self.thread_speed = []
        
        # Màu sắc
        self.C = {
            'R': Fore.LIGHTRED_EX,
            'G': Fore.LIGHTGREEN_EX,
            'Y': Fore.LIGHTYELLOW_EX,
            'B': Fore.LIGHTBLUE_EX,
            'M': Fore.LIGHTMAGENTA_EX,
            'C': Fore.LIGHTCYAN_EX,
            'W': Fore.LIGHTWHITE_EX
        }

    def _init_session(self):
        session = cloudscraper.create_scraper()
        session.headers.update({
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'DNT': '1',
            'Connection': 'keep-alive'
        })
        return session

    def _load_config(self):
        default_config = {
            "max_threads": 30,
            "timeout": 20,
            "retry_count": 5,
            "auto_update": True,
            "use_selenium": False,
            "anti_detect": True,
            "proxy_timeout": 10,
            "dynamic_delay": True
        }
        try:
            with open('config_ultra.json') as f:
                return {**default_config, **json.load(f)}
        except:
            return default_config

    def _save_config(self):
        with open('config_ultra.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def _setup_proxy(self, proxy=None):
        if proxy:
            try:
                ip, port, *auth = proxy.split(':')
                proxy_dict = {
                    'http': f'http://{ip}:{port}',
                    'https': f'http://{ip}:{port}'
                }
                if auth:
                    proxy_dict['http'] = f'http://{auth[0]}:{auth[1]}@{ip}:{port}'
                    proxy_dict['https'] = f'http://{auth[0]}:{auth[1]}@{ip}:{port}'
                self.session.proxies = proxy_dict
            except:
                pass

    def _init_selenium(self):
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = uc.Chrome(options=options)

    def _solve_captcha_selenium(self):
        if not self.driver:
            self._init_selenium()
        self.driver.get("https://ngl.link")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        captcha_token = self.driver.execute_script('return localStorage.getItem("captcha_token");')
        return captcha_token or "bypass_" + hashlib.md5(str(time.time()).encode()).hexdigest()

    def _generate_fingerprint(self):
        return {
            'device_id': hashlib.sha256(str(time.time()).encode()).hexdigest(),
            'screen_res': f"{random.randint(1280, 3840)}x{random.randint(720, 2160)}",
            'browser_plugins': random.choice(['Chrome PDF Viewer', 'Widevine', 'Native Client']),
            'timezone': random.choice(['GMT+7', 'GMT-5', 'GMT+0']),
            'gpu': random.choice(['NVIDIA', 'AMD', 'Intel'])
        }

    def _get_headers(self, username):
        fingerprint = self._generate_fingerprint()
        return {
            'Host': 'ngl.link',
            'User-Agent': self.ua.random,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://ngl.link',
            'Referer': f'https://ngl.link/{username}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'DNT': '1',
            'Connection': 'keep-alive',
            'X-Device-Id': fingerprint['device_id'],
            'X-Screen-Res': fingerprint['screen_res'],
            'X-Timezone': fingerprint['timezone']
        }

    def _send_request(self, username, message, proxy=None, retry=0):
        if not self.running:
            return False

        with self.semaphore:
            try:
                self._setup_proxy(proxy)
                headers = self._get_headers(username)
                data = {
                    'username': username,
                    'question': message,
                    'deviceId': headers['X-Device-Id'],
                    'gameSlug': '',
                    'referrer': '',
                    'captchaToken': self._solve_captcha_selenium() if self.config['use_selenium'] else None
                }

                start_time = time.time()
                response = self.session.post(
                    'https://ngl.link/api/submit',
                    headers=headers,
                    data=data,
                    timeout=self.config['timeout']
                )
                elapsed = time.time() - start_time

                if response.status_code == 200:
                    with self.lock:
                        self.sent_count += 1
                        self.thread_speed.append(elapsed)
                        avg_speed = sum(self.thread_speed[-10:]) / len(self.thread_speed[-10:]) if self.thread_speed else 0
                        print(f"{self.C['G']}[✓] {self.C['W']}Đã gửi: {self.C['G']}{self.sent_count} {self.C['W']}| "
                              f"Thất bại: {self.C['R']}{self.failed_count} {self.C['W']}| "
                              f"Tốc độ: {self.C['C']}{avg_speed:.2f}s {self.C['W']}| "
                              f"Luồng: {self.C['M']}{Thread.current_thread().name}")
                    return True

                else:
                    if retry < self.config['retry_count']:
                        time.sleep(1 + random.random())
                        return self._send_request(username, message, proxy, retry + 1)
                    with self.lock:
                        self.failed_count += 1
                        print(f"{self.C['R']}[✗] Lỗi HTTP {response.status_code} {self.C['W']}(Thử lại {retry + 1})")
                    return False

            except Exception as e:
                if retry < self.config['retry_count']:
                    time.sleep(1 + random.random())
                    return self._send_request(username, message, proxy, retry + 1)
                with self.lock:
                    self.failed_count += 1
                    print(f"{self.C['R']}[✗] Lỗi: {str(e)}")
                return False
            finally:
                self.session.proxies.clear()

    def _load_proxies(self, proxy_file):
        if not os.path.exists(proxy_file):
            return False
        with open(proxy_file, 'r') as f:
            self.proxies = [line.strip() for line in f if line.strip()]
        return True

    def _display_banner(self):
        System.Clear()
        banner = f"""
        {self.C['C']}╦ ╦╔═╗╦  ╔═╗╔═╗╔╦╗╔═╗╦═╗╔╦╗
        {self.C['M']}║║║║╣ ║  ║ ║╠═╣ ║ ║ ║╠╦╝ ║ 
        {self.C['Y']}╚╩╝╚═╝╩═╝╚═╝╩ ╩ ╩ ╚═╝╩╚═ ╩ 
        {self.C['G']}┌───────────────────────────────────────────┐
        {self.C['B']}│  PHIÊN BẢN VIP ULTIMATE v{self.version}   │
        {self.C['G']}└───────────────────────────────────────────┘
        {self.C['W']}• Hỗ trợ AI • Tốc độ cao • Chống phát hiện •
        {self.C['W']}• Đa luồng • Thống kê thời gian thực • Xoay proxy •
        """
        print(Center.XCenter(banner))
        print("\n")

    def _config_menu(self):
        while True:
            System.Clear()
            print(Colorate.Vertical(Colors.blue_to_purple, Center.XCenter("⚙️ MENU CẤU HÌNH ⚙️")))
            print("\n")
            for idx, (key, val) in enumerate(self.config.items()):
                print(f"{self.C['Y']}[{idx + 1}] {self.C['C']}{key}: {self.C['W']}{val}")

            print(f"\n{self.C['G']}[S] {self.C['W']}Lưu & Thoát")
            print(f"{self.C['R']}[Q] {self.C['W']}Thoát không lưu")

            choice = input(f"\n{self.C['M']}[?] Chọn tùy chọn: ").upper()

            if choice == 'S':
                self._save_config()
                return True
            elif choice == 'Q':
                return False
            elif choice.isdigit() and 0 < int(choice) <= len(self.config):
                key = list(self.config.keys())[int(choice) - 1]
                new_val = input(f"Nhập giá trị mới cho {key} (hiện tại: {self.config[key]}): ")
                try:
                    if isinstance(self.config[key], bool):
                        self.config[key] = new_val.lower() in ['true', '1', 'yes']
                    elif isinstance(self.config[key], int):
                        self.config[key] = int(new_val)
                    elif isinstance(self.config[key], float):
                        self.config[key] = float(new_val)
                    else:
                        self.config[key] = new_val
                except:
                    print(f"{self.C['R']}[!] Giá trị không hợp lệ!")

    def _start_attack(self, username, message, count, threads, delay):
        self.sent_count = 0
        self.failed_count = 0
        self.running = True
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for _ in range(count):
                proxy = random.choice(self.proxies) if self.proxies else None
                futures.append(executor.submit(
                    self._send_request, username, message, proxy
                ))
                time.sleep(delay * (0.8 + random.random() * 0.4) if self.config['dynamic_delay'] else delay)

            for future in futures:
                future.result()  # Chờ hoàn thành

        elapsed = time.time() - start_time
        print(f"\n{self.C['G']}✅ Tấn công hoàn thành sau {elapsed:.2f} giây")
        print(f"{self.C['G']}• Thành công: {self.sent_count}")
        print(f"{self.C['R']}• Thất bại: {self.failed_count}")
        print(f"{self.C['B']}• Yêu cầu/giây: {count / elapsed:.2f}")

    def run(self):
        self._display_banner()

        # Cấu hình
        if input(f"{self.C['M']}[?] Cấu hình thiết lập? (Y/N): ").upper() == 'Y':
            if not self._config_menu():
                return

        # Proxy
        if input(f"{self.C['M']}[?] Dùng proxy? (Y/N): ").upper() == 'Y':
            proxy_file = input(f"{self.C['M']}[?] Đường dẫn file proxy: ")
            if not self._load_proxies(proxy_file):
                print(f"{self.C['R']}[!] Không tìm thấy file proxy!")

        # Mục tiêu
        username = input(f"{self.C['M']}[?] Tên người dùng mục tiêu: ")
        message = input(f"{self.C['M']}[?] Nội dung tin nhắn: ")
        count = int(input(f"{self.C['M']}[?] Tổng số tin nhắn: "))
        threads = min(int(input(f"{self.C['M']}[?] Số luồng (1-{self.config['max_threads']}): ")), self.config['max_threads'])
        delay = max(float(input(f"{self.C['M']}[?] Độ trễ (1-10s): ")), 1)

        print(Colorate.Vertical(Colors.green_to_blue, "\n" + Box.DoubleCube("🚀 BẮT ĐẦU TẤN CÔNG 🚀")))
        
        try:
            self._start_attack(username, message, count, threads, delay)
        except KeyboardInterrupt:
            self.running = False
            print(f"\n{self.C['R']}[!] Dừng tấn công!")
        finally:
            if self.driver:
                self.driver.quit()

        input(f"\n{self.C['G']}[+] Nhấn ENTER để thoát...")

if __name__ == "__main__":
    try:
        tool = UltimateNGLSender()
        tool.run()
    except Exception as e:
        print(f"\n{Fore.RED}💀 LỖI NGHIÊM TRỌNG: {str(e)}")
        sys.exit(1)