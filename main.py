import tkinter as tk
import sys
from login_ui import LoginUI
from main_ui import MainUI
from user_manager import UserManager

def start_app():
    """
    Khởi động ứng dụng
    """
    # Tạo cửa sổ chính
    root = tk.Tk()
    
    # Thiết lập biểu tượng và tiêu đề
    root.title("Đăng Nhập - Hệ Thống Quản Lý Khách Hàng")
    root.geometry("400x300")
    
    # Tạo đối tượng quản lý người dùng
    user_manager = UserManager()
    
    # Hàm callback khi đăng nhập thành công
    def on_login_success():
        # Đóng cửa sổ đăng nhập
        root.destroy()
        
        # Tạo cửa sổ chính của ứng dụng
        main_root = tk.Tk()
        MainUI(main_root, user_manager)
        main_root.mainloop()
    
    # Tạo giao diện đăng nhập
    LoginUI(root, user_manager, on_login_success)
    
    # Chạy ứng dụng
    root.mainloop()

def restart_app():
    """
    Khởi động lại ứng dụng
    """
    python = sys.executable
    # Đối với các ứng dụng đã đóng gói, có thể cần xử lý khác
    try:
        import os
        os.execl(python, python, *sys.argv)
    except:
        # Nếu không thể khởi động lại, chỉ cần khởi động mới
        start_app()

if __name__ == "__main__":
    start_app() 