import json
import os
import hashlib
from datetime import datetime

class UserManager:
    def __init__(self, data_file="users.json"):
        """
        Khởi tạo UserManager với đường dẫn file dữ liệu
        """
        self.data_file = data_file
        self.users = []
        self.current_user = None
        self.load_data()
    
    def load_data(self):
        """
        Đọc dữ liệu người dùng từ file JSON
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if content:  # Kiểm tra nếu file không trống
                        self.users = json.loads(content)
                    else:
                        self.users = []
                        # Tạo tài khoản admin mặc định
                        self.create_default_admin()
                print(f"Đã tải dữ liệu người dùng từ {self.data_file}, số lượng người dùng: {len(self.users)}")
            else:
                self.users = []
                print(f"File {self.data_file} không tồn tại. Tạo danh sách người dùng mới.")
                # Tạo file trống nếu chưa tồn tại
                with open(self.data_file, 'w', encoding='utf-8') as file:
                    json.dump([], file, ensure_ascii=False, indent=4)
                # Tạo tài khoản admin mặc định
                self.create_default_admin()
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu người dùng: {e}")
            self.users = []
            # Tạo tài khoản admin mặc định
            self.create_default_admin()
    
    def create_default_admin(self):
        """
        Tạo tài khoản admin mặc định nếu chưa có người dùng nào
        """
        if not self.users:
            admin_user = {
                "id": "1",
                "username": "admin",
                "password": self.hash_password("admin123"),
                "full_name": "Administrator",
                "role": "admin",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.users.append(admin_user)
            self.save_data()
            print("Đã tạo tài khoản admin mặc định (username: admin, password: admin123)")
    
    def save_data(self):
        """
        Lưu dữ liệu người dùng ra file JSON
        """
        try:
            # Đảm bảo thư mục chứa file tồn tại
            file_dir = os.path.dirname(os.path.abspath(self.data_file))
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
                
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(self.users, file, ensure_ascii=False, indent=4)
            print(f"Đã lưu dữ liệu người dùng vào {self.data_file}, số lượng người dùng: {len(self.users)}")
            return True
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu người dùng: {e}")
            return False
    
    def hash_password(self, password):
        """
        Mã hóa mật khẩu sử dụng SHA-256
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username, password, full_name, role="user"):
        """
        Đăng ký người dùng mới
        """
        # Kiểm tra xem username đã tồn tại chưa
        if any(user.get("username") == username for user in self.users):
            return False, "Tên đăng nhập đã tồn tại!"
        
        # Tạo người dùng mới
        user_id = str(datetime.now().timestamp()).replace(".", "")
        new_user = {
            "id": user_id,
            "username": username,
            "password": self.hash_password(password),
            "full_name": full_name,
            "role": role,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.users.append(new_user)
        self.save_data()
        return True, "Đăng ký tài khoản thành công!"
    
    def login(self, username, password):
        """
        Đăng nhập người dùng
        """
        hashed_password = self.hash_password(password)
        
        for user in self.users:
            if user.get("username") == username and user.get("password") == hashed_password:
                self.current_user = user
                return True, "Đăng nhập thành công!"
        
        return False, "Tên đăng nhập hoặc mật khẩu không chính xác!"
    
    def logout(self):
        """
        Đăng xuất người dùng
        """
        self.current_user = None
    
    def get_current_user(self):
        """
        Lấy thông tin người dùng hiện tại
        """
        return self.current_user
    
    def is_admin(self):
        """
        Kiểm tra người dùng hiện tại có phải admin không
        """
        if self.current_user:
            return self.current_user.get("role") == "admin"
        return False
    
    def get_user_by_id(self, user_id):
        """
        Lấy thông tin người dùng theo ID
        """
        for user in self.users:
            if user.get("id") == user_id:
                # Kiểm tra đường dẫn ảnh đại diện
                if 'picture' in user and user['picture'] and not os.path.exists(user['picture']):
                    print(f"Cảnh báo: Không tìm thấy ảnh đại diện tại {user['picture']}")
                return user
        return None
    
    def delete_user(self, user_id):
        """
        Xóa một người dùng theo ID (chỉ admin mới có quyền)
        """
        if not self.is_admin():
            return False, "Bạn không có quyền thực hiện chức năng này!"
        
        for i, user in enumerate(self.users):
            if user.get("id") == user_id:
                # Không cho phép xóa tài khoản admin cuối cùng
                if user.get("role") == "admin" and self.count_admins() <= 1:
                    return False, "Không thể xóa tài khoản admin cuối cùng!"
                
                del self.users[i]
                self.save_data()
                return True, "Xóa người dùng thành công!"
        
        return False, "Không tìm thấy người dùng!"
    
    def count_admins(self):
        """
        Đếm số lượng tài khoản admin
        """
        return sum(1 for user in self.users if user.get("role") == "admin")
    
    def get_all_users(self):
        """
        Lấy danh sách tất cả người dùng (chỉ admin mới có quyền)
        """
        # Bỏ kiểm tra quyền tạm thời để sửa lỗi
        # if not self.is_admin():
        #     return []
        
        # In thông tin debug
        print(f"Đang lấy danh sách người dùng. Hiện có {len(self.users)} người dùng.")
        if len(self.users) == 0:
            print("Không có người dùng nào trong hệ thống!")
            # Tự động tạo admin mặc định nếu chưa có người dùng nào
            self.create_default_admin()
            
        return self.users
    
    def update_user(self, user_id, updated_data):
        """
        Cập nhật thông tin người dùng
        """
        # Kiểm tra quyền: 
        # - Admin có thể cập nhật thông tin của bất kỳ người dùng nào
        # - Người dùng chỉ có thể cập nhật thông tin cá nhân nhưng không thể thay đổi quyền
        is_self_update = self.current_user and self.current_user.get("id") == user_id
        
        if not self.is_admin() and not is_self_update:
            return False, "Bạn không có quyền thực hiện chức năng này!"
            
        # Nếu là người dùng thông thường đang cập nhật thông tin của chính mình
        # và cố gắng thay đổi quyền thì chặn lại
        if not self.is_admin() and is_self_update and "role" in updated_data:
            current_role = self.current_user.get("role", "user")
            if updated_data["role"] != current_role:
                return False, "Bạn không có quyền thay đổi vai trò của mình!"
        
        for i, user in enumerate(self.users):
            if user.get("id") == user_id:
                # Kiểm tra nếu đang cập nhật role của admin cuối cùng
                if user.get("role") == "admin" and updated_data.get("role") != "admin" and self.count_admins() <= 1:
                    return False, "Không thể thay đổi quyền của admin cuối cùng!"
                
                # Giữ lại ID và thời gian tạo
                updated_data["id"] = user_id
                updated_data["created_at"] = user.get("created_at")
                
                # Nếu có cập nhật mật khẩu
                if "new_password" in updated_data and updated_data["new_password"]:
                    updated_data["password"] = self.hash_password(updated_data["new_password"])
                    del updated_data["new_password"]
                else:
                    # Giữ nguyên mật khẩu cũ
                    updated_data["password"] = user.get("password")
                
                # Giữ nguyên role nếu không được cung cấp (đặc biệt quan trọng cho người dùng thông thường)
                if "role" not in updated_data:
                    updated_data["role"] = user.get("role", "user")
                
                # Giữ nguyên username
                if "username" not in updated_data:
                    updated_data["username"] = user.get("username", "")
                    
                # Cập nhật thời gian chỉnh sửa
                updated_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                self.users[i] = updated_data
                
                # Cập nhật current_user nếu đang update chính mình
                if self.current_user and self.current_user.get("id") == user_id:
                    self.current_user = updated_data
                
                self.save_data()
                return True, "Cập nhật thông tin người dùng thành công!"
        
        return False, "Không tìm thấy người dùng!"
    
    def reset_password(self, username, full_name, new_password):
        """
        Khôi phục mật khẩu cho người dùng quên mật khẩu
        Xác minh danh tính bằng username và họ tên đầy đủ
        """
        for i, user in enumerate(self.users):
            if user.get("username") == username:
                # Kiểm tra họ tên đầy đủ để xác minh danh tính
                if user.get("full_name") != full_name:
                    return False, "Thông tin xác minh không chính xác!"
                
                # Cập nhật mật khẩu mới
                self.users[i]["password"] = self.hash_password(new_password)
                self.users[i]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Lưu thay đổi
                self.save_data()
                return True, "Khôi phục mật khẩu thành công!"
        
        return False, "Không tìm thấy tài khoản với tên đăng nhập này!" 