from fastapi import FastAPI

app = FastAPI()

# Danh sách sản phẩm
products = [
    {"id": 1, "name": "Laptop Dell", "price": 15000000},
    {"id": 2, "name": "Chuột Logitech", "price": 350000},
    {"id": 3, "name": "Bàn phím cơ", "price": 1200000}
]


# API lấy chi tiết sản phẩm theo ID
@app.get("/products/{product_id}")
def get_product_detail(product_id: int):
    # Duyệt danh sách để tìm sản phẩm có id trùng với product_id
    for product in products:
        if product["id"] == product_id:
            return product

    # Không tìm thấy sản phẩm
    return {
        "message": "Không tìm thấy sản phẩm"
    }

# 1. 
# Vì ban đầu endpoint được khai báo:
# @app.get("/products/product_id")
#
# FastAPI hiểu đây là một đường dẫn cố định:
# /products/product_id
#
# Khi người dùng gọi:
# GET /products/1
#
# FastAPI không tìm thấy endpoint nào khớp với URL này,
# nên trả về lỗi 404 Not Found.


# 2. 
# Sai:
# @app.get("/products/product_id")
# Đúng:
# @app.get("/products/{product_id}")


# 3. 
# Vì "product_id" không được đặt trong dấu {}.
# FastAPI chỉ coi giá trị trong {} là biến được lấy từ URL.
# Ví dụ:
# /products/{product_id}
# Khi đó:
# GET /products/1
# -> product_id = 1
# GET /products/2
# -> product_id = 2


# 4.
# @app.get("/products/{product_id}")
# Tên trong {} phải trùng với tên tham số của hàm:
# def get_product_detail(product_id: int):
# Nếu tên không trùng, FastAPI sẽ không truyền được giá trị.


