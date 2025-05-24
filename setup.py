import sys
from cx_Freeze import setup, Executable

# Các thư viện phụ thuộc
build_exe_options = {
    "packages": ["tkinter", "PIL", "json", "requests", "os", "threading", "datetime", "hashlib"],
    "excludes": [],
    "include_files": ["customers.json", "users.json"],
}

# Thiết lập một số thông số
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Sử dụng GUI cho Windows

# Cấu hình exe
executables = [
    Executable(
        "main.py",
        base=base,
        target_name="QuanLyKhachHang.exe",
        icon=None,  # Có thể thêm icon nếu có
    )
]

setup(
    name="QuanLyKhachHang",
    version="1.0",
    description="Hệ thống Quản lý Khách hàng",
    options={"build_exe": build_exe_options},
    executables=executables,
)

# Hướng dẫn sử dụng:
# 1. Cài đặt cx_Freeze: pip install cx_Freeze
# 2. Chạy lệnh: python setup.py build
# 3. Thư mục build sẽ chứa ứng dụng đã đóng gói 