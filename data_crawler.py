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
                    customer = {
                        "id": str(datetime.now().timestamp()).replace(".", "") + str(random.randint(1000, 9999)),
                        "name": f"{user['name']['first']} {user['name']['last']}",
                        "email": user["email"],
                        "phone": user["phone"],
                        "address": f"{user['location']['street']['number']} {user['location']['street']['name']}, {user['location']['city']}, {user['location']['state']}, {user['location']['country']}",
                        "gender": user["gender"],
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