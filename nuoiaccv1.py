import asyncio
import os
import threading
import random
from tkinter import *
from tkinter import ttk, messagebox
from playwright.async_api import async_playwright

# Danh sách comment mẫu
COMMENT_LIST = [
    "Video hay quá 😍",
    "😂 chất lượng thật sự!",
    "Lướt thấy clip chất vãi!",
    "Tiktok toàn xịn thế này à?",
    "Ủa ai đây mà xinh vậy 😅"
]

stop_flag = False
PROFILE_DIR = "profiles"
os.makedirs(PROFILE_DIR, exist_ok=True)

# Thống kê real-time
stats = {
    "watched": 0,
    "liked": 0,
    "commented": 0,
    "followed": 0
}

def stop_script():
    global stop_flag
    stop_flag = True
    print("🛑 Đã yêu cầu dừng script.")

def update_stats_labels():
    if 'labels' in globals():
        labels["watched"].config(text=f"🎞️ Video đã xem: {stats['watched']}")
        labels["liked"].config(text=f"❤️ Đã Like: {stats['liked']}")
        labels["commented"].config(text=f"💬 Đã Comment: {stats['commented']}")
        labels["followed"].config(text=f"👤 Đã Follow: {stats['followed']}")

def get_profiles():
    return [f for f in os.listdir(PROFILE_DIR) if os.path.isdir(os.path.join(PROFILE_DIR, f))]

async def save_login_profile(profile_name, login_qr=True):
    path = os.path.join(PROFILE_DIR, profile_name)
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(path, headless=False)
        page = await browser.new_page()
        login_url = "https://www.tiktok.com/login/qr" if login_qr else "https://www.tiktok.com/login"
        await page.goto(login_url)
        print("🪪 Hãy đăng nhập tài khoản TikTok.")
        input("✅ Nhấn Enter sau khi đăng nhập xong...")
        await browser.close()

async def run_with_profile(profile_name, video_count, view_time, like_probability, comment_probability, follow_enabled):
    global stop_flag, stats
    stop_flag = False
    stats = {"watched": 0, "liked": 0, "commented": 0, "followed": 0}
    path = os.path.join(PROFILE_DIR, profile_name)
    log_file = open("log.txt", "w", encoding="utf-8")

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(path, headless=False)
        page = browser.pages[0] if browser.pages else await browser.new_page()
        await page.goto("https://www.tiktok.com/")

        watched = 0
        while watched < video_count and not stop_flag:
            try:
                video_url = page.url
                print(f"▶️ Video {watched + 1}: {video_url}")
                log_file.write(f"{watched + 1}. {video_url}\n")
                await asyncio.sleep(view_time)

                # ❤️ Auto Like
                try:
                    like_button = page.locator('[data-e2e="like-icon"]')
                    if await like_button.is_visible():
                        liked = await like_button.get_attribute("style")
                        if not liked or "fill: rgb(255" not in liked:
                            if random.randint(1, 100) <= like_probability:
                                await like_button.click()
                                stats["liked"] += 1
                                print("❤️ Đã Like video.")
                except Exception as e:
                    print(f"⚠️ Lỗi Like: {e}")

                # 💬 Auto Comment
                try:
                    if random.randint(1, 100) <= comment_probability:
                        comment_box = page.locator('div[contenteditable="true"]')
                        if await comment_box.is_visible():
                            comment = random.choice(COMMENT_LIST)
                            await comment_box.fill(comment)
                            await page.keyboard.press("Enter")
                            stats["commented"] += 1
                            print(f"💬 Đã comment: {comment}")
                except Exception as e:
                    print(f"⚠️ Lỗi Comment: {e}")

                # 👤 Auto Follow
                try:
                    if follow_enabled:
                        follow_btn = page.locator('button:has-text("Follow")')
                        if await follow_btn.is_visible():
                            await follow_btn.click()
                            stats["followed"] += 1
                            print("👤 Đã follow.")
                except Exception as e:
                    print(f"⚠️ Lỗi Follow: {e}")

                await page.keyboard.press("PageDown")
                watched += 1
                stats["watched"] += 1
                update_stats_labels()

                if await page.locator("text=You're all caught up").is_visible():
                    print("🎯 Hết video trong feed.")
                    break
            except Exception as e:
                print(f"⚠️ Lỗi không xác định: {e}")
                break

        print("✅ Hoàn tất lướt video.")
        await browser.close()
        log_file.close()

