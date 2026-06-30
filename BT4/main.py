from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

# Danh sách học viên đã có trong hệ thống
students = [
    {
        "full_name": "Tran Van B",
        "email": "existing@gmail.com",
        "age": 21,
        "course": "python",
        "phone": "0912345678"
    }
]


# Model nhận dữ liệu từ Request Body
class Student(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    age: int
    course: str
    phone: str


# API đăng ký học viên
@app.post("/students")
def create_student(student: Student):

    # Kiểm tra email đã tồn tại hay chưa
    for item in students:
        if item["email"] == student.email:
            return {
                "detail": "Email đã tồn tại trong hệ thống"
            }

    # Thêm học viên mới
    students.append(student.model_dump())

    return {
        "message": "Đăng ký học viên thành công",
        "student": student
    }


# ==========================================================
# PHẦN 1: PHÂN TÍCH & ĐỀ XUẤT ĐA GIẢI PHÁP
# ==========================================================

# 1. Phân tích Input / Output
#
# Input:
# Client gửi Request Body dạng JSON.
#
# Ví dụ:
#
# {
#     "full_name": "Nguyen Van A",
#     "email": "vana@gmail.com",
#     "age": 20,
#     "course": "python",
#     "phone": "0987654321"
# }
#
#
# Output thành công:
#
# {
#     "message": "Đăng ký học viên thành công",
#     "student": {
#         ...
#     }
# }
#
#
# Output thất bại:
#
# - Thiếu trường bắt buộc
# - Email sai định dạng
# - Email đã tồn tại
#
# Ví dụ:
#
# {
#     "detail": "Email đã tồn tại trong hệ thống"
# }


# ==========================================================
# 2. Đề xuất ít nhất 2 giải pháp
# ==========================================================

# Giải pháp 1:
#
# Không sử dụng Pydantic.
#
# Nhận dữ liệu bằng dict rồi tự kiểm tra:
#
# - Kiểm tra từng trường
# - Kiểm tra email
# - Kiểm tra độ dài tên
# - Kiểm tra email trùng
#
# Ưu điểm:
# Chủ động kiểm soát toàn bộ.
#
# Nhược điểm:
# Phải viết rất nhiều code.


# Giải pháp 2:
#
# Sử dụng Pydantic BaseModel.
#
# Khai báo kiểu dữ liệu ngay trong Model.
#
# FastAPI tự động kiểm tra:
#
# - Thiếu trường
# - Sai kiểu dữ liệu
# - Sai định dạng email
#
# Sau đó chỉ cần viết thêm phần kiểm tra email trùng.
#
# Ưu điểm:
# Code ngắn gọn.
#
# Dễ bảo trì.
#
# Ít lỗi hơn.


# ==========================================================
# PHẦN 2: SO SÁNH & LỰA CHỌN
# ==========================================================

# Bảng so sánh
#
# ------------------------------------------------------------
# Tiêu chí                  | Giải pháp 1 | Giải pháp 2
# ------------------------------------------------------------
# Độ dễ hiểu                | Trung bình  | Cao
# Số lượng code             | Nhiều       | Ít
# Kiểm soát lỗi             | Tự viết     | FastAPI hỗ trợ
# Cấu trúc dữ liệu          | Không rõ    | Rõ ràng
# Khả năng bảo trì          | Thấp        | Cao
# ------------------------------------------------------------


# Lựa chọn
#
# Chọn Giải pháp 2.
#
# Vì:
#
# - Ít code hơn.
# - FastAPI tự validate dữ liệu.
# - Code rõ ràng.
# - Dễ mở rộng.
# - Phù hợp với các dự án thực tế.


# ==========================================================
# PHẦN 3: THIẾT KẾ & TRIỂN KHAI
# ==========================================================

# Luồng xử lý
#
# Bước 1:
# Client gửi Request Body.
#
# Bước 2:
# FastAPI dùng Pydantic kiểm tra:
#
# - Thiếu trường
# - Sai kiểu dữ liệu
# - Sai email
# - full_name có ít nhất 3 ký tự
#
# Nếu sai:
# FastAPI trả lỗi 422.
#
# Bước 3:
# Nếu hợp lệ,
# kiểm tra email đã tồn tại chưa.
#
# Nếu email đã tồn tại:
#
# {
#     "detail": "Email đã tồn tại trong hệ thống"
# }
#
# Bước 4:
# Nếu chưa tồn tại,
# thêm học viên vào danh sách.
#
# Bước 5:
# Trả về thông báo đăng ký thành công.


# ==========================================================
# TEST CASE
# ==========================================================

# 1.
# POST /students
#
# {
#     "full_name":"Nguyen Van A",
#     "email":"vana@gmail.com",
#     "age":20,
#     "course":"python",
#     "phone":"0987654321"
# }
#
# Kết quả:
#
# {
#     "message":"Đăng ký học viên thành công",
#     "student":{...}
# }


# 2.
# Thiếu email
#
# {
#     "full_name":"Nguyen Van A",
#     "age":20,
#     "course":"python",
#     "phone":"0987654321"
# }
#
# Kết quả:
#
# FastAPI trả lỗi 422.


# 3.
# Email sai định dạng
#
# {
#     "full_name":"Nguyen Van A",
#     "email":"vana.gmail.com",
#     "age":20,
#     "course":"python",
#     "phone":"0987654321"
# }
#
# Kết quả:
#
# FastAPI trả lỗi 422.


# 4.
# Email đã tồn tại
#
# {
#     "full_name":"Nguyen Van A",
#     "email":"existing@gmail.com",
#     "age":20,
#     "course":"python",
#     "phone":"0987654321"
# }
#
# Kết quả:
#
# {
#     "detail":"Email đã tồn tại trong hệ thống"
# }