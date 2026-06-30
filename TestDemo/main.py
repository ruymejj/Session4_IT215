from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title = "Manager Student",
    description = "Đây là API cùng cấp để quản lí sinh viên cá biệt",
    version= "1.0.0"
)
#VD danh sách sinh viên này được lấy từ database về
student_database = [
    {"Id": 1, "username": "Quang Long", "Password": "123456"},
    {"Id": 2, "username": "Xuân Tân", "Password": "654321"}
]

#Định hình dữ liệu ng dùng nhập vào
class StudentSchema(BaseModel):
    id : int
    username : str
    Password : str

#Tạo API để lấy danh sách sinh viên
@app.get("/students", tags = ["Students"], summary = "Lấy danh sách sinh viên")
def get_all_students():
    return {
        "status_code": 200,
        "message": "Lấy danh sách sinh viên thành công",
        "data": student_database
    }

#Tạo API để thêm dữ liệu mới. Method: GET, POST, PUT, PATCH, and DELETE
@app.post("/students", tags= ["Create Student"])
def create_student(student: StudentSchema):
    student_id = len(student_database) + 1
    new_student = {
        "id": student_id,
        "username": student.username,
        "Password": student.Password
    }

    student_database.append(new_student)
    return {
        "status_code": 201,
        "Message": "Thêm thành công sinh viên",
        "data": new_student
    }

#Lấy API một sinh viên
@app.get("/students/{student_id}")