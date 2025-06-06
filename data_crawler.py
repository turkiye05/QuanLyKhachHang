import requests
import json
import os
import random
from datetime import datetime

class DataCrawler:
    def __init__(self, customers_file="customers.json"):
        """
        Khởi tạo DataCrawler để lấy dữ liệu mẫu từ API
        """
        self.customers_file = customers_file
        self.api_url = "https://randomuser.me/api/"
    
    def convert_gender(self, gender):
        """
        Chuyển đổi giới tính từ male/female sang Nam/Nữ
        """
        gender_map = {
            "male": "Nam",
            "female": "Nữ"
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
        # Lấy phần local của email
        local_part = email.split('@')[0]
        
        # Tạo email mới với domain gmail.com
        return f"{local_part}@gmail.com"
    
    def fetch_random_users(self, count=10):
        """
        Lấy dữ liệu người dùng ngẫu nhiên từ API randomuser.me
        """
        try:
            print(f"Đang lấy {count} khách hàng ngẫu nhiên từ API...")
            response = requests.get(f"{self.api_url}?results={count}&nat=us")
            
            if response.status_code == 200:
                data = response.json()
                
                # Chuyển đổi dữ liệu từ API sang định dạng khách hàng
                customers = []
                for user in data.get("results", []):
                    # Tạo ID duy nhất cho khách hàng mới theo định dạng KHxxxx
                    timestamp = str(int(datetime.now().timestamp()))
                    last_four = timestamp[-4:] if len(timestamp) >= 4 else timestamp.zfill(4)
                    customer_id = f"KH{last_four}"
                    
                    # Kiểm tra xem ID đã tồn tại chưa
                    while any(customer.get("id") == customer_id for customer in customers):
                        # Nếu ID đã tồn tại, tạo ID mới bằng cách thêm số ngẫu nhiên
                        last_four = str(random.randint(1000, 9999))
                        customer_id = f"KH{last_four}"
                    
                    customer = {
                        "id": customer_id,
                        "name": f"{user['name']['first']} {user['name']['last']}",
                        "email": self.format_email(user["email"]),
                        "phone": self.format_phone_number(user["phone"]),
                        "address": f"{user['location']['street']['number']} {user['location']['street']['name']}, {user['location']['city']}, {user['location']['state']}, {user['location']['country']}",
                        "gender": self.convert_gender(user["gender"]),
                        "age": user["dob"]["age"],
                        "picture": user["picture"]["large"],
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    customers.append(customer)
                
                # Lưu danh sách khách hàng vào file JSON
                self.save_customers(customers)
                
                print(f"Đã lấy thành công {len(customers)} khách hàng.")
                return True, customers
            else:
                return False, f"Lỗi khi gọi API: {response.status_code}"
        except Exception as e:
            return False, f"Lỗi khi lấy dữ liệu: {e}"
    
    def save_customers(self, customers):
        """
        Lưu danh sách khách hàng vào file JSON
        """
        existing_customers = []
        
        # Đọc file JSON hiện tại nếu có
        if os.path.exists(self.customers_file):
            try:
                with open(self.customers_file, 'r', encoding='utf-8') as file:
                    existing_customers = json.load(file)
            except Exception as e:
                print(f"Lỗi khi đọc file {self.customers_file}: {e}")
        
        # Thêm khách hàng mới vào danh sách hiện tại
        merged_customers = existing_customers + customers
        
        # Lưu lại file JSON
        try:
            with open(self.customers_file, 'w', encoding='utf-8') as file:
                json.dump(merged_customers, file, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Lỗi khi lưu file {self.customers_file}: {e}")
            return False 