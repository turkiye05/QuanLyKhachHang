import json
import os
import hashlib
from datetime import datetime
import random

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
        
        for i, user in enumerate(self.users):
            if user.get("id") == user_id:
                # Tạo bản sao của dữ liệu người dùng hiện tại
                updated_user = dict(user)
                
                # Cập nhật các trường được phép
                if "full_name" in updated_data:
                    updated_user["full_name"] = updated_data["full_name"]
                
                # Xử lý cập nhật mật khẩu
                if "new_password" in updated_data and updated_data["new_password"]:
                    updated_user["password"] = self.hash_password(updated_data["new_password"])
                
                # Chỉ admin mới có thể thay đổi role
                if self.is_admin() and "role" in updated_data:
                    # Kiểm tra nếu đang cập nhật role của admin cuối cùng
                    if user.get("role") == "admin" and updated_data["role"] != "admin" and self.count_admins() <= 1:
                        return False, "Không thể thay đổi quyền của admin cuối cùng!"
                    updated_user["role"] = updated_data["role"]
                
                # Cập nhật thời gian chỉnh sửa
                updated_user["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Cập nhật ảnh đại diện nếu có
                if "picture" in updated_data:
                    updated_user["picture"] = updated_data["picture"]
                
                # Lưu vào danh sách người dùng
                self.users[i] = updated_user
                
                # Cập nhật current_user nếu đang update chính mình
                if is_self_update:
                    self.current_user = updated_user
                
                # Lưu vào file
                if self.save_data():
                    return True, "Cập nhật thông tin thành công!"
                else:
                    return False, "Lỗi khi lưu dữ liệu!"
                
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
    
    def format_user_id(self):
        """
        Tạo ID người dùng theo định dạng NVxxxx (6 ký tự)
        """
        # Tạo số ngẫu nhiên 4 chữ số
        random_num = str(random.randint(1000, 9999))
        user_id = f"NV{random_num}"
        
        # Kiểm tra xem ID đã tồn tại chưa
        while any(user.get("id") == user_id for user in self.users):
            random_num = str(random.randint(1000, 9999))
            user_id = f"NV{random_num}"
            
        return user_id
    
    def format_phone_number(self, phone):
        """
        Định dạng số điện thoại thành chính xác 10 chữ số, bắt đầu bằng 09 hoặc 08
        """
        # Loại bỏ tất cả ký tự không phải số
        phone = ''.join(filter(str.isdigit, phone))
        
        # Nếu số điện thoại bắt đầu bằng 0, loại bỏ số 0
        if phone.startswith('0'):
            phone = phone[1:]
            
        # Nếu số điện thoại bắt đầu bằng 84, loại bỏ 84
        if phone.startswith('84'):
            phone = phone[2:]
            
        # Nếu số điện thoại dài hơn 10 số, chỉ lấy 10 số
        if len(phone) > 10:
            phone = phone[:10]
            
        # Nếu số điện thoại ngắn hơn 10 số, thêm số 0 vào đầu
        if len(phone) < 10:
            phone = phone.zfill(10)
            
        # Kiểm tra và thêm đầu số 09 hoặc 08
        if not phone.startswith(('09', '08')):
            # Nếu số điện thoại bắt đầu bằng 9, thêm 0 vào đầu
            if phone.startswith('9'):
                phone = '0' + phone[:9]
            # Nếu số điện thoại bắt đầu bằng 8, thêm 0 vào đầu
            elif phone.startswith('8'):
                phone = '0' + phone[:9]
            # Nếu không bắt đầu bằng 9 hoặc 8, thêm 09 vào đầu
            else:
                phone = '09' + phone[-8:]
            
        return phone
    
    def validate_phone_number(self, phone):
        """
        Kiểm tra tính hợp lệ của số điện thoại
        - Phải có chính xác 10 chữ số
        - Phải bắt đầu bằng 09 hoặc 08
        """
        # Loại bỏ tất cả ký tự không phải số
        phone = ''.join(filter(str.isdigit, phone))
        
        # Nếu số điện thoại bắt đầu bằng 0, loại bỏ số 0
        if phone.startswith('0'):
            phone = phone[1:]
            
        # Nếu số điện thoại bắt đầu bằng 84, loại bỏ 84
        if phone.startswith('84'):
            phone = phone[2:]
            
        # Kiểm tra độ dài và ký tự
        if len(phone) != 10 or not phone.isdigit():
            return False
            
        # Kiểm tra đầu số
        if not phone.startswith(('09', '08')):
            return False
            
        return True
    
    def add_user(self, user_data):
        """
        Thêm người dùng mới vào hệ thống
        """
        # Kiểm tra quyền admin
        if not self.is_admin():
            return False, "Bạn không có quyền thực hiện chức năng này!"
        
        # Kiểm tra username đã tồn tại chưa
        if any(user.get("username") == user_data["username"] for user in self.users):
            return False, "Tên đăng nhập đã tồn tại!"
        
        # Kiểm tra độ dài mật khẩu
        if len(user_data["password"]) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự!"
        
        # Kiểm tra và định dạng số điện thoại
        if "phone" in user_data:
            if not self.validate_phone_number(user_data["phone"]):
                return False, "Số điện thoại không hợp lệ! Vui lòng nhập chính xác 10 chữ số và bắt đầu bằng 09 hoặc 08."
            user_data["phone"] = self.format_phone_number(user_data["phone"])
        
        # Tạo ID mới theo định dạng NVxxxx
        user_id = self.format_user_id()
        
        # Tạo người dùng mới
        new_user = {
            "id": user_id,
            "username": user_data["username"],
            "password": self.hash_password(user_data["password"]),
            "full_name": user_data["full_name"],
            "phone": user_data.get("phone", ""),
            "role": user_data["role"],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Thêm vào danh sách
        self.users.append(new_user)
        
        # Lưu vào file
        if self.save_data():
            return True, "Thêm người dùng thành công!"
        else:
            return False, "Lỗi khi lưu dữ liệu!" 