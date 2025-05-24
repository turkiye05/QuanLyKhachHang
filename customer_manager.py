import json
import os
from datetime import datetime

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
                        self.customers = json.loads(content)
                    else:
                        self.customers = []
                print(f"Đã tải dữ liệu từ {self.data_file}, số lượng khách hàng: {len(self.customers)}")
            else:
                self.customers = []
                print(f"File {self.data_file} không tồn tại. Tạo danh sách khách hàng mới.")
                # Tạo file trống nếu chưa tồn tại
                with open(self.data_file, 'w', encoding='utf-8') as file:
                    json.dump([], file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {e}")
            self.customers = []
    
    def reload_data(self):
        """
        Tải lại dữ liệu từ file JSON
        """
        self.load_data()
        return self.customers
    
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
    
    def add_customer(self, customer_data):
        """
        Thêm một khách hàng mới
        """
        # Tạo ID duy nhất cho khách hàng mới
        customer_id = str(datetime.now().timestamp()).replace(".", "")
        customer_data["id"] = customer_id
        customer_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
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
                # Giữ lại ID và thời gian tạo
                updated_data["id"] = customer_id
                updated_data["created_at"] = customer.get("created_at")
                updated_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
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
        Tìm kiếm khách hàng theo từ khóa
        """
        results = []
        keyword = keyword.lower()
        
        for customer in self.customers:
            if (keyword in customer.get("name", "").lower() or
                keyword in customer.get("email", "").lower() or
                keyword in customer.get("phone", "").lower() or
                keyword in customer.get("address", "").lower()):
                results.append(customer)
        
        return results 