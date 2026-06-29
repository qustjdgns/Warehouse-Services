PRODUCTS = {
    "P001": {
        "name": "Logitech Keyboard",
        "stock": 30,
        "location": "A-01"
    },
    "P002": {
        "name": "Wireless Mouse",
        "stock": 18,
        "location": "B-02"
    },
    "P003": {
        "name": "USB-C Cable",
        "stock": 75,
        "location": "C-05"
    }
}


def get_product(barcode):
    # barcode로 상품 조회
    return PRODUCTS.get(barcode)


def inbound_stock(barcode, quantity):
    # 입고: 재고 증가
    product = get_product(barcode)

    if product is None:
        return False, "상품을 찾을 수 없습니다.", None

    product["stock"] += quantity

    return True, "입고 처리 완료", product


def outbound_stock(barcode, quantity):
    # 출고: 재고 감소
    product = get_product(barcode)

    if product is None:
        return False, "상품을 찾을 수 없습니다.", None

    if product["stock"] < quantity:
        return False, "출고 수량이 현재 재고보다 많습니다.", product

    product["stock"] -= quantity

    return True, "출고 처리 완료", product
