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
from typing import Dict, List, Optional, Tuple
import re
import requests
from bs4 import BeautifulSoup

# ======== CẤU HÌNH VIP PRO ======== #
init(autoreset=True)
os.system('cls' if os.name == 'nt' else 'clear')

class VIPConfig:
    # 🔧 Cài đặt hệ thống
    LUU_DATABASE = True           # Lưu vào SQLite database
    LUU_LOG_JSON = True           # Lưu dữ liệu vào file JSON
    AUTO_BACKUP = True            # Tự động backup dữ liệu
    MAX_LOG_FILES = 10            # Số lượng file log tối đa
    
    # 🌟 Tính năng VIP
    VOICE_READER = False          # Đọc bình luận bằng giọng nói (VIP)
    AUTO_REPLY = True             # Tự động trả lời bình luận
    ADVANCED_AI_MOD = True        # AI phát hiện spam/bot nâng cao
    REAL_TIME_STATS = True        # Hiển thị thống kê thời gian thực
    GIFT_ALERTS = True            # Thông báo quà tặng đặc biệt
    RAIN_MODE = False             # Chế độ mưa quà (VIP)
    
    # ⚙️ Cài đặt hiển thị
    HIEN_THI_THOI_GIAN = True     
    TINH_TIEN_QUA = True          
    DEM_GIO = True                
    MAX_COMMENT_LEN = 50          
    HIEN_THI_GIO_BINH_LUAN = True 
    
    # 🔒 Bảo mật
    LOC_TU_KHOA = ["mua acc", "bán", "spam", "http", "telegram", "admin", "hack", "cheat"]
    BLOCKED_USERS = []            # Danh sách user bị chặn
    ALLOWED_LANGS = ["vi", "en"]  # Ngôn ngữ cho phép
    
    # 💎 Quà VIP
    VIP_GIFTS = {
        "lion": 299000,
        "galaxy": 199000,
        "universe": 999000,
        "diamond": 50000
    }

# ======== TIỆN ÍCH VIP ======== #
class VIPUtils:
    @staticmethod
    def generate_id() -> str:
        """Tạo ID ngẫu nhiên cho session"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    @staticmethod
    def tinh_tien_qua(diamond: int) -> str:
        """Chuyển kim cương sang VNĐ với định dạng đẹp"""
        if diamond >= 1000000:
            return f"{diamond/1000000:.1f}M VNĐ"
        elif diamond >= 1000:
            return f"{diamond/1000:.1f}K VNĐ"
        return f"{diamond:,}💎"
    
    @staticmethod
    def format_thoi_gian(seconds: int) -> str:
        """Định dạng thời gian từ giây -> HH:MM:SS"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    @staticmethod
    def rut_gon_text(text: str, max_len: int = 50) -> str:
        """Rút gọn text với ... nếu quá dài"""
        if len(text) > max_len:
            return text[:max_len-3] + "..."
        return text
    
    @staticmethod
    def get_user_level(follower_count: int) -> str:
        """Xác định level người dùng theo follower"""
        if follower_count > 1000000:
            return "👑 SIÊU VIP"
        elif follower_count > 500000:
            return "💎 VIP ĐẶC BIỆT"
        elif follower_count > 100000:
            return "⭐ VIP"
        elif follower_count > 50000:
            return "🔥 PRO"
        elif follower_count > 10000:
            return "🌙 NỔI TIẾNG"
        return "🌱 MỚI"

# ======== AI MODERATOR PRO ======== #
class AIModeratorPro:
    def __init__(self):
        self.user_activity = defaultdict(lambda: {'count': 0, 'last_time': 0})
        self.recent_comments = []
        self.bad_words = self.load_bad_words()
        
    def load_bad_words(self) -> List[str]:
        """Tải danh sách từ khóa nhạy cảm từ file"""
        try:
            with open('bad_words.txt', 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines()]
        except:
            return VIPConfig.LOC_TU_KHOA
    
    def detect_spam(self, user: str, comment: str) -> bool:
        """Phát hiện spam với thuật toán nâng cao"""
        now = time.time()
        user_data = self.user_activity[user]
        
        # Reset nếu không hoạt động 15s
        if now - user_data['last_time'] > 15:
            user_data['count'] = 0
        
        # Kiểm tra hành vi spam
        user_data['count'] += 1
        user_data['last_time'] = now
        
        # 1. Quá nhiều comment trong thời gian ngắn
        if user_data['count'] > 8:
            return True
            
        # 2. Comment giống nhau nhiều lần
        if len(self.recent_comments) > 5 and comment in self.recent_comments[-5:]:
            return True
            
        # 3. Chứa từ khóa nhạy cảm
        if any(bad_word in comment.lower() for bad_word in self.bad_words):
            return True
            
        # 4. Link hoặc email
        if re.search(r'http[s]?://|www\.|@\S+\.\S+', comment):
            return True
            
        self.recent_comments.append(comment)
        return False

