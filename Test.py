# ████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗   ██╗   ██╗██╗██████╗ 
# ╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝   ██║   ██║██║██╔══██╗
#    ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝    ██║   ██║██║██████╔╝
#    ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗    ╚██╗ ██╔╝██║██╔═══╝ 
#    ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗    ╚████╔╝ ██║██║     
#    ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝     ╚═══╝  ╚═╝╚═╝     
#                                                                      
#  ██████╗ ██████╗  ██████╗      ██████╗ ██████╗ ██╗███╗   ██╗███████╗
# ██╔═══██╗██╔══██╗██╔═══██╗    ██╔════╝██╔═══██╗██║████╗  ██║██╔════╝
# ██║   ██║██████╔╝██║   ██║    ██║     ██║   ██║██║██╔██╗ ██║█████╗  
# ██║   ██║██╔═══╝ ██║   ██║    ██║     ██║   ██║██║██║╚██╗██║██╔══╝  
# ╚██████╔╝██║     ╚██████╔╝    ╚██████╗╚██████╔╝██║██║ ╚████║███████╗
#  ╚═════╝ ╚═╝      ╚═════╝      ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝

from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent, JoinEvent, LikeEvent, ShareEvent, FollowEvent
from colorama import Fore, Style, init
import asyncio
import os
import json
from datetime import datetime
import time
from pyfiglet import Figlet
import threading
from collections import defaultdict
import random
import string
import sqlite3
import queue

# ======== CẤU HÌNH HỆ THỐNG ======== #
init(autoreset=True)
os.system('cls' if os.name == 'nt' else 'clear')

class Config:
    LUU_DATABASE = True
    LUU_LOG_JSON = True
    AUTO_BACKUP = True
    BACKUP_INTERVAL = 300  # 5 phút
    MAX_LOG_FILES = 10
    
    # Cài đặt hiển thị
    HIEN_THI_THOI_GIAN = True
    TINH_TIEN_QUA = True
    MAX_COMMENT_LEN = 50
    HIEN_THI_GIO_BINH_LUAN = True
    
    # Bảo mật
    LOC_TU_KHOA = ["mua acc", "bán", "spam", "http", "telegram", "admin"]

class TienIch:
    @staticmethod
    def tinh_tien_qua(diamond: int) -> str:
        if diamond >= 1000000:
            return f"{diamond/1000000:.1f}M VNĐ"
        return f"{diamond/1000:.1f}K VNĐ" if diamond >= 1000 else f"{diamond}💎"
    
    @staticmethod
    def format_thoi_gian(seconds: int) -> str:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    @staticmethod
    def rut_gon_text(text: str, max_len: int) -> str:
        return text if len(text) <= max_len else text[:max_len-3] + "..."
    
    @staticmethod
    def lay_thoi_gian():
        # Sửa thành màu trắng
        return f"{Fore.WHITE}[{datetime.now().strftime('%H:%M:%S')}] "

