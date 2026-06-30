from config.database import get_connection


def get_product(barcode):
    # barcode로 상품 1개 조회
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT barcode, name, stock, location
                FROM products
                WHERE barcode = %s
            """
            cursor.execute(sql, (barcode,))
            return cursor.fetchone()
    finally:
        conn.close()


def get_products():
    # 전체 상품 목록 조회
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT barcode, name, stock, location
                FROM products
                ORDER BY barcode
            """
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        conn.close()


def inbound_stock(barcode, quantity):
    # 입고: 재고 증가
    product = get_product(barcode)

    if product is None:
        return False, "상품을 찾을 수 없습니다.", None

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE products
                SET stock = stock + %s
                WHERE barcode = %s
            """
            cursor.execute(sql, (quantity, barcode))

            history_sql = """
                INSERT INTO history (barcode, type, quantity, worker)
                VALUES (%s, 'IN', %s, %s)
            """
            cursor.execute(history_sql, (barcode, quantity, "operator"))

            conn.commit()

        updated_product = get_product(barcode)
        return True, "입고 처리 완료", updated_product

    except Exception as e:
        conn.rollback()
        return False, str(e), product

    finally:
        conn.close()


def outbound_stock(barcode, quantity):
    # 출고: 재고 감소
    product = get_product(barcode)

    if product is None:
        return False, "상품을 찾을 수 없습니다.", None

    if product["stock"] < quantity:
        return False, "출고 수량이 현재 재고보다 많습니다.", product

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE products
                SET stock = stock - %s
                WHERE barcode = %s
            """
            cursor.execute(sql, (quantity, barcode))

            history_sql = """
                INSERT INTO history (barcode, type, quantity, worker)
                VALUES (%s, 'OUT', %s, %s)
            """
            cursor.execute(history_sql, (barcode, quantity, "operator"))

            conn.commit()

        updated_product = get_product(barcode)
        return True, "출고 처리 완료", updated_product

    except Exception as e:
        conn.rollback()
        return False, str(e), product

    finally:
        conn.close()

def create_product(barcode, name, stock, location):
    # 상품 추가: products 테이블에 INSERT
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO products (barcode, name, stock, location)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (barcode, name, stock, location))

        conn.commit()
        return True, "상품 등록 완료"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        conn.close()


def update_product(barcode, name, stock, location):
    # 상품 수정: barcode 기준으로 상품 정보 UPDATE
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE products
                SET name = %s,
                    stock = %s,
                    location = %s
                WHERE barcode = %s
            """
            cursor.execute(sql, (name, stock, location, barcode))

        conn.commit()
        return True, "상품 수정 완료"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        conn.close()


def delete_product(barcode):
    # 상품 삭제: barcode 기준으로 DELETE
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            sql = """
                DELETE FROM products
                WHERE barcode = %s
            """
            cursor.execute(sql, (barcode,))

        conn.commit()
        return True, "상품 삭제 완료"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        conn.close()
