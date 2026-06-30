from fastapi import FastAPI

app = FastAPI()

# Danh sách sản phẩm
products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000}
]


# API tìm kiếm và lọc sản phẩm
@app.get("/products")
def get_products(keyword: str = None, max_price: float = None):

    # Kiểm tra giá tối đa có hợp lệ hay không
    if max_price is not None and max_price < 0:
        return {
            "detail": "max_price không được âm"
        }

    result = []

    # Duyệt từng sản phẩm
    for product in products:

        # Giả sử sản phẩm hợp lệ
        is_match = True

        # Lọc theo từ khóa
        if keyword is not None:
            if keyword.lower() not in product["name"].lower():
                is_match = False

        # Lọc theo giá tối đa
        if max_price is not None:
            if product["price"] > max_price:
                is_match = False

        # Nếu thỏa mãn điều kiện thì thêm vào kết quả
        if is_match:
            result.append(product)

    return result


#Phân tích
# 1. Input của bài toán là gì?
# Input gồm:
# - Danh sách sản phẩm (products)
# - Query Parameter:
#   + keyword (không bắt buộc)
#   + max_price (không bắt buộc)
# Ví dụ:
# GET /products
# GET /products?keyword=mouse
# GET /products?max_price=1000000
# GET /products?keyword=mouse&max_price=300000


# 2. Output mong muốn là gì?
# Trả về danh sách sản phẩm phù hợp với điều kiện tìm kiếm.
# Nếu không truyền query parameter
# -> trả về toàn bộ sản phẩm.
# Nếu truyền keyword
# -> trả về sản phẩm có tên chứa keyword.
# Nếu truyền max_price
# -> trả về sản phẩm có giá nhỏ hơn hoặc bằng max_price.
# Nếu truyền cả hai
# -> sản phẩm phải thỏa mãn cả hai điều kiện.
# Nếu max_price < 0
# {
#     "detail": "max_price không được âm"
# }

# 3. Đề xuất giải pháp xử lý bài toán
# Bước 1:
# Nhận Query Parameter từ URL.
# Bước 2:
# Kiểm tra max_price.
# Nếu max_price nhỏ hơn 0
# -> trả về thông báo lỗi.
# Bước 3:
# Duyệt toàn bộ danh sách products.
# Bước 4:
# Kiểm tra từng điều kiện:
# - keyword
# - max_price
# Bước 5:
# Nếu sản phẩm thỏa mãn tất cả điều kiện
# thì thêm vào danh sách kết quả.
# Bước 6:
# Trả về danh sách kết quả.

