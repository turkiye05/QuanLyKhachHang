import tkinter as tk
from tkinter import messagebox, ttk
from user_manager import UserManager

class LoginUI:
    def __init__(self, root, user_manager, on_login_success):
        """
        Khởi tạo giao diện đăng nhập
        """
        self.root = root
        self.user_manager = user_manager
        self.on_login_success = on_login_success
        
        # Thiết lập cửa sổ đăng nhập
        self.root.title("Đăng Nhập - Hệ Thống Quản Lý Khách Hàng")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Tạo style cho các widget
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        
        # Tạo frame chính
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="ĐĂNG NHẬP HỆ THỐNG", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Frame chứa form đăng nhập
        login_frame = ttk.Frame(main_frame)
        login_frame.pack(pady=10, fill=tk.X)
        
        # Username
        username_label = ttk.Label(login_frame, text="Tên đăng nhập:")
        username_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Password
        password_label = ttk.Label(login_frame, text="Mật khẩu:")
        password_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.password_entry = ttk.Entry(login_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Login button
        login_button = ttk.Button(login_frame, text="Đăng Nhập", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Register and Forgot Password links
        links_frame = ttk.Frame(main_frame)
        links_frame.pack(fill=tk.X)
        
        # Register link
        register_label = ttk.Label(links_frame, text="Chưa có tài khoản?")
        register_label.grid(row=0, column=0, sticky=tk.W)
        
        register_link = ttk.Label(links_frame, text="Đăng ký ngay", foreground="blue", cursor="hand2")
        register_link.grid(row=0, column=1, sticky=tk.W, padx=5)
        register_link.bind("<Button-1>", self.open_register)
        
        # Forgot password link
        forgot_pw_link = ttk.Label(links_frame, text="Quên mật khẩu?", foreground="blue", cursor="hand2")
        forgot_pw_link.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        forgot_pw_link.bind("<Button-1>", self.open_forgot_password)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        footer_label = ttk.Label(footer_frame, text="© 2025 Hệ Thống Quản Lý Khách Hàng", foreground="gray")
        footer_label.pack()
        
        # Bind Enter key cho đăng nhập
        self.root.bind("<Return>", lambda event: self.login())
        
        # Focus vào ô username
        self.username_entry.focus()
    
    def login(self):
        """
        Xử lý đăng nhập
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        success, message = self.user_manager.login(username, password)
        
        if success:
            messagebox.showinfo("Thông báo", message)
            self.on_login_success()
        else:
            messagebox.showerror("Lỗi", message)
    
    def open_register(self, event):
        """
        Mở màn hình đăng ký
        """
        register_window = tk.Toplevel(self.root)
        RegisterUI(register_window, self.user_manager)
        
    def open_forgot_password(self, event):
        """
        Mở màn hình quên mật khẩu
        """
        forgot_pw_window = tk.Toplevel(self.root)
        ForgotPasswordUI(forgot_pw_window, self.user_manager)


class RegisterUI:
    def __init__(self, root, user_manager):
        """
        Khởi tạo giao diện đăng ký
        """
        self.root = root
        self.user_manager = user_manager
        
        # Thiết lập cửa sổ đăng ký
        self.root.title("Đăng Ký - Hệ Thống Quản Lý Khách Hàng")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        
        # Tạo style cho các widget
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        
        # Tạo frame chính
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="ĐĂNG KÝ TÀI KHOẢN", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Frame chứa form đăng ký
        register_frame = ttk.Frame(main_frame)
        register_frame.pack(pady=10, fill=tk.X)
        
        # Họ tên đầy đủ
        fullname_label = ttk.Label(register_frame, text="Họ tên đầy đủ:")
        fullname_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.fullname_entry = ttk.Entry(register_frame, width=30)
        self.fullname_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Username
        username_label = ttk.Label(register_frame, text="Tên đăng nhập:")
        username_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.username_entry = ttk.Entry(register_frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Password
        password_label = ttk.Label(register_frame, text="Mật khẩu:")
        password_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.password_entry = ttk.Entry(register_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Confirm Password
        confirm_password_label = ttk.Label(register_frame, text="Xác nhận mật khẩu:")
        confirm_password_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.confirm_password_entry = ttk.Entry(register_frame, width=30, show="*")
        self.confirm_password_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Register button
        register_button = ttk.Button(register_frame, text="Đăng Ký", command=self.register)
        register_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        footer_label = ttk.Label(footer_frame, text="© 2025 Hệ Thống Quản Lý Khách Hàng", foreground="gray")
        footer_label.pack()
        
        # Bind Enter key cho đăng ký
        self.root.bind("<Return>", lambda event: self.register())
        
        # Focus vào ô họ tên
        self.fullname_entry.focus()
    
    def register(self):
        """
        Xử lý đăng ký tài khoản
        """
        full_name = self.fullname_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        
        # Kiểm tra các trường dữ liệu
        if not full_name or not username or not password or not confirm_password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu và xác nhận mật khẩu không khớp!")
            return
        
        if len(password) < 6:
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
            return
        
        # Đăng ký tài khoản
        success, message = self.user_manager.register(username, password, full_name)
        
        if success:
            messagebox.showinfo("Thông báo", message)
            self.root.destroy()
        else:
            messagebox.showerror("Lỗi", message)


class ForgotPasswordUI:
    def __init__(self, root, user_manager):
        """
        Khởi tạo giao diện quên mật khẩu
        """
        self.root = root
        self.user_manager = user_manager
        
        # Thiết lập cửa sổ quên mật khẩu
        self.root.title("Quên Mật Khẩu - Hệ Thống Quản Lý Khách Hàng")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Tạo style cho các widget
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        
        # Tạo frame chính
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="KHÔI PHỤC MẬT KHẨU", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Frame chứa form khôi phục mật khẩu
        reset_frame = ttk.Frame(main_frame)
        reset_frame.pack(pady=10, fill=tk.X)
        
        # Username
        username_label = ttk.Label(reset_frame, text="Tên đăng nhập:")
        username_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.username_entry = ttk.Entry(reset_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Họ tên đầy đủ (để xác minh danh tính)
        fullname_label = ttk.Label(reset_frame, text="Họ tên đầy đủ:")
        fullname_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.fullname_entry = ttk.Entry(reset_frame, width=30)
        self.fullname_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Mật khẩu mới
        new_password_label = ttk.Label(reset_frame, text="Mật khẩu mới:")
        new_password_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.new_password_entry = ttk.Entry(reset_frame, width=30, show="*")
        self.new_password_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Xác nhận mật khẩu mới
        confirm_password_label = ttk.Label(reset_frame, text="Xác nhận mật khẩu:")
        confirm_password_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.confirm_password_entry = ttk.Entry(reset_frame, width=30, show="*")
        self.confirm_password_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Reset button
        reset_button = ttk.Button(reset_frame, text="Khôi phục mật khẩu", command=self.reset_password)
        reset_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        footer_label = ttk.Label(footer_frame, text="© 2025 Hệ Thống Quản Lý Khách Hàng", foreground="gray")
        footer_label.pack()
        
        # Bind Enter key
        self.root.bind("<Return>", lambda event: self.reset_password())
        
        # Focus vào ô username
        self.username_entry.focus()
    
    def reset_password(self):
        """
        Xử lý khôi phục mật khẩu
        """
        username = self.username_entry.get().strip()
        full_name = self.fullname_entry.get().strip()
        new_password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        
        # Kiểm tra các trường dữ liệu
        if not username or not full_name or not new_password or not confirm_password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu mới và xác nhận mật khẩu không khớp!")
            return
        
        if len(new_password) < 6:
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
            return
        
        # Khôi phục mật khẩu
        success, message = self.user_manager.reset_password(username, full_name, new_password)
        
        if success:
            messagebox.showinfo("Thông báo", message)
            self.root.destroy()
        else:
            messagebox.showerror("Lỗi", message) 