import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import os
import threading
import shutil
from PIL import Image, ImageTk
import urllib.request
import io
from customer_manager import CustomerManager
from user_manager import UserManager
from data_crawler import DataCrawler

class MainUI:
    def __init__(self, root, user_manager):
        """
        Khởi tạo giao diện chính của ứng dụng
        """
        self.root = root
        self.user_manager = user_manager
        self.customer_manager = CustomerManager()
        self.data_crawler = DataCrawler()
        
        # Lưu trữ hình ảnh đã tải về
        self.image_cache = {}
        
        # Tạo thư mục lưu hình ảnh người dùng nếu chưa có
        self.user_images_dir = "user_images"
        if not os.path.exists(self.user_images_dir):
            os.makedirs(self.user_images_dir)
        
        # Thiết lập cửa sổ chính
        self.setup_main_window()
        
        # Tạo các thành phần giao diện
        self.create_menu()
        self.create_header()
        self.create_tabs()
        self.create_customer_tab()
        self.create_user_tab()
        
        # Tải dữ liệu ban đầu
        self.load_customers()
    
    def setup_main_window(self):
        """
        Thiết lập cửa sổ chính của ứng dụng
        """
        self.root.title("Hệ Thống Quản Lý Khách Hàng")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        
        # Tạo style cho các widget
        self.style = ttk.Style()
        self.style.configure("TNotebook", tabposition="n")
        self.style.configure("TButton", padding=6, font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        self.style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        self.style.configure("Treeview", font=("Arial", 10))
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    
    def create_menu(self):
        """
        Tạo menu cho ứng dụng
        """
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Menu File
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Tải dữ liệu mẫu", command=self.load_sample_data)
        file_menu.add_separator()
        file_menu.add_command(label="Đăng xuất", command=self.logout)
        file_menu.add_command(label="Thoát", command=self.root.quit)
        self.menu_bar.add_cascade(label="Tệp", menu=file_menu)
        
        # Menu Customer
        customer_menu = tk.Menu(self.menu_bar, tearoff=0)
        customer_menu.add_command(label="Thêm khách hàng", command=self.show_add_customer_form)
        customer_menu.add_command(label="Làm mới danh sách", command=self.load_customers)
        self.menu_bar.add_cascade(label="Khách hàng", menu=customer_menu)
        
        # Menu User (chỉ admin mới thấy)
        self.user_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.user_menu.add_command(label="Quản lý người dùng", command=self.show_user_tab)
        
        if self.user_manager.is_admin():
            self.menu_bar.add_cascade(label="Người dùng", menu=self.user_menu)
            
        # Menu tài khoản (dành cho tất cả người dùng)
        account_menu = tk.Menu(self.menu_bar, tearoff=0)
        account_menu.add_command(label="Thông tin cá nhân", command=self.show_current_user_profile)
        account_menu.add_command(label="Đổi mật khẩu", command=self.show_change_password_form)
        self.menu_bar.add_cascade(label="Tài khoản", menu=account_menu)
        
        # Menu Help
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Hướng dẫn sử dụng", command=self.show_help)
        help_menu.add_command(label="Thông tin ứng dụng", command=self.show_about)
        self.menu_bar.add_cascade(label="Trợ giúp", menu=help_menu)
    
    def create_header(self):
        """
        Tạo phần header cho ứng dụng
        """
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill=tk.X, pady=5)
        
        # Tên người dùng
        current_user = self.user_manager.get_current_user()
        welcome_text = f"Xin chào, {current_user.get('full_name', 'Khách')}!"
        
        welcome_label = ttk.Label(header_frame, text=welcome_text, style="Header.TLabel")
        welcome_label.pack(side=tk.LEFT)
        
        # Hiển thị vai trò
        role_text = "Quản trị viên" if self.user_manager.is_admin() else "Người dùng"
        role_label = ttk.Label(header_frame, text=f"Vai trò: {role_text}", foreground="blue")
        role_label.pack(side=tk.RIGHT)
    
    def create_tabs(self):
        """
        Tạo các tab chính của ứng dụng
        """
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tab quản lý khách hàng
        self.customer_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.customer_tab, text="Quản lý khách hàng")
        
        # Tab quản lý người dùng (chỉ hiển thị với admin)
        self.user_tab = ttk.Frame(self.tab_control)
        
        if self.user_manager.is_admin():
            self.tab_control.add(self.user_tab, text="Quản lý người dùng")
    
    def create_customer_tab(self):
        """
        Tạo giao diện tab quản lý khách hàng
        """
        # Frame tìm kiếm
        search_frame = ttk.LabelFrame(self.customer_tab, text="Tìm kiếm", padding=10)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        search_label = ttk.Label(search_frame, text="Tìm kiếm:")
        search_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        
        search_button = ttk.Button(search_frame, text="Tìm", command=self.search_customers)
        search_button.grid(row=0, column=2, padx=5, pady=5)
        
        refresh_button = ttk.Button(search_frame, text="Làm mới", command=self.load_customers)
        refresh_button.grid(row=0, column=3, padx=5, pady=5)
        
        add_button = ttk.Button(search_frame, text="Thêm mới", command=self.show_add_customer_form)
        add_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Frame danh sách khách hàng
        list_frame = ttk.LabelFrame(self.customer_tab, text="Danh sách khách hàng", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tạo Treeview để hiển thị danh sách khách hàng
        columns = ("id", "name", "email", "phone", "address", "gender", "age")
        self.customer_tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        
        # Đặt tiêu đề cho các cột
        self.customer_tree.heading("id", text="ID")
        self.customer_tree.heading("name", text="Họ tên")
        self.customer_tree.heading("email", text="Email")
        self.customer_tree.heading("phone", text="Số điện thoại")
        self.customer_tree.heading("address", text="Địa chỉ")
        self.customer_tree.heading("gender", text="Giới tính")
        self.customer_tree.heading("age", text="Tuổi")
        
        # Đặt độ rộng và căn chỉnh cho các cột
        self.customer_tree.column("id", width=80, anchor=tk.W)
        self.customer_tree.column("name", width=150, anchor=tk.W)
        self.customer_tree.column("email", width=200, anchor=tk.W)
        self.customer_tree.column("phone", width=120, anchor=tk.W)
        self.customer_tree.column("address", width=250, anchor=tk.W)
        self.customer_tree.column("gender", width=80, anchor=tk.CENTER)
        self.customer_tree.column("age", width=50, anchor=tk.CENTER)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.customer_tree.yview)
        self.customer_tree.configure(yscroll=scrollbar.set)
        
        # Đặt vị trí cho treeview và scrollbar
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind sự kiện click đúp chuột để xem chi tiết
        self.customer_tree.bind("<Double-1>", self.view_customer_details)
        
        # Tạo menu ngữ cảnh cho treeview
        self.context_menu = tk.Menu(self.customer_tree, tearoff=0)
        self.context_menu.add_command(label="Xem chi tiết", command=self.view_selected_customer)
        self.context_menu.add_command(label="Chỉnh sửa", command=self.edit_selected_customer)
        self.context_menu.add_command(label="Xóa", command=self.delete_selected_customer)
        
        # Bind chuột phải để hiển thị menu ngữ cảnh
        self.customer_tree.bind("<Button-3>", self.show_context_menu)
    
    def create_user_tab(self):
        """
        Tạo giao diện tab quản lý người dùng (chỉ admin mới thấy)
        """
        if not self.user_manager.is_admin():
            return
        
        # Frame danh sách người dùng
        user_list_frame = ttk.LabelFrame(self.user_tab, text="Danh sách người dùng", padding=10)
        user_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Button panel
        button_frame = ttk.Frame(user_list_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        add_user_button = ttk.Button(button_frame, text="Thêm người dùng", command=self.show_add_user_form)
        add_user_button.pack(side=tk.LEFT, padx=5)
        
        refresh_users_button = ttk.Button(button_frame, text="Làm mới", command=self.load_users)
        refresh_users_button.pack(side=tk.LEFT, padx=5)
        
        # Tạo Treeview để hiển thị danh sách người dùng
        columns = ("id", "username", "full_name", "role", "created_at")
        self.user_tree = ttk.Treeview(user_list_frame, columns=columns, show="headings", selectmode="browse")
        
        # Đặt tiêu đề cho các cột
        self.user_tree.heading("id", text="ID")
        self.user_tree.heading("username", text="Tên đăng nhập")
        self.user_tree.heading("full_name", text="Họ tên")
        self.user_tree.heading("role", text="Vai trò")
        self.user_tree.heading("created_at", text="Ngày tạo")
        
        # Đặt độ rộng và căn chỉnh cho các cột
        self.user_tree.column("id", width=80, anchor=tk.W)
        self.user_tree.column("username", width=150, anchor=tk.W)
        self.user_tree.column("full_name", width=200, anchor=tk.W)
        self.user_tree.column("role", width=100, anchor=tk.CENTER)
        self.user_tree.column("created_at", width=150, anchor=tk.W)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(user_list_frame, orient=tk.VERTICAL, command=self.user_tree.yview)
        self.user_tree.configure(yscroll=scrollbar.set)
        
        # Đặt vị trí cho treeview và scrollbar
        self.user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind sự kiện click đúp chuột để xem chi tiết
        self.user_tree.bind("<Double-1>", self.view_user_details)
        
        # Tạo menu ngữ cảnh cho treeview
        self.user_context_menu = tk.Menu(self.user_tree, tearoff=0)
        self.user_context_menu.add_command(label="Xem chi tiết", command=self.view_selected_user)
        self.user_context_menu.add_command(label="Chỉnh sửa", command=self.edit_selected_user)
        self.user_context_menu.add_command(label="Xóa", command=self.delete_selected_user)
        
        # Bind chuột phải để hiển thị menu ngữ cảnh
        self.user_tree.bind("<Button-3>", self.show_user_context_menu)
        
        try:
            # Tải danh sách người dùng
            self.load_users()
        except Exception as e:
            print(f"Lỗi khi tải danh sách người dùng: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải danh sách người dùng: {e}")
            # Đảm bảo file users.json tồn tại và có cấu trúc hợp lệ
            self.user_manager.save_data()
    
    def load_customers(self):
        """
        Tải danh sách khách hàng vào treeview
        """
        # Xóa tất cả các mục hiện tại
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Lấy danh sách khách hàng từ customer_manager
        customers = self.customer_manager.get_all_customers()
        
        # Thêm các khách hàng vào treeview
        for customer in customers:
            values = (
                customer.get("id", ""),
                customer.get("name", ""),
                customer.get("email", ""),
                customer.get("phone", ""),
                customer.get("address", ""),
                customer.get("gender", ""),
                customer.get("age", "")
            )
            self.customer_tree.insert("", tk.END, values=values)
    
    def search_customers(self):
        """
        Tìm kiếm khách hàng theo từ khóa
        """
        keyword = self.search_entry.get().strip()
        
        if not keyword:
            self.load_customers()
            return
        
        # Lấy kết quả tìm kiếm
        results = self.customer_manager.search_customers(keyword)
        
        # Xóa tất cả các mục hiện tại trong treeview
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Thêm kết quả tìm kiếm vào treeview
        for customer in results:
            values = (
                customer.get("id", ""),
                customer.get("name", ""),
                customer.get("email", ""),
                customer.get("phone", ""),
                customer.get("address", ""),
                customer.get("gender", ""),
                customer.get("age", "")
            )
            self.customer_tree.insert("", tk.END, values=values)
    
    def show_context_menu(self, event):
        """
        Hiển thị menu ngữ cảnh khi click chuột phải vào treeview
        """
        # Xác định vị trí click
        item = self.customer_tree.identify_row(event.y)
        
        if item:
            # Chọn dòng được click
            self.customer_tree.selection_set(item)
            # Hiển thị menu ngữ cảnh
            self.context_menu.post(event.x_root, event.y_root)
    
    def get_selected_customer_id(self):
        """
        Lấy ID của khách hàng đang được chọn trong treeview
        """
        selected_items = self.customer_tree.selection()
        
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một khách hàng!")
            return None
        
        # Lấy giá trị của cột id
        values = self.customer_tree.item(selected_items[0])["values"]
        if not values or len(values) == 0:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu khách hàng được chọn!")
            return None
            
        customer_id = values[0]
        print(f"Đã chọn khách hàng có ID: {customer_id}, có kiểu dữ liệu: {type(customer_id)}")
        return str(customer_id)  # Đảm bảo ID là dạng chuỗi
    
    def view_customer_details(self, event):
        """
        Xem chi tiết khách hàng khi click đúp chuột
        """
        self.view_selected_customer()
    
    def view_selected_customer(self):
        """
        Xem chi tiết khách hàng được chọn
        """
        customer_id = self.get_selected_customer_id()
        
        if not customer_id:
            return
        
        # In ra ID để debug
        print(f"Đang tìm khách hàng với ID: {customer_id}")
        
        # Lấy thông tin chi tiết từ customer_manager
        customer = self.customer_manager.get_customer_by_id(customer_id)
        
        if not customer:
            messagebox.showerror("Lỗi", f"Không tìm thấy thông tin khách hàng với ID: {customer_id}! \nVui lòng tải lại danh sách.")
            # Tải lại danh sách khách hàng để đảm bảo dữ liệu đồng bộ
            self.load_customers()
            return
        
        # Tạo cửa sổ hiển thị chi tiết
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Chi tiết khách hàng: {customer.get('name', '')}")
        detail_window.geometry("600x500")
        detail_window.resizable(False, False)
        
        # Frame chính
        main_frame = ttk.Frame(detail_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Chia thành 2 phần: hình ảnh và thông tin
        # Phần hình ảnh
        image_frame = ttk.LabelFrame(main_frame, text="Hình ảnh", padding=10)
        image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Tải và hiển thị hình ảnh
        image_url = customer.get("picture", "")
        image_label = ttk.Label(image_frame, text="Không có hình ảnh")
        image_label.pack(padx=10, pady=10)
        
        if image_url and image_url != "":
            # Hiển thị thông báo đang tải
            image_label.config(text="Đang tải hình ảnh...")
            # Tải hình ảnh trong một thread riêng
            threading.Thread(target=self.load_image, args=(image_url, image_label)).start()
        
        # Phần thông tin
        info_frame = ttk.LabelFrame(main_frame, text="Thông tin chi tiết", padding=10)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Hiển thị thông tin
        ttk.Label(info_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=customer.get("id", "")).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Họ tên:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=customer.get("name", "")).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=customer.get("email", "")).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Số điện thoại:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=customer.get("phone", "")).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Địa chỉ:").grid(row=4, column=0, sticky=tk.W, pady=5)
        address_label = ttk.Label(info_frame, text=customer.get("address", ""), wraplength=300)
        address_label.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Giới tính:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=customer.get("gender", "")).grid(row=5, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Tuổi:").grid(row=6, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=str(customer.get("age", ""))).grid(row=6, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Ngày tạo:").grid(row=7, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=customer.get("created_at", "")).grid(row=7, column=1, sticky=tk.W, pady=5)
        
        # Các nút
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        edit_button = ttk.Button(button_frame, text="Chỉnh sửa", 
                                command=lambda: self.edit_customer(customer_id, detail_window))
        edit_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = ttk.Button(button_frame, text="Xóa", 
                                  command=lambda: self.delete_customer(customer_id, detail_window))
        delete_button.pack(side=tk.LEFT, padx=5)
        
        close_button = ttk.Button(button_frame, text="Đóng", command=detail_window.destroy)
        close_button.pack(side=tk.RIGHT, padx=5)
    
    def load_image(self, url, label_widget):
        """
        Tải hình ảnh từ URL và hiển thị vào label
        """
        try:
            # Kiểm tra cache
            if url in self.image_cache:
                photo = self.image_cache[url]
            else:
                # Tải hình ảnh từ URL
                with urllib.request.urlopen(url) as response:
                    image_data = response.read()
                
                # Chuyển đổi thành đối tượng hình ảnh
                image = Image.open(io.BytesIO(image_data))
                
                # Thay đổi kích thước hình ảnh
                image = image.resize((150, 150), Image.LANCZOS)
                
                # Chuyển đổi thành đối tượng PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # Lưu vào cache
                self.image_cache[url] = photo
            
            # Cập nhật label
            label_widget.config(image=photo, text="")
            label_widget.image = photo  # Giữ tham chiếu đến hình ảnh
        except Exception as e:
            label_widget.config(text=f"Không thể tải hình ảnh: {e}")
    
    def load_sample_data(self):
        """
        Tải dữ liệu mẫu từ API
        """
        # Hiển thị hộp thoại nhập số lượng
        count = simpledialog.askinteger("Tải dữ liệu mẫu", "Nhập số lượng khách hàng mẫu:", 
                                      initialvalue=10, minvalue=1, maxvalue=100)
        
        if not count:
            return
        
        # Hiển thị thông báo đang tải
        messagebox.showinfo("Thông báo", f"Đang tải {count} khách hàng mẫu từ API. Vui lòng đợi...")
        
        # Tải dữ liệu trong một thread riêng
        def fetch_data():
            success, data = self.data_crawler.fetch_random_users(count)
            
            # Cập nhật UI trong main thread
            self.root.after(0, lambda: self.handle_sample_data_result(success, data))
        
        threading.Thread(target=fetch_data).start()
    
    def handle_sample_data_result(self, success, data):
        """
        Xử lý kết quả sau khi tải dữ liệu mẫu
        """
        if success:
            # Làm mới danh sách
            self.load_customers()
            
            # Thông báo thành công
            messagebox.showinfo("Thành công", f"Đã tải {len(data)} khách hàng mẫu!")
        else:
            # Thông báo lỗi
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu mẫu: {data}")
    
    def logout(self):
        """
        Đăng xuất khỏi hệ thống
        """
        # Xác nhận đăng xuất
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?")
        
        if confirm:
            self.user_manager.logout()
            self.root.destroy()
            
            # Khởi động lại ứng dụng
            from main import restart_app
            restart_app()
    
    def show_add_customer_form(self):
        """
        Hiển thị form thêm khách hàng mới
        """
        # Tạo cửa sổ form
        form_window = tk.Toplevel(self.root)
        form_window.title("Thêm khách hàng mới")
        form_window.geometry("500x500")
        form_window.resizable(False, False)
        
        # Frame chính
        main_frame = ttk.Frame(form_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="THÊM KHÁCH HÀNG MỚI", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Form nhập liệu
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Họ tên
        ttk.Label(form_frame, text="Họ tên:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame, width=40)
        name_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        email_entry = ttk.Entry(form_frame, width=40)
        email_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Số điện thoại
        ttk.Label(form_frame, text="Số điện thoại:").grid(row=2, column=0, sticky=tk.W, pady=5)
        phone_entry = ttk.Entry(form_frame, width=40)
        phone_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Địa chỉ
        ttk.Label(form_frame, text="Địa chỉ:").grid(row=3, column=0, sticky=tk.W, pady=5)
        address_entry = ttk.Entry(form_frame, width=40)
        address_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Giới tính
        ttk.Label(form_frame, text="Giới tính:").grid(row=4, column=0, sticky=tk.W, pady=5)
        gender_var = tk.StringVar(value="male")
        gender_frame = ttk.Frame(form_frame)
        gender_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(gender_frame, text="Nam", variable=gender_var, value="male").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="Nữ", variable=gender_var, value="female").pack(side=tk.LEFT, padx=5)
        
        # Tuổi
        ttk.Label(form_frame, text="Tuổi:").grid(row=5, column=0, sticky=tk.W, pady=5)
        age_spinbox = ttk.Spinbox(form_frame, from_=1, to=120, width=5)
        age_spinbox.grid(row=5, column=1, sticky=tk.W, pady=5)
        age_spinbox.set(25)
        
        # Nút lưu và hủy
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        save_button = ttk.Button(button_frame, text="Lưu", 
                               command=lambda: self.save_new_customer(
                                   name_entry.get(),
                                   email_entry.get(),
                                   phone_entry.get(),
                                   address_entry.get(),
                                   gender_var.get(),
                                   age_spinbox.get(),
                                   form_window))
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="Hủy", command=form_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def save_new_customer(self, name, email, phone, address, gender, age, window):
        """
        Lưu thông tin khách hàng mới
        """
        # Kiểm tra dữ liệu nhập vào
        if not name or not email or not phone or not address:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Lỗi", "Tuổi phải là một số nguyên!")
            return
        
        # Tạo đối tượng khách hàng mới
        new_customer = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "gender": gender,
            "age": age
        }
        
        # Thêm vào danh sách
        self.customer_manager.add_customer(new_customer)
        
        # Làm mới danh sách
        self.load_customers()
        
        # Đóng cửa sổ form
        window.destroy()
        
        # Thông báo thành công
        messagebox.showinfo("Thành công", "Đã thêm khách hàng mới!")
    
    def edit_selected_customer(self):
        """
        Chỉnh sửa khách hàng được chọn
        """
        customer_id = self.get_selected_customer_id()
        
        if not customer_id:
            return
        
        self.edit_customer(customer_id)
    
    def edit_customer(self, customer_id, parent_window=None):
        """
        Hiển thị form chỉnh sửa thông tin khách hàng
        """
        # Lấy thông tin khách hàng
        customer = self.customer_manager.get_customer_by_id(customer_id)
        
        if not customer:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin khách hàng!")
            return
        
        # Tạo cửa sổ form
        form_window = tk.Toplevel(parent_window if parent_window else self.root)
        form_window.title(f"Chỉnh sửa khách hàng: {customer.get('name', '')}")
        form_window.geometry("500x500")
        form_window.resizable(False, False)
        
        # Frame chính
        main_frame = ttk.Frame(form_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="CHỈNH SỬA THÔNG TIN KHÁCH HÀNG", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Form nhập liệu
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Họ tên
        ttk.Label(form_frame, text="Họ tên:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame, width=40)
        name_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        name_entry.insert(0, customer.get("name", ""))
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        email_entry = ttk.Entry(form_frame, width=40)
        email_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        email_entry.insert(0, customer.get("email", ""))
        
        # Số điện thoại
        ttk.Label(form_frame, text="Số điện thoại:").grid(row=2, column=0, sticky=tk.W, pady=5)
        phone_entry = ttk.Entry(form_frame, width=40)
        phone_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        phone_entry.insert(0, customer.get("phone", ""))
        
        # Địa chỉ
        ttk.Label(form_frame, text="Địa chỉ:").grid(row=3, column=0, sticky=tk.W, pady=5)
        address_entry = ttk.Entry(form_frame, width=40)
        address_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        address_entry.insert(0, customer.get("address", ""))
        
        # Giới tính
        ttk.Label(form_frame, text="Giới tính:").grid(row=4, column=0, sticky=tk.W, pady=5)
        gender_var = tk.StringVar(value=customer.get("gender", "male"))
        gender_frame = ttk.Frame(form_frame)
        gender_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(gender_frame, text="Nam", variable=gender_var, value="male").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="Nữ", variable=gender_var, value="female").pack(side=tk.LEFT, padx=5)
        
        # Tuổi
        ttk.Label(form_frame, text="Tuổi:").grid(row=5, column=0, sticky=tk.W, pady=5)
        age_spinbox = ttk.Spinbox(form_frame, from_=1, to=120, width=5)
        age_spinbox.grid(row=5, column=1, sticky=tk.W, pady=5)
        age_spinbox.set(customer.get("age", 25))
        
        # Nút lưu và hủy
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        save_button = ttk.Button(button_frame, text="Lưu", 
                               command=lambda: self.save_customer_edit(
                                   customer_id,
                                   name_entry.get(),
                                   email_entry.get(),
                                   phone_entry.get(),
                                   address_entry.get(),
                                   gender_var.get(),
                                   age_spinbox.get(),
                                   form_window,
                                   parent_window))
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="Hủy", command=form_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def save_customer_edit(self, customer_id, name, email, phone, address, gender, age, window, parent_window=None):
        """
        Lưu thông tin khách hàng đã chỉnh sửa
        """
        # Kiểm tra dữ liệu nhập vào
        if not name or not email or not phone or not address:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Lỗi", "Tuổi phải là một số nguyên!")
            return
        
        # Lấy thông tin khách hàng hiện tại
        customer = self.customer_manager.get_customer_by_id(customer_id)
        
        # Cập nhật thông tin
        updated_customer = dict(customer)  # Tạo bản sao
        updated_customer.update({
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "gender": gender,
            "age": age
        })
        
        # Lưu lại
        success = self.customer_manager.update_customer(customer_id, updated_customer)
        
        if success:
            # Làm mới danh sách
            self.load_customers()
            
            # Đóng cửa sổ form
            window.destroy()
            
            # Đóng cửa sổ chi tiết nếu có
            if parent_window:
                parent_window.destroy()
            
            # Thông báo thành công
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin khách hàng!")
        else:
            messagebox.showerror("Lỗi", "Không thể cập nhật thông tin khách hàng!")
    
    def delete_selected_customer(self):
        """
        Xóa khách hàng được chọn
        """
        customer_id = self.get_selected_customer_id()
        
        if not customer_id:
            return
        
        self.delete_customer(customer_id)
    
    def delete_customer(self, customer_id, parent_window=None):
        """
        Xóa một khách hàng
        """
        # Xác nhận xóa
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa khách hàng này?")
        
        if not confirm:
            return
        
        # Thực hiện xóa
        success = self.customer_manager.delete_customer(customer_id)
        
        if success:
            # Làm mới danh sách
            self.load_customers()
            
            # Đóng cửa sổ chi tiết nếu có
            if parent_window:
                parent_window.destroy()
            
            # Thông báo thành công
            messagebox.showinfo("Thành công", "Đã xóa khách hàng!")
        else:
            messagebox.showerror("Lỗi", "Không thể xóa khách hàng!")
    
    def show_user_tab(self):
        """
        Chuyển đến tab quản lý người dùng
        """
        if self.user_manager.is_admin():
            self.tab_control.select(1)  # Chuyển đến tab thứ 2
        else:
            messagebox.showwarning("Cảnh báo", "Bạn không có quyền truy cập chức năng này!")
    
    def show_user_context_menu(self, event):
        """
        Hiển thị menu ngữ cảnh cho treeview người dùng
        """
        if not self.user_manager.is_admin():
            return
        
        # Xác định vị trí click
        item = self.user_tree.identify_row(event.y)
        
        if item:
            # Chọn dòng được click
            self.user_tree.selection_set(item)
            # Hiển thị menu ngữ cảnh
            self.user_context_menu.post(event.x_root, event.y_root)
    
    def get_selected_user_id(self):
        """
        Lấy ID của người dùng đang được chọn
        """
        if not self.user_manager.is_admin():
            messagebox.showwarning("Cảnh báo", "Bạn không có quyền thực hiện chức năng này!")
            return None
        
        selected_items = self.user_tree.selection()
        
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một người dùng!")
            return None
        
        # Lấy giá trị của cột id
        user_id = self.user_tree.item(selected_items[0])["values"][0]
        return user_id
    
    def view_user_details(self, event):
        """
        Xem chi tiết người dùng khi click đúp chuột
        """
        self.view_selected_user()
    
    def view_selected_user(self):
        """
        Xem chi tiết người dùng được chọn
        """
        user_id = self.get_selected_user_id()
        if not user_id:
            return
        
        # Lấy thông tin người dùng
        user = self.user_manager.get_user_by_id(user_id)
        if not user:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin người dùng!")
            return
            
        # Tạo cửa sổ hiển thị chi tiết
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Chi tiết người dùng: {user.get('username', '')}")
        detail_window.geometry("600x500")
        detail_window.resizable(False, False)
        
        # Frame chính
        main_frame = ttk.Frame(detail_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="THÔNG TIN CHI TIẾT NGƯỜI DÙNG", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Chia thành 2 phần: hình ảnh và thông tin chi tiết
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Phần hình ảnh
        image_frame = ttk.LabelFrame(content_frame, text="Ảnh đại diện", padding=10, width=200)
        image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Hiển thị ảnh đại diện
        self.user_image_label = ttk.Label(image_frame, text="Không có ảnh")
        self.user_image_label.pack(padx=10, pady=10)
        
        # Kiểm tra và hiển thị ảnh
        image_path = user.get("picture", "")
        if image_path and os.path.exists(image_path):
            try:
                # Tải ảnh từ file
                image = Image.open(image_path)
                image = image.resize((150, 150), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                # Hiển thị ảnh
                self.user_image_label.config(image=photo, text="")
                self.user_image_label.image = photo
            except Exception as e:
                print(f"Lỗi khi tải ảnh: {e}")
                self.user_image_label.config(text="Không thể tải ảnh")
        
        # Nút tải ảnh đại diện mới
        is_current_user = self.user_manager.get_current_user().get('id') == user_id
        is_admin = self.user_manager.is_admin()
        
        if is_current_user or is_admin:
            upload_button = ttk.Button(image_frame, text="Tải ảnh mới", 
                                    command=lambda: self.upload_user_image(user_id))
            upload_button.pack(pady=10)
            
            # Thêm một nút tải ảnh riêng biệt vào các nút ở dưới để làm rõ hơn
            upload_image_button = ttk.Button(main_frame, text="Tải ảnh đại diện mới", 
                                          command=lambda: self.upload_user_image(user_id))
            upload_image_button.pack(side=tk.TOP, pady=5)
        
        # Frame thông tin chi tiết
        info_frame = ttk.LabelFrame(content_frame, text="Thông tin chi tiết", padding=10)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Hiển thị thông tin
        ttk.Label(info_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=user.get("id", "")).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Tên đăng nhập:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=user.get("username", "")).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Họ tên:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=user.get("full_name", "")).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Vai trò:").grid(row=3, column=0, sticky=tk.W, pady=5)
        role_text = "Quản trị viên" if user.get("role") == "admin" else "Người dùng"
        ttk.Label(info_frame, text=role_text).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Ngày tạo:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=user.get("created_at", "")).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        if "updated_at" in user:
            ttk.Label(info_frame, text="Cập nhật lần cuối:").grid(row=5, column=0, sticky=tk.W, pady=5)
            ttk.Label(info_frame, text=user.get("updated_at", "")).grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Các nút
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        edit_button = ttk.Button(button_frame, text="Chỉnh sửa thông tin", 
                               command=lambda: self.edit_user(user_id, detail_window))
        edit_button.pack(side=tk.LEFT, padx=5)
        
        password_button = ttk.Button(button_frame, text="Đổi mật khẩu", 
                                   command=lambda: self.show_change_password_form())
        password_button.pack(side=tk.LEFT, padx=5)
        
        close_button = ttk.Button(button_frame, text="Đóng", command=detail_window.destroy)
        close_button.pack(side=tk.RIGHT, padx=5)
    
    def edit_selected_user(self):
        """
        Chỉnh sửa người dùng được chọn
        """
        if not self.user_manager.is_admin():
            messagebox.showwarning("Cảnh báo", "Bạn không có quyền thực hiện chức năng này!")
            return
        
        user_id = self.get_selected_user_id()
        if not user_id:
            return
        
        self.edit_user(user_id)
    
    def edit_user(self, user_id, parent_window=None):
        """
        Hiển thị form chỉnh sửa thông tin người dùng
        """
        # Lấy thông tin người dùng
        user = self.user_manager.get_user_by_id(user_id)
        
        if not user:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin người dùng!")
            return
        
        # Kiểm tra quyền: admin có thể sửa tất cả, người dùng chỉ sửa được thông tin của mình
        current_user = self.user_manager.get_current_user()
        is_editing_self = current_user and current_user.get("id") == user_id
        
        if not self.user_manager.is_admin() and not is_editing_self:
            messagebox.showwarning("Cảnh báo", "Bạn không có quyền chỉnh sửa thông tin của người dùng khác!")
            return
        
        # Tạo cửa sổ form
        form_window = tk.Toplevel(parent_window if parent_window else self.root)
        form_window.title(f"Chỉnh sửa người dùng: {user.get('username', '')}")
        form_window.geometry("500x420")
        form_window.resizable(False, False)
        
        # Frame chính
        main_frame = ttk.Frame(form_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="CHỈNH SỬA THÔNG TIN NGƯỜI DÙNG", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Form nhập liệu
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Họ tên đầy đủ
        ttk.Label(form_frame, text="Họ tên đầy đủ:").grid(row=0, column=0, sticky=tk.W, pady=5)
        fullname_entry = ttk.Entry(form_frame, width=30)
        fullname_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        fullname_entry.insert(0, user.get("full_name", ""))
        
        # Tên đăng nhập (chỉ hiển thị, không cho phép sửa)
        ttk.Label(form_frame, text="Tên đăng nhập:").grid(row=1, column=0, sticky=tk.W, pady=5)
        username_entry = ttk.Entry(form_frame, width=30, state="readonly")
        username_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        username_entry.insert(0, user.get("username", ""))
        
        # Mật khẩu mới (tùy chọn)
        ttk.Label(form_frame, text="Mật khẩu mới:").grid(row=2, column=0, sticky=tk.W, pady=5)
        new_password_entry = ttk.Entry(form_frame, width=30, show="*")
        new_password_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Xác nhận mật khẩu mới
        ttk.Label(form_frame, text="Xác nhận mật khẩu:").grid(row=3, column=0, sticky=tk.W, pady=5)
        confirm_password_entry = ttk.Entry(form_frame, width=30, show="*")
        confirm_password_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Vai trò (chỉ admin mới thay đổi được)
        ttk.Label(form_frame, text="Vai trò:").grid(row=4, column=0, sticky=tk.W, pady=5)
        role_var = tk.StringVar(value=user.get("role", "user"))
        role_frame = ttk.Frame(form_frame)
        role_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        admin_radio = ttk.Radiobutton(role_frame, text="Quản trị viên", variable=role_var, value="admin")
        admin_radio.pack(side=tk.LEFT, padx=5)
        
        user_radio = ttk.Radiobutton(role_frame, text="Người dùng", variable=role_var, value="user")
        user_radio.pack(side=tk.LEFT, padx=5)
        
        # Vô hiệu hóa các nút radio nếu không phải admin
        if not self.user_manager.is_admin():
            admin_radio.config(state="disabled")
            user_radio.config(state="disabled")
        
        # Nút lưu và hủy
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        save_button = ttk.Button(button_frame, text="Lưu", 
                               command=lambda: self.save_user_edit(
                                   user_id,
                                   fullname_entry.get(),
                                   new_password_entry.get(),
                                   confirm_password_entry.get(),
                                   role_var.get(),
                                   form_window,
                                   parent_window))
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="Hủy", command=form_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def save_user_edit(self, user_id, full_name, new_password, confirm_password, role, window, parent_window=None):
        """
        Lưu thông tin người dùng đã chỉnh sửa
        """
        # Kiểm tra dữ liệu nhập vào
        if not full_name:
            messagebox.showerror("Lỗi", "Vui lòng nhập họ tên đầy đủ!")
            return
        
        # Kiểm tra mật khẩu nếu có nhập mới
        if new_password:
            if len(new_password) < 6:
                messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
                return
            
            if new_password != confirm_password:
                messagebox.showerror("Lỗi", "Mật khẩu mới và xác nhận mật khẩu không khớp!")
                return
        
        # Tạo dữ liệu cập nhật
        updated_data = {
            "full_name": full_name,
            "role": role
        }
        
        # Thêm mật khẩu mới nếu có
        if new_password:
            updated_data["new_password"] = new_password
        
        # Thực hiện cập nhật
        success, message = self.user_manager.update_user(user_id, updated_data)
        
        if success:
            # Làm mới danh sách người dùng
            self.load_users()
            
            # Đóng cửa sổ form
            window.destroy()
            
            # Đóng cửa sổ chi tiết nếu có
            if parent_window:
                parent_window.destroy()
            
            # Thông báo thành công
            messagebox.showinfo("Thành công", message)
        else:
            messagebox.showerror("Lỗi", message)
    
    def delete_user(self, user_id, parent_window=None):
        """
        Xóa một người dùng
        """
        if not self.user_manager.is_admin():
            messagebox.showwarning("Cảnh báo", "Bạn không có quyền thực hiện chức năng này!")
            return
        
        # Xác nhận xóa
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa người dùng này?")
        
        if not confirm:
            return
        
        # Thực hiện xóa
        success, message = self.user_manager.delete_user(user_id)
        
        if success:
            # Làm mới danh sách
            self.load_users()
            
            # Đóng cửa sổ chi tiết nếu có
            if parent_window:
                parent_window.destroy()
            
            # Thông báo thành công
            messagebox.showinfo("Thành công", message)
        else:
            messagebox.showerror("Lỗi", message)
    
    def delete_selected_user(self):
        """
        Xóa người dùng được chọn
        """
        if not self.user_manager.is_admin():
            messagebox.showwarning("Cảnh báo", "Bạn không có quyền thực hiện chức năng này!")
            return
        
        user_id = self.get_selected_user_id()
        if not user_id:
            return
        
        self.delete_user(user_id)
    
    def load_users(self):
        """
        Tải danh sách người dùng vào treeview
        """
        if not self.user_manager.is_admin():
            return
            
        # Xóa tất cả các mục hiện tại
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        try:
            # Lấy danh sách người dùng từ user_manager
            users = self.user_manager.get_all_users()
            
            print(f"Đã tải {len(users)} người dùng từ hệ thống")
            
            # Nếu không có người dùng nào, hiển thị thông báo
            if len(users) == 0:
                messagebox.showinfo("Thông báo", "Không có người dùng nào trong hệ thống! Hệ thống sẽ tạo tài khoản admin mặc định.")
                self.user_manager.create_default_admin()
                # Tải lại danh sách
                users = self.user_manager.get_all_users()
            
            # Thêm các người dùng vào treeview
            for user in users:
                values = (
                    user.get("id", ""),
                    user.get("username", ""),
                    user.get("full_name", ""),
                    "Quản trị viên" if user.get("role") == "admin" else "Người dùng",
                    user.get("created_at", "")
                )
                self.user_tree.insert("", tk.END, values=values)
                
        except Exception as e:
            print(f"Lỗi khi tải danh sách người dùng: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải danh sách người dùng: {e}")
            # Đảm bảo file users.json tồn tại và có cấu trúc hợp lệ
            self.user_manager.save_data()
    
    def show_add_user_form(self):
        """
        Hiển thị form thêm người dùng mới
        """
        if not self.user_manager.is_admin():
            messagebox.showwarning("Cảnh báo", "Bạn không có quyền thực hiện chức năng này!")
            return
        
        # Chức năng này sẽ được triển khai khi cần thiết
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển!")
    
    def show_help(self):
        """
        Hiển thị hướng dẫn sử dụng
        """
        help_text = """
        HƯỚNG DẪN SỬ DỤNG
        
        1. Quản lý khách hàng:
           - Xem danh sách khách hàng
           - Tìm kiếm khách hàng theo từ khóa
           - Thêm khách hàng mới
           - Chỉnh sửa thông tin khách hàng
           - Xóa khách hàng
           
        2. Quản lý người dùng (chỉ dành cho admin):
           - Xem danh sách người dùng
           - Thêm người dùng mới
           - Chỉnh sửa thông tin người dùng
           - Xóa người dùng
           
        3. Tải dữ liệu mẫu:
           - Tự động tải dữ liệu khách hàng mẫu từ API
        """
        
        # Hiển thị hộp thoại hướng dẫn
        messagebox.showinfo("Hướng dẫn sử dụng", help_text)
    
    def show_about(self):
        """
        Hiển thị thông tin về ứng dụng
        """
        about_text = """
        HỆ THỐNG QUẢN LÝ KHÁCH HÀNG
        
        Phiên bản: 1.0
        
        Tính năng:
        - Quản lý danh sách khách hàng
        - Quản lý người dùng với phân quyền
        - Tự động lấy dữ liệu từ API
        
        © 2025 Hệ Thống Quản Lý Khách Hàng
        """
        
        # Hiển thị hộp thoại thông tin
        messagebox.showinfo("Thông tin ứng dụng", about_text)
        
    def show_current_user_profile(self):
        """
        Hiển thị thông tin cá nhân của người dùng hiện tại
        """
        current_user = self.user_manager.get_current_user()
        if not current_user:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin người dùng!")
            return
            
        # Sử dụng phương thức view_selected_user đã được nâng cấp
        # để hiển thị thông tin cá nhân bao gồm ảnh đại diện
        user_id = current_user.get("id")
        
        # Lấy thông tin người dùng
        user = self.user_manager.get_user_by_id(user_id)
        if not user:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin người dùng!")
            return
            
        # Tạo cửa sổ hiển thị chi tiết
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Thông tin cá nhân: {user.get('username', '')}")
        detail_window.geometry("600x500")
        detail_window.resizable(False, False)
        
        # Frame chính
        main_frame = ttk.Frame(detail_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="THÔNG TIN CÁ NHÂN", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Thêm một nút tải ảnh đại diện ở trên đầu để dễ nhìn thấy
        upload_image_button = ttk.Button(main_frame, text="Tải ảnh đại diện mới", 
                                      command=lambda: self.upload_user_image(user_id))
        upload_image_button.pack(side=tk.TOP, pady=5)
        
        # Chia thành 2 phần: hình ảnh và thông tin chi tiết
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Phần hình ảnh
        image_frame = ttk.LabelFrame(content_frame, text="Ảnh đại diện", padding=10, width=200)
        image_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Hiển thị ảnh đại diện
        self.user_image_label = ttk.Label(image_frame, text="Không có ảnh")
        self.user_image_label.pack(padx=10, pady=10)
        
        # Kiểm tra và hiển thị ảnh
        image_path = user.get("picture", "")
        if image_path and os.path.exists(image_path):
            try:
                # Tải ảnh từ file
                image = Image.open(image_path)
                image = image.resize((150, 150), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                # Hiển thị ảnh
                self.user_image_label.config(image=photo, text="")
                self.user_image_label.image = photo
            except Exception as e:
                print(f"Lỗi khi tải ảnh: {e}")
                self.user_image_label.config(text="Không thể tải ảnh")
        
        # Nút tải ảnh đại diện mới
        is_current_user = self.user_manager.get_current_user().get('id') == user_id
        is_admin = self.user_manager.is_admin()
        
        if is_current_user or is_admin:
            upload_button = ttk.Button(image_frame, text="Tải ảnh mới", 
                                    command=lambda: self.upload_user_image(user_id))
            upload_button.pack(pady=10)
        
        # Frame thông tin chi tiết
        info_frame = ttk.LabelFrame(content_frame, text="Thông tin chi tiết", padding=10)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Hiển thị thông tin
        ttk.Label(info_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=user.get("id", "")).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Tên đăng nhập:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=user.get("username", "")).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Họ tên:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=user.get("full_name", "")).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Vai trò:").grid(row=3, column=0, sticky=tk.W, pady=5)
        role_text = "Quản trị viên" if user.get("role") == "admin" else "Người dùng"
        ttk.Label(info_frame, text=role_text).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Ngày tạo:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=user.get("created_at", "")).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        if "updated_at" in user:
            ttk.Label(info_frame, text="Cập nhật lần cuối:").grid(row=5, column=0, sticky=tk.W, pady=5)
            ttk.Label(info_frame, text=user.get("updated_at", "")).grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Các nút
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        edit_button = ttk.Button(button_frame, text="Chỉnh sửa thông tin", 
                               command=lambda: self.edit_user(user_id, detail_window))
        edit_button.pack(side=tk.LEFT, padx=5)
        
        password_button = ttk.Button(button_frame, text="Đổi mật khẩu", 
                                   command=lambda: self.show_change_password_form())
        password_button.pack(side=tk.LEFT, padx=5)
        
        # Nút tải ảnh đại diện
        another_upload_button = ttk.Button(button_frame, text="Tải ảnh đại diện", 
                                         command=lambda: self.upload_user_image(user_id))
        another_upload_button.pack(side=tk.LEFT, padx=5)
        
        close_button = ttk.Button(button_frame, text="Đóng", command=detail_window.destroy)
        close_button.pack(side=tk.RIGHT, padx=5)
    
    def show_change_password_form(self):
        """
        Hiển thị form đổi mật khẩu cho người dùng hiện tại
        """
        current_user = self.user_manager.get_current_user()
        if not current_user:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin người dùng!")
            return
        
        # Tạo cửa sổ đổi mật khẩu
        form_window = tk.Toplevel(self.root)
        form_window.title("Đổi mật khẩu")
        form_window.geometry("400x300")
        form_window.resizable(False, False)
        
        # Frame chính
        main_frame = ttk.Frame(form_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="ĐỔI MẬT KHẨU", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Form nhập liệu
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Mật khẩu hiện tại
        ttk.Label(form_frame, text="Mật khẩu hiện tại:").grid(row=0, column=0, sticky=tk.W, pady=5)
        current_password_entry = ttk.Entry(form_frame, width=30, show="*")
        current_password_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Mật khẩu mới
        ttk.Label(form_frame, text="Mật khẩu mới:").grid(row=1, column=0, sticky=tk.W, pady=5)
        new_password_entry = ttk.Entry(form_frame, width=30, show="*")
        new_password_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Xác nhận mật khẩu mới
        ttk.Label(form_frame, text="Xác nhận mật khẩu:").grid(row=2, column=0, sticky=tk.W, pady=5)
        confirm_password_entry = ttk.Entry(form_frame, width=30, show="*")
        confirm_password_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Các nút
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        save_button = ttk.Button(button_frame, text="Lưu thay đổi", 
                              command=lambda: self.save_password_change(
                                  current_password_entry.get(),
                                  new_password_entry.get(),
                                  confirm_password_entry.get(),
                                  form_window))
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="Hủy", command=form_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def save_password_change(self, current_password, new_password, confirm_password, window):
        """
        Lưu thay đổi mật khẩu
        """
        # Kiểm tra dữ liệu
        if not current_password or not new_password or not confirm_password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
            
        if new_password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu mới và xác nhận mật khẩu không khớp!")
            return
            
        if len(new_password) < 6:
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
            return
            
        # Lấy thông tin người dùng hiện tại
        current_user = self.user_manager.get_current_user()
        
        # Kiểm tra mật khẩu hiện tại
        hashed_current_password = self.user_manager.hash_password(current_password)
        if current_user.get("password") != hashed_current_password:
            messagebox.showerror("Lỗi", "Mật khẩu hiện tại không chính xác!")
            return
            
        # Cập nhật mật khẩu
        user_id = current_user.get("id")
        updated_data = {
            "new_password": new_password
        }
        
        success, message = self.user_manager.update_user(user_id, updated_data)
        
        if success:
            # Đóng cửa sổ
            window.destroy()
            
            # Thông báo thành công
            messagebox.showinfo("Thành công", "Đổi mật khẩu thành công!")
        else:
            messagebox.showerror("Lỗi", message)

    def upload_user_image(self, user_id):
        """
        Hiển thị form tải ảnh đại diện cho người dùng
        """
        # Tạo cửa sổ form tải ảnh
        form_window = tk.Toplevel(self.root)
        form_window.title("Tải ảnh đại diện")
        form_window.geometry("500x350")
        form_window.resizable(False, False)
        
        # Frame chính
        main_frame = ttk.Frame(form_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="TẢI ẢNH ĐẠI DIỆN", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Form nhập liệu
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Thêm hướng dẫn
        instruction_text = """
        Hướng dẫn:
        1. Nhấn nút "Chọn ảnh" để chọn file ảnh từ máy tính
        2. Chỉ hỗ trợ định dạng JPG, JPEG và PNG
        3. Ảnh sẽ tự động được thay đổi kích thước
        4. Nhấn "Hủy" để đóng cửa sổ này
        """
        instruction_label = ttk.Label(form_frame, text=instruction_text, wraplength=400, justify=tk.LEFT)
        instruction_label.pack(pady=20)
        
        # Biến để lưu trữ đường dẫn đã chọn
        self.selected_image_path = tk.StringVar()
        
        # Hiển thị đường dẫn file đã chọn
        path_frame = ttk.Frame(form_frame)
        path_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(path_frame, text="File đã chọn:").pack(side=tk.LEFT, padx=5)
        path_label = ttk.Label(path_frame, textvariable=self.selected_image_path, foreground="blue")
        path_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Nút chọn ảnh
        select_button = ttk.Button(form_frame, text="Chọn ảnh", 
                                 command=lambda: self.select_image_file(user_id, form_window))
        select_button.pack(pady=10)
        
        # Nút hủy
        cancel_button = ttk.Button(form_frame, text="Hủy", command=form_window.destroy)
        cancel_button.pack(pady=10)

    def select_image_file(self, user_id, form_window):
        """
        Hiển thị hộp thoại chọn file và xử lý file đã chọn
        """
        # Hiển thị hộp thoại chọn file
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh đại diện", 
            filetypes=[
                ("Image files", "*.jpg;*.jpeg;*.png"),
                ("JPEG files", "*.jpg;*.jpeg"),
                ("PNG files", "*.png")
            ]
        )
        
        if not file_path:
            return
        
        # Cập nhật đường dẫn đã chọn
        self.selected_image_path.set(file_path)
        
        # Xử lý ảnh
        self.handle_image_upload(user_id, file_path)
        
        # Đóng form
        form_window.destroy()

    def handle_image_upload(self, user_id, file_path):
        """
        Xử lý việc tải ảnh đại diện
        """
        if not file_path:
            return
        
        try:
            # Tạo tên file mới
            file_extension = os.path.splitext(file_path)[1]
            new_filename = f"user_{user_id}{file_extension}"
            new_file_path = os.path.join(self.user_images_dir, new_filename)
            
            # Sao chép file vào thư mục lưu trữ
            shutil.copy2(file_path, new_file_path)
            
            # Resize ảnh để hiển thị
            image = Image.open(new_file_path)
            image = image.resize((150, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Hiển thị ảnh mới
            if hasattr(self, 'user_image_label'):
                self.user_image_label.config(image=photo, text="")
                self.user_image_label.image = photo
            
            # Cập nhật đường dẫn ảnh vào thông tin người dùng
            user = self.user_manager.get_user_by_id(user_id)
            if user:
                user['picture'] = new_file_path
                self.user_manager.update_user(user_id, user)
                
                # Cập nhật giao diện
                if hasattr(self, 'user_tree'):
                    self.load_users()
                
                # Thông báo thành công
                messagebox.showinfo("Thành công", "Đã cập nhật ảnh đại diện!")
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin người dùng!")
                
        except Exception as e:
            print(f"Lỗi khi tải ảnh: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải ảnh: {e}")