class DatabaseManager:
    def __init__(self):
        self.db_queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self._db_worker, daemon=True)
        self.worker_thread.start()
        
    def _db_worker(self):
        self.conn = sqlite3.connect('tiktok_live.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_db()
        
        while True:
            task = self.db_queue.get()
            if task is None:
                break
            try:
                task()
            except Exception as e:
                print(f"{Fore.RED}❌ Lỗi database: {e}")
            self.db_queue.task_done()
            
    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                room_id TEXT,
                start_time TEXT,
                duration INTEGER,
                total_gifts INTEGER,
                total_value INTEGER
            )
        ''')
        self.conn.commit()
        
    def execute(self, query, params=None):
        self.db_queue.put(lambda: self._execute(query, params))
        
    def _execute(self, query, params):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()
        
    def close(self):
        self.db_queue.put(None)
        self.worker_thread.join()
        self.conn.close()

class QuanLyLive:
    def __init__(self):
        self.session_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.start_time = time.time()
        self.stats = {
            'gifts': defaultdict(int),
            'total_value': 0,
            'likes': 0,
            'follows': 0,
            'shares': 0
        }
        
        if Config.LUU_DATABASE:
            self.db_manager = DatabaseManager()
            self._init_db()
    
    def _init_db(self):
        self.db_manager.execute('''
            CREATE TABLE IF NOT EXISTS gifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                gift_name TEXT,
                gift_value INTEGER,
                sender TEXT,
                timestamp TEXT
            )
        ''')
    
    def them_qua(self, ten_qua: str, gia_tri: int, nguoi_gui: str):
        self.stats['gifts'][ten_qua] += gia_tri
        self.stats['total_value'] += gia_tri
        
        if Config.LUU_DATABASE:
            self.db_manager.execute(
                '''INSERT INTO gifts (session_id, gift_name, gift_value, sender, timestamp)
                VALUES (?, ?, ?, ?, ?)''',
                (self.session_id, ten_qua, gia_tri, nguoi_gui, datetime.now().isoformat())
            )
    
    def save_session(self):
        if Config.LUU_DATABASE:
            duration = int(time.time() - self.start_time)
            self.db_manager.execute(
                '''INSERT INTO sessions (session_id, room_id, start_time, duration, total_gifts, total_value)
                VALUES (?, ?, ?, ?, ?, ?)''',
                (
                    self.session_id, client.unique_id,
                    datetime.fromtimestamp(self.start_time).isoformat(),
                    duration,
                    sum(self.stats['gifts'].values()),
                    self.stats['total_value']
                )
            )
    
    def close(self):
        if Config.LUU_DATABASE:
            self.db_manager.close()

def hien_thi_banner():
    f = Figlet(font='slant')
    print(Fore.MAGENTA + f.renderText('TIKTOK LIVE'))
    print(Fore.CYAN + "═" * 70)
    print(Fore.YELLOW + "🌟 CÔNG CỤ THEO DÕI TIKTOK LIVE 🌟")
    print(Fore.CYAN + "═" * 70)

# ======== KHỞI TẠO HỆ THỐNG ======== #
hien_thi_banner()
id_phong = input(Fore.YELLOW + "🎤 Nhập ID TikTok chủ phòng (Bỏ @): " + Style.RESET_ALL)

# Khởi tạo client
client = TikTokLiveClient(unique_id=id_phong)
quan_ly = QuanLyLive()

# ======== XỬ LÝ SỰ KIỆN ======== #
@client.on(ConnectEvent)
async def ket_noi(event: ConnectEvent):
    print(f"\n{Fore.GREEN}✅ Đã kết nối đến: {Fore.CYAN}@{event.unique_id}")

@client.on(GiftEvent)
async def xu_ly_qua(event: GiftEvent):
    so_luong = event.repeat_count if event.gift.streakable else 1
    gia_tri = event.gift.diamond_count * so_luong
    
    quan_ly.them_qua(event.gift.name, gia_tri, event.user.nickname)
    
    thoi_gian = TienIch.lay_thoi_gian() if Config.HIEN_THI_THOI_GIAN else ""
    tien_vn = TienIch.tinh_tien_qua(gia_tri) if Config.TINH_TIEN_QUA else ""
    
    print(f"{thoi_gian}{Fore.YELLOW}🎁 {event.user.nickname} "
          f"{Fore.MAGENTA}tặng {event.gift.name} x{so_luong} "
          f"{Fore.CYAN}{tien_vn}")

@client.on(CommentEvent)
async def xu_ly_binh_luan(event: CommentEvent):
    thoi_gian = TienIch.lay_thoi_gian() if Config.HIEN_THI_GIO_BINH_LUAN else ""
    print(f"{thoi_gian}{Fore.BLUE}💬 {event.user.nickname}: "
          f"{Fore.GREEN}{TienIch.rut_gon_text(event.comment, Config.MAX_COMMENT_LEN)}")

@client.on(LikeEvent)
async def xu_ly_like(event: LikeEvent):
    quan_ly.stats['likes'] += event.count
    thoi_gian = TienIch.lay_thoi_gian() if Config.HIEN_THI_THOI_GIAN else ""
    print(f"{thoi_gian}{Fore.YELLOW}❤️ {event.user.nickname} thả {event.count} like | Tổng: {quan_ly.stats['likes']}")

@client.on(FollowEvent)
async def xu_ly_theo_doi(event: FollowEvent):
    quan_ly.stats['follows'] += 1
    thoi_gian = TienIch.lay_thoi_gian() if Config.HIEN_THI_THOI_GIAN else ""
    print(f"{thoi_gian}{Fore.CYAN}✨ {event.user.nickname} đã theo dõi | Tổng: {quan_ly.stats['follows']}")

@client.on(ShareEvent)
async def xu_ly_share(event: ShareEvent):
    quan_ly.stats['shares'] += 1
    thoi_gian = TienIch.lay_thoi_gian() if Config.HIEN_THI_THOI_GIAN else ""
    print(f"{thoi_gian}{Fore.MAGENTA}🔄 {event.user.nickname} đã chia sẻ | Tổng: {quan_ly.stats['shares']}")

@client.on(JoinEvent)
async def xu_ly_join(event: JoinEvent):
    thoi_gian = TienIch.lay_thoi_gian() if Config.HIEN_THI_THOI_GIAN else ""
    print(f"{thoi_gian}{Fore.GREEN}👋 {event.user.nickname} đã vào phòng")

# ======== CHẠY CHƯƠNG TRÌNH ======== #
if __name__ == "__main__":
    try:
        print(f"\n{Fore.YELLOW}🔄 Đang kết nối...{Style.RESET_ALL}")
        client.run()
    except KeyboardInterrupt:
        quan_ly.save_session()
        print(f"\n{Fore.RED}⛔ Đã dừng chương trình")
        print(f"{Fore.CYAN}📊 Tổng quà: {TienIch.tinh_tien_qua(quan_ly.stats['total_value'])}")
        print(f"{Fore.CYAN}❤️ Tổng like: {quan_ly.stats['likes']}")
        print(f"{Fore.CYAN}✨ Tổng theo dõi: {quan_ly.stats['follows']}")
        print(f"{Fore.CYAN}🔄 Tổng chia sẻ: {quan_ly.stats['shares']}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Lỗi: {e}")
    finally:
        quan_ly.close()