# ======== QUẢN LÝ LIVESTREAM PRO ======== #
class LiveManagerPro:
    def __init__(self):
        self.session_id = VIPUtils.generate_id()
        self.start_time = time.time()
        self.stats = {
            'gifts': defaultdict(int),
            'total_value': 0,
            'likes': 0,
            'follows': 0,
            'shares': 0,
            'views': 0,
            'comments': 0
        }
        self.top_donors = {}
        self.gift_history = []
        self.vip_users = set()
        
        if VIPConfig.LUU_DATABASE:
            self.init_database()
    
    def init_database(self):
        """Khởi tạo database SQLite"""
        self.conn = sqlite3.connect('tiktok_live.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                room_id TEXT,
                start_time TEXT,
                duration INTEGER,
                total_gifts INTEGER,
                total_value INTEGER,
                total_likes INTEGER,
                total_follows INTEGER,
                total_shares INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS gifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                gift_name TEXT,
                gift_value INTEGER,
                sender TEXT,
                timestamp TEXT,
                FOREIGN KEY(session_id) REFERENCES sessions(session_id)
            )
        ''')
        self.conn.commit()
    
    def record_gift(self, gift_name: str, value: int, sender: str):
        """Ghi nhận quà tặng vào hệ thống"""
        self.stats['gifts'][gift_name] += value
        self.stats['total_value'] += value
        self.gift_history.append({
            'time': time.time(),
            'gift': gift_name,
            'value': value,
            'sender': sender
        })
        
        # Cập nhật top người tặng
        if sender not in self.top_donors:
            self.top_donors[sender] = 0
        self.top_donors[sender] += value
        
        # Kiểm tra quà VIP
        if gift_name.lower() in VIPConfig.VIP_GIFTS:
            self.vip_users.add(sender)
            
        # Lưu vào database nếu enabled
        if VIPConfig.LUU_DATABASE:
            self.cursor.execute('''
                INSERT INTO gifts (session_id, gift_name, gift_value, sender, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.session_id, gift_name, value, sender, datetime.now().isoformat()))
            self.conn.commit()
    
    def get_live_duration(self) -> str:
        """Lấy thời lượng live"""
        return VIPUtils.format_thoi_gian(int(time.time() - self.start_time))
    
    def get_gifts_per_minute(self, minutes: int = 1) -> List[Dict]:
        """Lấy danh sách quà trong N phút gần nhất"""
        cutoff = time.time() - minutes * 60
        return [g for g in self.gift_history if g['time'] >= cutoff]
    
    def save_session(self):
        """Lưu thông tin session vào database"""
        if not VIPConfig.LUU_DATABASE:
            return
            
        duration = int(time.time() - self.start_time)
        self.cursor.execute('''
            INSERT INTO sessions (
                session_id, room_id, start_time, duration,
                total_gifts, total_value, total_likes,
                total_follows, total_shares
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.session_id, client.unique_id,
            datetime.fromtimestamp(self.start_time).isoformat(),
            duration, sum(self.stats['gifts'].values()),
            self.stats['total_value'], self.stats['likes'],
            self.stats['follows'], self.stats['shares']
        ))
        self.conn.commit()

# ======== HỆ THỐNG TƯƠNG TÁC TỰ ĐỘNG ======== #
class AutoInteraction:
    def __init__(self):
        self.last_reply_time = 0
        self.reply_cooldown = 30  # 30s giữa các lần reply
        self.common_questions = {
            "hello": "Xin chào bạn! Cảm ơn đã tham gia livestream ❤️",
            "tên gì": "Mình là Bot trợ lý livestream nha ^^",
            "khỏe không": "Mình khỏe lắm, cảm ơn bạn đã quan tâm 😊",
            "kết bạn": "Kết bạn với mình qua Facebook nhé: fb.com/example",
            "instagram": "Follow mình trên Instagram @example nhé!",
            "youtube": "Đăng ký kênh YouTube của mình nha: youtube.com/example"
        }
    
    def should_reply(self, comment: str, user: str) -> bool:
        """Xác định có nên trả lời bình luận không"""
        if time.time() - self.last_reply_time < self.reply_cooldown:
            return False
            
        comment_lower = comment.lower()
        for keyword in self.common_questions:
            if keyword in comment_lower:
                return True
                
        # Trả lời khi được tag hoặc hỏi trực tiếp
        if "@bot" in comment_lower or "bot ơi" in comment_lower:
            return True
            
        return False
    
    def generate_reply(self, comment: str) -> str:
        """Tạo câu trả lời tự động"""
        comment_lower = comment.lower()
        for keyword, reply in self.common_questions.items():
            if keyword in comment_lower:
                return reply
                
        # Trả lời mặc định
        replies = [
            "Cảm ơn bạn đã bình luận!",
            "Bạn muốn hỏi gì nào?",
            "Mình đã ghi nhận bình luận của bạn ❤️",
            "Livestream đang rất vui, cùng tham gia nhé!",
            "Bạn có thể gửi câu hỏi chi tiết hơn không?"
        ]
        return random.choice(replies)

# ======== GIAO DIỆN VIP ======== #
class VIPInterface:
    @staticmethod
    def show_banner():
        """Hiển thị banner đẹp mắt"""
        f = Figlet(font='slant')
        print(Fore.MAGENTA + f.renderText('VIP PRO'))
        print(Fore.CYAN + "═" * 70)
        print(Fore.YELLOW + "🌟 CÔNG CỤ THEO DÕI TIKTOK LIVE VIP PRO - BẢN ĐỘC QUYỀN 🌟")
        print(Fore.CYAN + "═" * 70)
        print(Fore.GREEN + "🔥 TÍNH NĂNG VIP:")
        print(Fore.WHITE + "  👑 Hệ thống AI chống spam thông minh đa tầng")
        print(Fore.WHITE + "  💎 Thống kê quà tặng theo thời gian thực + Database")
        print(Fore.WHITE + "  🛡️ Hệ thống lọc từ khóa nâng cao + User block")
        print(Fore.WHITE + "  🤖 Tự động trả lời bình luận thông minh")
        print(Fore.WHITE + "  📊 Báo cáo chi tiết đa dạng + Xuất Excel")
        print(Fore.WHITE + "  ⚡ Tối ưu hiệu năng cao cấp")
        print(Fore.CYAN + "═" * 70 + Style.RESET_ALL)
    
    @staticmethod
    def show_gift_alert(gift_name: str, sender: str, value: int):
        """Hiển thị thông báo quà VIP"""
        alert_box = [
            "╔════════════════════════════════════════════════╗",
            f"║   🎁  {Fore.YELLOW}QUÀ VIP ĐẶC BIỆT!{Style.RESET_ALL}   🎁  ║",
            "╟────────────────────────────────────────────────╢",
            f"║ {Fore.CYAN}Người gửi:{Style.RESET_ALL} {sender:<30} ║",
            f"║ {Fore.MAGENTA}Loại quà:{Style.RESET_ALL} {gift_name:<30} ║",
            f"║ {Fore.GREEN}Giá trị:{Style.RESET_ALL} {VIPUtils.tinh_tien_qua(value):<30} ║",
            "╚════════════════════════════════════════════════╝"
        ]
        for line in alert_box:
            print(line)
    
    @staticmethod
    def show_real_time_stats(manager: LiveManagerPro):
        """Hiển thị thống kê thời gian thực"""
        duration = manager.get_live_duration()
        total_gifts = sum(manager.stats['gifts'].values())
        total_value = manager.stats['total_value']
        
        stats_box = [
            "╔════════════════════════════════════════════════╗",
            f"║   📊  {Fore.YELLOW}THỐNG KÊ THỜI GIAN THỰC{Style.RESET_ALL}   📊  ║",
            "╟────────────────────────────────────────────────╢",
            f"║ {Fore.CYAN}Thời lượng:{Style.RESET_ALL} {duration:<30} ║",
            f"║ {Fore.MAGENTA}Tổng quà:{Style.RESET_ALL} {total_gifts:<30} ║",
            f"║ {Fore.GREEN}Tổng giá trị:{Style.RESET_ALL} {VIPUtils.tinh_tien_qua(total_value):<30} ║",
            f"║ {Fore.BLUE}Likes:{Style.RESET_ALL} {manager.stats['likes']:<30} ║",
            f"║ {Fore.CYAN}Theo dõi mới:{Style.RESET_ALL} {manager.stats['follows']:<30} ║",
            "╚════════════════════════════════════════════════╝"
        ]
        for line in stats_box:
            print(line)

# ======== KHỞI TẠO HỆ THỐNG ======== #
VIPInterface.show_banner()
room_id = input(Fore.YELLOW + "🎤 Nhập ID TikTok chủ phòng (Bỏ @): " + Style.RESET_ALL)

# Khởi tạo các thành phần
client = TikTokLiveClient(unique_id=room_id)
manager = LiveManagerPro()
ai_mod = AIModeratorPro()
auto_interact = AutoInteraction() if VIPConfig.AUTO_REPLY else None

# ======== XỬ LÝ SỰ KIỆN VIP ======== #
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"\n{Fore.GREEN}✅ Đã kết nối đến: {Fore.CYAN}@{event.unique_id}")
    print(f"{Fore.YELLOW}⏳ Đang lấy dữ liệu live...\n{Fore.CYAN}═" * 70)
    if VIPConfig.REAL_TIME_STATS:
        threading.Thread(target=show_periodic_stats, daemon=True).start()

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    gift = event.gift
    quantity = event.repeat_count if gift.streakable else 1
    total_value = gift.diamond_count * quantity
    
    # Ghi nhận quà
    manager.record_gift(gift.name, total_value, event.user.nickname)
    
    # Hiển thị thông tin
    time_prefix = f"{Fore.BLACK}[{datetime.now().strftime('%H:%M:%S')}] " if VIPConfig.HIEN_THI_THOI_GIAN else ""
    value_display = f"{Fore.CYAN}{VIPUtils.tinh_tien_qua(total_value)}" if VIPConfig.TINH_TIEN_QUA else ""
    
    # Kiểm tra quà VIP
    if gift.name.lower() in VIPConfig.VIP_GIFTS and VIPConfig.GIFT_ALERTS:
        VIPInterface.show_gift_alert(gift.name, event.user.nickname, total_value)
    else:
        print(f"{time_prefix}{Fore.YELLOW}🎁 {event.user.nickname} "
              f"{Fore.MAGENTA}tặng {gift.name} x{quantity} "
              f"{value_display}")

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    user = event.user.nickname
    comment = event.comment
    
    # Kiểm tra spam/bot
    if VIPConfig.ADVANCED_AI_MOD and ai_mod.detect_spam(user, comment):
        time_prefix = f"{Fore.BLACK}[{datetime.now().strftime('%H:%M:%S')}] " if VIPConfig.HIEN_THI_GIO_BINH_LUAN else ""
        print(f"{time_prefix}{Fore.RED}🚫 Bot/Spam: {user}: {VIPUtils.rut_gon_text(comment, VIPConfig.MAX_COMMENT_LEN)}")
        return
    
    # Tự động trả lời
    if VIPConfig.AUTO_REPLY and auto_interact.should_reply(comment, user):
        reply = auto_interact.generate_reply(comment)
        print(f"{Fore.BLACK}[{datetime.now().strftime('%H:%M:%S')}] {Fore.GREEN}🤖 AUTO REPLY: {reply}")
        auto_interact.last_reply_time = time.time()
    
    # Hiển thị bình luận
    time_prefix = f"{Fore.BLACK}[{datetime.now().strftime('%H:%M:%S')}] " if VIPConfig.HIEN_THI_GIO_BINH_LUAN else ""
    user_level = VIPUtils.get_user_level(event.user.follower_count)
    print(f"{time_prefix}{Fore.BLUE}{user_level} {user}: {Fore.GREEN}{VIPUtils.rut_gon_text(comment, VIPConfig.MAX_COMMENT_LEN)}")

@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    manager.stats['likes'] += event.count
    time_prefix = f"{Fore.BLACK}[{datetime.now().strftime('%H:%M:%S')}] " if VIPConfig.HIEN_THI_THOI_GIAN else ""
    print(f"{time_prefix}{Fore.YELLOW}❤️ {event.user.nickname} thả {event.count} like | Tổng: {manager.stats['likes']}")

@client.on(FollowEvent)
async def on_follow(event: FollowEvent):
    manager.stats['follows'] += 1
    time_prefix = f"{Fore.BLACK}[{datetime.now().strftime('%H:%M:%S')}] " if VIPConfig.HIEN_THI_THOI_GIAN else ""
    print(f"{time_prefix}{Fore.CYAN}✨ {event.user.nickname} đã theo dõi | Tổng: {manager.stats['follows']}")

@client.on(ShareEvent)
async def on_share(event: ShareEvent):
    manager.stats['shares'] += 1
    time_prefix = f"{Fore.BLACK}[{datetime.now().strftime('%H:%M:%S')}] " if VIPConfig.HIEN_THI_THOI_GIAN else ""
    print(f"{time_prefix}{Fore.MAGENTA}🔄 {event.user.nickname} đã chia sẻ | Tổng: {manager.stats['shares']}")

@client.on(JoinEvent)
async def on_join(event: JoinEvent):
    time_prefix = f"{Fore.BLACK}[{datetime.now().strftime('%H:%M:%S')}] " if VIPConfig.HIEN_THI_THOI_GIAN else ""
    print(f"{time_prefix}{Fore.GREEN}👋 {event.user.nickname} đã vào phòng")

# ======== TIỆN ÍCH BỔ SUNG ======== #
def show_periodic_stats():
    """Hiển thị thống kê định kỳ"""
    while True:
        time.sleep(60)  # Mỗi phút hiển thị 1 lần
        if VIPConfig.REAL_TIME_STATS:
            VIPInterface.show_real_time_stats(manager)

def backup_data():
    """Tự động backup dữ liệu"""
    if not VIPConfig.AUTO_BACKUP:
        return
        
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup database
    if VIPConfig.LUU_DATABASE:
        backup_file = os.path.join(backup_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        with open(backup_file, 'wb') as f:
            for line in manager.conn.iterdump():
                f.write(f'{line}\n'.encode('utf-8'))
    
    # Backup logs
    if VIPConfig.LUU_LOG_JSON:
        log_data = {
            "session_id": manager.session_id,
            "room_id": room_id,
            "stats": manager.stats,
            "top_donors": dict(sorted(manager.top_donors.items(), key=lambda x: x[1], reverse=True)[:10]),
            "timestamp": datetime.now().isoformat()
        }
        backup_file = os.path.join(backup_dir, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=4, ensure_ascii=False)

# ======== CHẠY CHƯƠNG TRÌNH ======== #
if __name__ == "__main__":
    try:
        print(f"\n{Fore.YELLOW}🔄 Đang kết nối...{Style.RESET_ALL}")
        
        # Bắt đầu các tiến trình nền
        if VIPConfig.AUTO_BACKUP:
            threading.Thread(target=backup_data, daemon=True).start()
        
        client.run()
        
    except KeyboardInterrupt:
        # Lưu dữ liệu khi dừng
        manager.save_session()
        if VIPConfig.LUU_DATABASE:
            manager.conn.close()
        
        # Hiển thị báo cáo tổng kết
        print(f"\n{Fore.RED}⛔ Đã dừng chương trình")
        print(f"{Fore.CYAN}📊 BÁO CÁO TỔNG KẾT VIP:")
        print(f"⏱️ Thời lượng live: {manager.get_live_duration()}")
        print(f"🎁 Tổng quà: {sum(manager.stats['gifts'].values()):,} (Trị giá: {VIPUtils.tinh_tien_qua(manager.stats['total_value'])})")
        print(f"❤️ Tổng like: {manager.stats['likes']:,}")
        print(f"✨ Tổng theo dõi mới: {manager.stats['follows']:,}")
        print(f"🔄 Tổng chia sẻ: {manager.stats['shares']:,}")
        
        # Top 3 người tặng quà
        print(f"\n{Fore.YELLOW}🏆 TOP NGƯỜI TẶNG QUÀ:")
        top_donors = sorted(manager.top_donors.items(), key=lambda x: x[1], reverse=True)[:3]
        for i, (user, amount) in enumerate(top_donors, 1):
            print(f"  {i}. {Fore.CYAN}{user}: {Fore.GREEN}{VIPUtils.tinh_tien_qua(amount)}")
        
        # Quà được tặng nhiều nhất
        print(f"\n{Fore.MAGENTA}🎯 QUÀ PHỔ BIẾN NHẤT:")
        top_gifts = sorted(manager.stats['gifts'].items(), key=lambda x: x[1], reverse=True)[:3]
        for gift, count in top_gifts:
            print(f"  - {gift}: {count:,} lần")
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ LỖI VIP: {e}")
        if VIPConfig.LUU_DATABASE:
            manager.conn.close()