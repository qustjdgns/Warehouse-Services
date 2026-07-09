from config.database import get_connection
import redis
import json


# Redis 연결
redis_client = redis.Redis(
    host="redis-service",
    port=6379,
    decode_responses=True
)


# ----------------------------
# 상품 단건 조회 (Redis 적용)
# ----------------------------
def get_product(barcode):

    cache_key = f"product:{barcode}"

    # 1. Redis 조회
    cached_product = redis_client.get(cache_key)

    if cached_product:
        return json.loads(cached_product)


    # 2. PostgreSQL/MariaDB 조회
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            sql = """
                SELECT barcode, name, stock, location
                FROM products
                WHERE barcode = %s
            """

            cursor.execute(
                sql,
                (barcode,)
            )

            product = cursor.fetchone()


            # 3. Redis 저장
            if product:

                redis_client.set(
                    cache_key,
                    json.dumps(product),
                    ex=300
                )


            return product


    finally:
        conn.close()



# ----------------------------
# 전체 상품 조회
# ----------------------------
def get_products():

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



# ----------------------------
# 입고 처리
# ----------------------------
def inbound_stock(barcode, quantity, worker="system"):

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

            cursor.execute(
                sql,
                (
                    quantity,
                    barcode
                )
            )


            history_sql = """
                INSERT INTO history
                (barcode, type, quantity, worker)
                VALUES (%s, 'IN', %s, %s)
            """

            cursor.execute(
                history_sql,
                (
                    barcode,
                    quantity,
                    worker
                )
            )


            conn.commit()


        # 캐시 삭제
        redis_client.delete(
            f"product:{barcode}"
        )


        updated_product = get_product(barcode)

        return True, "입고 처리 완료", updated_product


    except Exception as e:

        conn.rollback()

        return False, str(e), product


    finally:

        conn.close()



# ----------------------------
# 출고 처리
# ----------------------------
def outbound_stock(barcode, quantity, worker="system"):

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


            cursor.execute(
                sql,
                (
                    quantity,
                    barcode
                )
            )



            history_sql = """
                INSERT INTO history
                (barcode, type, quantity, worker)
                VALUES (%s, 'OUT', %s, %s)
            """


            cursor.execute(
                history_sql,
                (
                    barcode,
                    quantity,
                    worker
                )
            )


            conn.commit()



        # 캐시 삭제
        redis_client.delete(
            f"product:{barcode}"
        )


        updated_product = get_product(barcode)

        return True, "출고 처리 완료", updated_product



    except Exception as e:

        conn.rollback()

        return False, str(e), product



    finally:

        conn.close()




# ----------------------------
# 상품 등록
# ----------------------------
def create_product(barcode, name, stock, location):

    conn = get_connection()


    try:

        with conn.cursor() as cursor:

            sql = """
                INSERT INTO products
                (barcode, name, stock, location)
                VALUES (%s, %s, %s, %s)
            """


            cursor.execute(
                sql,
                (
                    barcode,
                    name,
                    stock,
                    location
                )
            )


        conn.commit()


        return True, "상품 등록 완료"



    except Exception as e:

        conn.rollback()

        return False, str(e)



    finally:

        conn.close()




# ----------------------------
# 상품 수정
# ----------------------------
def update_product(barcode, name, stock, location):

    conn = get_connection()


    try:

        with conn.cursor() as cursor:

            sql = """
                UPDATE products
                SET name=%s,
                    stock=%s,
                    location=%s
                WHERE barcode=%s
            """


            cursor.execute(
                sql,
                (
                    name,
                    stock,
                    location,
                    barcode
                )
            )


        conn.commit()


        redis_client.delete(
            f"product:{barcode}"
        )


        return True, "상품 수정 완료"



    except Exception as e:

        conn.rollback()

        return False, str(e)



    finally:

        conn.close()




# ----------------------------
# 상품 삭제
# ----------------------------
def delete_product(barcode):

    conn = get_connection()


    try:

        with conn.cursor() as cursor:

            sql = """
                DELETE FROM products
                WHERE barcode=%s
            """


            cursor.execute(
                sql,
                (barcode,)
            )


        conn.commit()


        redis_client.delete(
            f"product:{barcode}"
        )


        return True, "상품 삭제 완료"



    except Exception as e:

        conn.rollback()

        return False, str(e)



    finally:

        conn.close()
