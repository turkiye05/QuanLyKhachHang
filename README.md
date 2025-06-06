# Hệ Thống Quản Lý Khách Hàng

Ứng dụng quản lý danh sách khách hàng trong cửa hàng với giao diện người dùng đồ họa (GUI) và các chức năng CRUD.

## Tính năng chính

1. **Quản lý khách hàng**
   - Xem danh sách khách hàng
   - Tìm kiếm khách hàng
   - Thêm, sửa, xóa thông tin khách hàng
   - Hiển thị chi tiết thông tin khách hàng

2. **Quản lý người dùng và phân quyền**
   - Đăng nhập, đăng ký tài khoản
   - Phân quyền người dùng (admin và user thông thường)
   - Quản lý danh sách người dùng (chỉ admin)

3. **Lấy dữ liệu từ API**
   - Tải dữ liệu mẫu từ API randomuser.me
   - Hiển thị hình ảnh khách hàng

4. **Lưu trữ dữ liệu**
   - Sử dụng file JSON để lưu trữ dữ liệu

## Cài đặt

### Cài đặt từ mã nguồn

1. Cài đặt Python 3.7+ (https://python.org)

2. Cài đặt các thư viện phụ thuộc:
   ```
   pip install pillow requests
   ```

3. Chạy ứng dụng:
   ```
   python main.py
   ```

### Cài đặt từ file thực thi (Windows)

1. Tải file QuanLyKhachHang.exe
2. Chạy file QuanLyKhachHang.exe

## Đóng gói ứng dụng

Để đóng gói ứng dụng thành file thực thi, sử dụng cx_Freeze:

1. Cài đặt cx_Freeze:
   ```
   pip install cx_Freeze
   ```

2. Chạy lệnh đóng gói:
   ```
   python setup.py build
   ```

3. Thư mục build sẽ chứa ứng dụng đã đóng gói

## Hướng dẫn sử dụng

### Đăng nhập

- Tài khoản admin mặc định:
  - Tên đăng nhập: admin
  - Mật khẩu: admin123

- Người dùng mới có thể đăng ký tài khoản qua màn hình đăng nhập

### Quản lý khách hàng

- **Xem danh sách**: Mở tab "Quản lý khách hàng"
- **Tìm kiếm**: Nhập từ khóa vào ô tìm kiếm và nhấn "Tìm"
- **Thêm mới**: Nhấn nút "Thêm mới" hoặc chọn menu "Khách hàng > Thêm khách hàng"
- **Xem chi tiết**: Click đúp vào một khách hàng trong danh sách
- **Xóa**: Click chuột phải vào khách hàng và chọn "Xóa"

### Quản lý người dùng (chỉ admin)

- Chuyển đến tab "Quản lý người dùng" hoặc chọn menu "Người dùng > Quản lý người dùng"
- Các chức năng tương tự như quản lý khách hàng

### Tải dữ liệu mẫu

- Chọn menu "Tệp > Tải dữ liệu mẫu"
- Nhập số lượng khách hàng mẫu cần tải

## Cấu trúc dự án

- `main.py` - File chính để chạy ứng dụng
- `login_ui.py` - Giao diện đăng nhập và đăng ký
- `main_ui.py` - Giao diện chính của ứng dụng
- `customer_manager.py` - Quản lý danh sách khách hàng
- `user_manager.py` - Quản lý người dùng và phân quyền
- `data_crawler.py` - Lấy dữ liệu từ API
- `setup.py` - Cấu hình đóng gói ứng dụng
- `customers.json` - Lưu trữ dữ liệu khách hàng
- `users.json` - Lưu trữ dữ liệu người dùng

## Yêu cầu hệ thống

- Python 3.7+
- Windows, macOS, hoặc Linux
- 100MB RAM trở lên
- 50MB dung lượng đĩa trống 