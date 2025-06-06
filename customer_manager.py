import json
import os
from datetime import datetime
import random

class CustomerManager:
    def __init__(self, data_file="customers.json"):
        """
        Khởi tạo CustomerManager với đường dẫn file dữ liệu
        """
        self.data_file = data_file
        self.customers = []
        self.load_data()
    
    def load_data(self):
        """
        Đọc dữ liệu khách hàng từ file JSON
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if content:  # Kiểm tra nếu file không trống
                        try:
                            self.customers = json.loads(content)
                            if not isinstance(self.customers, list):
                                raise ValueError("Dữ liệu không đúng định dạng danh sách")
                            print(f"Đã tải dữ liệu từ {self.data_file}, số lượng khách hàng: {len(self.customers)}")
                            return True
                        except json.JSONDecodeError as je:
                            print(f"Lỗi định dạng JSON: {je}")
                            self.customers = []
                            return False
                        except ValueError as ve:
                            print(f"Lỗi dữ liệu: {ve}")
                            self.customers = []
                            return False
                    else:
                        self.customers = []
                        print(f"File {self.data_file} trống")
                        return True
            else:
                self.customers = []
                print(f"File {self.data_file} không tồn tại. Tạo danh sách khách hàng mới.")
                # Tạo file trống nếu chưa tồn tại
                with open(self.data_file, 'w', encoding='utf-8') as file:
                    json.dump([], file, ensure_ascii=False, indent=4)
                return True
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {e}")
            self.customers = []
            return False
    
    def save_data(self):
        """
        Lưu dữ liệu khách hàng ra file JSON
        """
        try:
            # Đảm bảo thư mục chứa file tồn tại
            file_dir = os.path.dirname(os.path.abspath(self.data_file))
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
                
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(self.customers, file, ensure_ascii=False, indent=4)
            print(f"Đã lưu dữ liệu vào {self.data_file}, số lượng khách hàng: {len(self.customers)}")
            return True
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")
            return False
    
    def convert_gender(self, gender):
        """
        Chuyển đổi giới tính từ male/female sang Nam/Nữ
        """
        gender_map = {
            "male": "Nam",
            "female": "Nữ"
        }
        return gender_map.get(gender.lower(), gender)
    
    def convert_gender_back(self, gender):
        """
        Chuyển đổi giới tính từ Nam/Nữ sang male/female
        """
        gender_map = {
            "nam": "male",
            "nữ": "female"
        }
        return gender_map.get(gender.lower(), gender)
    
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
    
    def format_email(self, email):
        """
        Định dạng email thành dạng gmail.com
        """
        # Nếu email không có @, thêm @gmail.com
        if '@' not in email:
            return f"{email}@gmail.com"
            
        # Nếu email có @, kiểm tra phần sau @
        local_part, domain = email.split('@')
        
        # Nếu domain không phải gmail.com, thay thế bằng gmail.com
        if domain.lower() != 'gmail.com':
            return f"{local_part}@gmail.com"
            
        return email.lower()
    
    def validate_phone_number(self, phone):
        """
        Kiểm tra tính hợp lệ của số điện thoại
        - Phải có chính xác 10 chữ số
        - Phải bắt đầu bằng 09 hoặc 08
        """
        # Loại bỏ tất cả ký tự không phải số
        phone = ''.join(filter(str.isdigit, phone))
        
        # Nếu số điện thoại bắt đầu bằng 84, thay bằng 0
        if phone.startswith('84'):
            phone = '0' + phone[2:]
        
        # Kiểm tra độ dài và ký tự
        if len(phone) != 10 or not phone.isdigit():
            return False
        
        # Kiểm tra đầu số
        if not phone.startswith(('09', '08')):
            return False
        
        return True
    
    def validate_email(self, email):
        """
        Kiểm tra tính hợp lệ của email
        """
        # Kiểm tra định dạng cơ bản của email
        if '@' not in email or '.' not in email:
            return False
            
        # Kiểm tra phần local và domain
        local_part, domain = email.split('@')
        
        # Kiểm tra độ dài phần local
        if len(local_part) < 1:
            return False
            
        # Kiểm tra domain
        if domain.lower() != 'gmail.com':
            return False
            
        return True
    
    def add_customer(self, customer_data):
        """
        Thêm một khách hàng mới
        """
        # Kiểm tra và định dạng số điện thoại
        if "phone" in customer_data:
            if not self.validate_phone_number(customer_data["phone"]):
                raise ValueError("Số điện thoại không hợp lệ! Vui lòng nhập chính xác 10 chữ số và bắt đầu bằng 09 hoặc 08.")
            customer_data["phone"] = self.format_phone_number(customer_data["phone"])
        
        # Kiểm tra và định dạng email
        if "email" in customer_data:
            if not self.validate_email(customer_data["email"]):
                raise ValueError("Email không hợp lệ! Vui lòng nhập đúng định dạng @gmail.com")
            customer_data["email"] = self.format_email(customer_data["email"])
        
        # Tạo ID duy nhất cho khách hàng mới theo định dạng KHxxxx
        timestamp = str(int(datetime.now().timestamp()))
        last_four = timestamp[-4:] if len(timestamp) >= 4 else timestamp.zfill(4)
        customer_id = f"KH{last_four}"
        
        # Kiểm tra xem ID đã tồn tại chưa
        while any(customer.get("id") == customer_id for customer in self.customers):
            # Nếu ID đã tồn tại, tạo ID mới bằng cách thêm số ngẫu nhiên
            last_four = str(random.randint(1000, 9999))
            customer_id = f"KH{last_four}"
        
        customer_data["id"] = customer_id
        customer_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Chuyển đổi giới tính sang định dạng Nam/Nữ
        if "gender" in customer_data:
            customer_data["gender"] = self.convert_gender(customer_data["gender"])
        
        self.customers.append(customer_data)
        self.save_data()
        return customer_id
    
    def get_all_customers(self):
        """
        Lấy toàn bộ danh sách khách hàng
        """
        return self.customers
    
    def get_customer_by_id(self, customer_id):
        """
        Tìm khách hàng theo ID
        """
        print(f"Đang tìm khách hàng có ID: {customer_id}")
        print(f"Danh sách khách hàng hiện có: {len(self.customers)} khách hàng")
        for i, customer in enumerate(self.customers):
            current_id = customer.get("id")
            print(f"Khách hàng thứ {i}: ID = {current_id}, kiểu dữ liệu: {type(current_id)}")
            if str(current_id) == str(customer_id):
                print(f"Đã tìm thấy khách hàng: {customer.get('name')}")
                return customer
        print(f"Không tìm thấy khách hàng với ID: {customer_id}")
        return None
    
    def update_customer(self, customer_id, updated_data):
        """
        Cập nhật thông tin khách hàng
        """
        for i, customer in enumerate(self.customers):
            if customer.get("id") == customer_id:
                # Kiểm tra và định dạng số điện thoại
                if "phone" in updated_data:
                    if not self.validate_phone_number(updated_data["phone"]):
                        raise ValueError("Số điện thoại không hợp lệ! Vui lòng nhập chính xác 10 chữ số và bắt đầu bằng 09 hoặc 08.")
                    updated_data["phone"] = self.format_phone_number(updated_data["phone"])
                
                # Kiểm tra và định dạng email
                if "email" in updated_data:
                    if not self.validate_email(updated_data["email"]):
                        raise ValueError("Email không hợp lệ! Vui lòng nhập đúng định dạng @gmail.com")
                    updated_data["email"] = self.format_email(updated_data["email"])
                
                # Giữ lại ID và thời gian tạo
                updated_data["id"] = customer_id
                updated_data["created_at"] = customer.get("created_at")
                updated_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Chuyển đổi giới tính sang định dạng Nam/Nữ
                if "gender" in updated_data:
                    updated_data["gender"] = self.convert_gender(updated_data["gender"])
                
                self.customers[i] = updated_data
                self.save_data()
                return True
        return False
    
    def delete_customer(self, customer_id):
        """
        Xóa một khách hàng theo ID
        """
        for i, customer in enumerate(self.customers):
            if customer.get("id") == customer_id:
                del self.customers[i]
                self.save_data()
                return True
        return False
    
    def search_customers(self, keyword):
        """
        Tìm kiếm khách hàng theo từ khóa hoặc ID
        """
        results = []
        if not keyword:
            return results
            
        # Chuẩn hóa từ khóa tìm kiếm
        keyword = keyword.lower().strip()
        
        # Hàm chuẩn hóa chuỗi để tìm kiếm không phân biệt dấu
        def normalize_text(text):
            if not text:
                return ""
            text = text.lower()
            # Loại bỏ dấu tiếng Việt
            text = text.replace('à', 'a').replace('á', 'a').replace('ả', 'a').replace('ã', 'a').replace('ạ', 'a')
            text = text.replace('ă', 'a').replace('ằ', 'a').replace('ắ', 'a').replace('ẳ', 'a').replace('ẵ', 'a').replace('ặ', 'a')
            text = text.replace('â', 'a').replace('ầ', 'a').replace('ấ', 'a').replace('ẩ', 'a').replace('ẫ', 'a').replace('ậ', 'a')
            text = text.replace('đ', 'd')
            text = text.replace('è', 'e').replace('é', 'e').replace('ẻ', 'e').replace('ẽ', 'e').replace('ẹ', 'e')
            text = text.replace('ê', 'e').replace('ề', 'e').replace('ế', 'e').replace('ể', 'e').replace('ễ', 'e').replace('ệ', 'e')
            text = text.replace('ì', 'i').replace('í', 'i').replace('ỉ', 'i').replace('ĩ', 'i').replace('ị', 'i')
            text = text.replace('ò', 'o').replace('ó', 'o').replace('ỏ', 'o').replace('õ', 'o').replace('ọ', 'o')
            text = text.replace('ô', 'o').replace('ồ', 'o').replace('ố', 'o').replace('ổ', 'o').replace('ỗ', 'o').replace('ộ', 'o')
            text = text.replace('ơ', 'o').replace('ờ', 'o').replace('ớ', 'o').replace('ở', 'o').replace('ỡ', 'o').replace('ợ', 'o')
            text = text.replace('ù', 'u').replace('ú', 'u').replace('ủ', 'u').replace('ũ', 'u').replace('ụ', 'u')
            text = text.replace('ư', 'u').replace('ừ', 'u').replace('ứ', 'u').replace('ử', 'u').replace('ữ', 'u').replace('ự', 'u')
            text = text.replace('ỳ', 'y').replace('ý', 'y').replace('ỷ', 'y').replace('ỹ', 'y').replace('ỵ', 'y')
            return text
            
        normalized_keyword = normalize_text(keyword)
        
        for customer in self.customers:
            # Kiểm tra ID trước
            customer_id = str(customer.get("id", "")).lower()
            if keyword == customer_id:
                # Nếu tìm thấy ID chính xác, trả về ngay kết quả
                return [customer]
            
            # Chuẩn hóa các trường dữ liệu để tìm kiếm
            name = normalize_text(customer.get("name", ""))
            email = normalize_text(customer.get("email", ""))
            phone = normalize_text(customer.get("phone", ""))
            address = normalize_text(customer.get("address", ""))
            
            # Tìm kiếm trong các trường
            if (normalized_keyword in name or
                normalized_keyword in email or
                normalized_keyword in phone or
                normalized_keyword in address or
                normalized_keyword in customer_id):  # Thêm tìm kiếm trong ID
                results.append(customer)
        
        return results 