import json
import os
from datetime import datetime
import logging

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
                logger.info(f"Đã tải dữ liệu từ {self.data_file}, số lượng khách hàng: {len(self.customers)}")
            else:
                self.customers = []
                logger.info(f"File {self.data_file} không tồn tại. Tạo danh sách khách hàng mới.")
                # Tạo file trống nếu chưa tồn tại
                with open(self.data_file, 'w', encoding='utf-8') as file:
                    json.dump([], file, ensure_ascii=False, indent=4)
        except json.JSONDecodeError as e:
            logger.error(f"Lỗi khi đọc file JSON: {e}")
            self.customers = []
        except Exception as e:
            logger.error(f"Lỗi không xác định khi tải dữ liệu: {e}")
            self.customers = []
    
    def reload_data(self):
        """
        Tải lại dữ liệu từ file JSON
        """
        try:
            # Xóa cache hiện tại
            self.customers = []
            # Tải lại dữ liệu từ file
            self.load_data()
            logger.info("Đã tải lại dữ liệu thành công")
            return self.customers
        except Exception as e:
            logger.error(f"Lỗi khi tải lại dữ liệu: {e}")
            return []
    
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
            logger.info(f"Đã lưu dữ liệu vào {self.data_file}, số lượng khách hàng: {len(self.customers)}")
            return True
        except Exception as e:
            logger.error(f"Lỗi khi lưu dữ liệu: {e}")
            return False
    
    def add_customer(self, customer_data):
        """
        Thêm một khách hàng mới
        """
        try:
            # Tạo ID duy nhất cho khách hàng mới
            customer_id = str(datetime.now().timestamp()).replace(".", "")
            customer_data["id"] = customer_id
            customer_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.customers.append(customer_data)
            if self.save_data():
                logger.info(f"Đã thêm khách hàng mới với ID: {customer_id}")
                return customer_id
            return None
        except Exception as e:
            logger.error(f"Lỗi khi thêm khách hàng: {e}")
            return None
    
    def get_all_customers(self):
        """
        Lấy toàn bộ danh sách khách hàng
        """
        return self.customers
    
    def get_customer_by_id(self, customer_id):
        """
        Tìm khách hàng theo ID
        """
        try:
            customer_id = str(customer_id)  # Chuyển đổi ID về dạng string
            logger.info(f"Đang tìm khách hàng có ID: {customer_id}")
            
            for customer in self.customers:
                if str(customer.get("id")) == customer_id:
                    logger.info(f"Đã tìm thấy khách hàng: {customer.get('name')}")
                    return customer
                    
            logger.warning(f"Không tìm thấy khách hàng với ID: {customer_id}")
            return None
        except Exception as e:
            logger.error(f"Lỗi khi tìm khách hàng: {e}")
            return None
    
    def update_customer(self, customer_id, updated_data):
        """
        Cập nhật thông tin khách hàng
        """
        try:
            customer_id = str(customer_id)  # Chuyển đổi ID về dạng string
            for i, customer in enumerate(self.customers):
                if str(customer.get("id")) == customer_id:
                    # Giữ lại ID và thời gian tạo
                    updated_data["id"] = customer_id
                    updated_data["created_at"] = customer.get("created_at")
                    updated_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    self.customers[i] = updated_data
                    if self.save_data():
                        logger.info(f"Đã cập nhật khách hàng với ID: {customer_id}")
                        return True
                    return False
            logger.warning(f"Không tìm thấy khách hàng để cập nhật với ID: {customer_id}")
            return False
        except Exception as e:
            logger.error(f"Lỗi khi cập nhật khách hàng: {e}")
            return False
    
    def delete_customer(self, customer_id):
        """
        Xóa một khách hàng theo ID
        """
        try:
            customer_id = str(customer_id)  # Chuyển đổi ID về dạng string
            for i, customer in enumerate(self.customers):
                if str(customer.get("id")) == customer_id:
                    del self.customers[i]
                    if self.save_data():
                        logger.info(f"Đã xóa khách hàng với ID: {customer_id}")
                        return True
                    return False
            logger.warning(f"Không tìm thấy khách hàng để xóa với ID: {customer_id}")
            return False
        except Exception as e:
            logger.error(f"Lỗi khi xóa khách hàng: {e}")
            return False
    
    def search_customers(self, keyword):
        """
        Tìm kiếm khách hàng theo từ khóa
        """
        try:
            results = []
            keyword = keyword.lower()
            
            for customer in self.customers:
                if (keyword in customer.get("name", "").lower() or
                    keyword in customer.get("email", "").lower() or
                    keyword in customer.get("phone", "").lower() or
                    keyword in customer.get("address", "").lower()):
                    results.append(customer)
            
            logger.info(f"Tìm thấy {len(results)} kết quả cho từ khóa: {keyword}")
            return results
        except Exception as e:
            logger.error(f"Lỗi khi tìm kiếm khách hàng: {e}")
            return [] 
