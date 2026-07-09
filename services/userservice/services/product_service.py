from config.database import get_connection
from config.redis import redis_client

import json



# 상품 단건 조회 (Redis Cache)
def get_product(barcode):

    cache_key = f"product:{barcode}"


    cached = redis_client.get(
        cache_key
    )


    if cached:

        return json.loads(
            cached
        )



    conn = get_connection()


    try:

        with conn.cursor() as cursor:


            sql = """
                SELECT barcode,
                       name,
                       stock,
                       location
                FROM products
                WHERE barcode = %s
            """


            cursor.execute(
                sql,
                (barcode,)
            )


            product = cursor.fetchone()



            if product:

                redis_client.set(

                    cache_key,

                    json.dumps(product),

                    ex=300

                )



            return product



    finally:

        conn.close()





# 전체 상품 조회
def get_products():

    conn = get_connection()


    try:

        with conn.cursor() as cursor:


            cursor.execute("""
                SELECT barcode,
                       name,
                       stock,
                       location
                FROM products
                ORDER BY barcode
            """)


            return cursor.fetchall()



    finally:

        conn.close()





# 입고
def inbound_stock(
        barcode,
        quantity,
        worker="system"
):

    product = get_product(
        barcode
    )


    if product is None:

        return False, "상품을 찾을 수 없습니다.", None



    conn = get_connection()


    try:

        with conn.cursor() as cursor:


            cursor.execute(
                """
                UPDATE products
                SET stock = stock + %s
                WHERE barcode = %s
                """,
                (
                    quantity,
                    barcode
                )
            )



            cursor.execute(
                """
                INSERT INTO history
                (barcode,type,quantity,worker)
                VALUES (%s,'IN',%s,%s)
                """,
                (
                    barcode,
                    quantity,
                    worker
                )
            )


            conn.commit()



        redis_client.delete(
            f"product:{barcode}"
        )


        return True, "입고 처리 완료", get_product(barcode)



    except Exception as e:


        conn.rollback()

        return False, str(e), product



    finally:

        conn.close()





# 출고
def outbound_stock(
        barcode,
        quantity,
        worker="system"
):

    product = get_product(
        barcode
    )


    if product is None:

        return False, "상품을 찾을 수 없습니다.", None



    if product["stock"] < quantity:

        return False, "재고 부족", product



    conn = get_connection()



    try:

        with conn.cursor() as cursor:


            cursor.execute(
                """
                UPDATE products
                SET stock = stock - %s
                WHERE barcode = %s
                """,
                (
                    quantity,
                    barcode
                )
            )


            cursor.execute(
                """
                INSERT INTO history
                (barcode,type,quantity,worker)
                VALUES (%s,'OUT',%s,%s)
                """,
                (
                    barcode,
                    quantity,
                    worker
                )
            )


            conn.commit()



        redis_client.delete(
            f"product:{barcode}"
        )


        return True, "출고 처리 완료", get_product(barcode)



    except Exception as e:


        conn.rollback()

        return False, str(e), product



    finally:

        conn.close()
