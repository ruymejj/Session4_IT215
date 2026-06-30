from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
import re
import random

app = FastAPI()


# Model Request Body
class StudentRegister(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    age: int = Field(..., ge=15, le=60)
    phone: str = Field(..., min_length=10, max_length=11)
    course: str
    note: str | None = Field(default=None, max_length=200)


@app.post("/students/register")
def register_student(student: StudentRegister):

    # Kiểm tra số điện thoại chỉ chứa chữ số
    if not re.fullmatch(r"\d+", student.phone):
        return {
            "detail": "Số điện thoại chỉ được chứa chữ số"
        }

    # Tạo mã đăng ký ngẫu nhiên
    register_id = "STU" + str(random.randint(1000, 9999))

    # Chuẩn hóa dữ liệu
    result = student.model_dump()

    result["full_name"] = result["full_name"].title()

    if result["note"] is not None:
        result["note"] = result["note"].lower()

    return {
        "message": "Đăng ký học viên thành công",
        "register_id": register_id,
        "data": result
    }


# ==========================================================
# PHÂN TÍCH BÀI TOÁN
# ==========================================================

# 1. Input
#
# Client gửi Request Body dạng JSON:
#
# {
#     "full_name": "Nguyen Van A",
#     "email": "vana@example.com",
#     "age":20,
#     "phone":"0987654321",
#     "course":"python",
#     "note":"Muon hoc lop buoi toi"
# }
#
#
# ==========================================================
# 2. Output
# ==========================================================
#
# Nếu dữ liệu hợp lệ:
#
# {
#     "message":"Đăng ký học viên thành công",
#     "register_id":"STU1234",
#     "data":{...}
# }
#
#
# Nếu dữ liệu không hợp lệ:
#
# FastAPI trả lỗi Validate (422)
#
# Hoặc:
#
# {
#     "detail":"Số điện thoại chỉ được chứa chữ số"
# }


# ==========================================================
# LUỒNG XỬ LÝ
# ==========================================================
#
# Bước 1:
# Client gửi Request Body.
#
# Bước 2:
# FastAPI dùng Pydantic kiểm tra:
#
# - full_name >= 3 ký tự
# - email đúng định dạng
# - age từ 15 đến 60
# - phone dài từ 10 đến 11 ký tự
# - note tối đa 200 ký tự
#
# Nếu sai:
# FastAPI trả lỗi 422.
#
# Bước 3:
# Kiểm tra phone chỉ chứa số.
#
# Nếu chứa chữ:
#
# {
#     "detail":"Số điện thoại chỉ được chứa chữ số"
# }
#
# Bước 4:
# Sinh mã đăng ký.
#
# Ví dụ:
#
# STU3562
#
# Bước 5:
# Chuẩn hóa dữ liệu:
#
# full_name
# -> Viết hoa chữ cái đầu.
#
# note
# -> Chuyển thành chữ thường.
#
# Bước 6:
# Trả kết quả.


# ==========================================================
# TEST CASE THÀNH CÔNG
# ==========================================================
#
# POST /students/register
#
# {
#     "full_name":"Nguyen Van A",
#     "email":"vana@example.com",
#     "age":20,
#     "phone":"0987654321",
#     "course":"python",
#     "note":"Muon hoc lop buoi toi"
# }
#
# Kết quả:
#
# {
#     "message":"Đăng ký học viên thành công",
#     "register_id":"STU1234",
#     "data":{
#         "full_name":"Nguyen Van A",
#         "email":"vana@example.com",
#         "age":20,
#         "phone":"0987654321",
#         "course":"python",
#         "note":"muon hoc lop buoi toi"
#     }
# }


# ==========================================================
# TEST CASE THẤT BẠI
# ==========================================================
#
# 1. Thiếu email
#
# -> FastAPI trả lỗi 422.
#
#
# 2. age = 10
#
# -> FastAPI trả lỗi 422.
#
#
# 3. age = 70
#
# -> FastAPI trả lỗi 422.
#
#
# 4. phone = "09876abcde"
#
# {
#     "detail":"Số điện thoại chỉ được chứa chữ số"
# }
#
#
# 5. phone = "12345"
#
# -> FastAPI trả lỗi 422.
#
#
# 6. note dài hơn 200 ký tự
#
# -> FastAPI trả lỗi 422.
#
#
# 7. full_name = "An"
#
# -> FastAPI trả lỗi 422.