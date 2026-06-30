from fastapi import FastAPI

app = FastAPI()

# Danh sách đơn hàng
orders = [
    {"id": 1, "customer_name": "Nguyễn Văn An", "total": 250000, "status": "pending"},
    {"id": 2, "customer_name": "Trần Thị Bình", "total": 500000, "status": "paid"},
    {"id": 3, "customer_name": "Lê Văn Cường", "total": 150000, "status": "cancelled"},
    {"id": 4, "customer_name": "Phạm Thị Dung", "total": 320000, "status": "pending"}
]


# API lấy danh sách đơn hàng theo trạng thái
@app.get("/orders/status/{status}")
def get_orders_by_status(status: str):
    # Danh sách trạng thái hợp lệ
    valid_status = ["pending", "paid", "cancelled"]

    # Kiểm tra trạng thái có hợp lệ hay không
    if status not in valid_status:
        return {
            "message": "Trạng thái đơn hàng không hợp lệ"
        }

    # Lọc các đơn hàng theo trạng thái
    result = []

    for order in orders:
        if order["status"] == status:
            result.append(order)

    return result

#Phân tích lỗi
# 1. Endpoint hiện tại có Path Parameter không?
# Có.
# Endpoint:
# @app.get("/orders/status/{status}")
# Trong đó:
# {status} là Path Parameter.


# 2. Path Parameter trong bài này là gì?
# Path Parameter là:
# status
# Giá trị này được lấy trực tiếp từ URL.
# Ví dụ:
# GET /orders/status/pending
# => status = "pending"
# GET /orders/status/paid
# => status = "paid"


# 3. Khi gọi /orders/status/pending,
# biến status nhận giá trị gì?
# status sẽ nhận giá trị:
# "pending"
# FastAPI tự động lấy giá trị trong URL
# và truyền vào tham số của hàm:
# def get_orders_by_status(status: str)


# 4. Vì sao API hiện tại trả về sai dữ liệu?
# Vì mặc dù đã nhận được Path Parameter,
# chương trình lại không sử dụng biến status
# để lọc dữ liệu.
# API luôn trả về toàn bộ danh sách orders,
# nên frontend nhận cả đơn hàng pending,
# paid và cancelled.


# 5. Dòng code nào đang khiến API bỏ qua giá trị status?
# Dòng:
# return orders
# Dòng này trả về toàn bộ danh sách đơn hàng,
# không kiểm tra trạng thái của từng đơn hàng,
# nên bỏ qua hoàn toàn giá trị status
# được truyền từ URL.