def start_gui():
    def start_script():
        selected_profile = profile_var.get()
        if not selected_profile:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn tài khoản!")
            return
        try:
            video_count = int(entry_count.get())
            view_time = int(scale_time.get())
            like_chance = int(scale_like.get())
            comment_chance = int(scale_comment.get())
            follow_on = follow_var.get()
            start_button.config(state=DISABLED)
            stop_button.config(state=NORMAL)
            threading.Thread(
                target=lambda: asyncio.run(run_with_profile(
                    selected_profile, video_count, view_time,
                    like_chance, comment_chance, follow_on
                )),
                daemon=True
            ).start()
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ.")

    def create_profile(login_qr=True):
        profile_name = new_profile_entry.get().strip()
        if not profile_name:
            messagebox.showwarning("Thiếu tên", "Vui lòng nhập tên tài khoản.")
            return
        if profile_name in get_profiles():
            messagebox.showwarning("Trùng tên", "Tên tài khoản đã tồn tại.")
            return
        threading.Thread(
            target=lambda: asyncio.run(save_login_profile(profile_name, login_qr)),
            daemon=True
        ).start()
        method = "mã QR" if login_qr else "thủ công"
        messagebox.showinfo("🆕 Đăng nhập", f"Đang đăng nhập '{profile_name}' bằng {method}.\nSau khi login xong, quay lại đây.")

    global labels
    root = Tk()
    root.title("TikTok Viewer – Full Tool")
    root.geometry("440x650")

    Label(root, text="👤 Chọn tài khoản TikTok:").pack(pady=5)
    profile_var = StringVar()
    profile_dropdown = ttk.Combobox(root, textvariable=profile_var, values=get_profiles())
    profile_dropdown.pack()
    Button(root, text="🔄 Làm mới danh sách", command=lambda: profile_dropdown.config(values=get_profiles())).pack(pady=2)

    Label(root, text="➕ Tạo tài khoản mới:").pack(pady=5)
    new_profile_entry = Entry(root, justify="center")
    new_profile_entry.pack()
    frame_buttons = Frame(root)
    frame_buttons.pack()
    Button(frame_buttons, text="📱 Login QR", command=lambda: create_profile(True)).pack(side=LEFT, padx=5)
    Button(frame_buttons, text="🖐️ Login tay", command=lambda: create_profile(False)).pack(side=LEFT)

    Label(root, text="🧮 Số video muốn lướt:").pack(pady=5)
    entry_count = Entry(root, justify="center")
    entry_count.insert(0, "5")
    entry_count.pack()

    Label(root, text="⏱️ Thời gian xem (giây):").pack(pady=5)
    scale_time = Scale(root, from_=1, to=15, orient=HORIZONTAL)
    scale_time.set(3)
    scale_time.pack()

    Label(root, text="❤️ Tỷ lệ Like (%):").pack(pady=5)
    scale_like = Scale(root, from_=0, to=100, orient=HORIZONTAL)
    scale_like.set(30)
    scale_like.pack()

    Label(root, text="💬 Tỷ lệ Comment (%):").pack(pady=5)
    scale_comment = Scale(root, from_=0, to=100, orient=HORIZONTAL)
    scale_comment.set(20)
    scale_comment.pack()

    follow_var = IntVar()
    follow_checkbox = Checkbutton(root, text="👤 Tự động Follow", variable=follow_var)
    follow_checkbox.pack(pady=5)

    start_button = Button(root, text="▶️ Bắt đầu", command=start_script)
    start_button.pack(pady=10)

    stop_button = Button(root, text="🛑 Dừng", command=stop_script, state=DISABLED)
    stop_button.pack()

    Label(root, text="📄 Log video đã xem: log.txt").pack(pady=10)

    Label(root, text="📊 Thống kê hoạt động:").pack(pady=10)
    labels = {
        "watched": Label(root, text="🎞️ Video đã xem: 0"),
        "liked": Label(root, text="❤️ Đã Like: 0"),
        "commented": Label(root, text="💬 Đã Comment: 0"),
        "followed": Label(root, text="👤 Đã Follow: 0")
    }
    for lbl in labels.values():
        lbl.pack()

    root.mainloop()

if __name__ == "__main__":
    start_gui()
