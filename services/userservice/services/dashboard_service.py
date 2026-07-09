
from config.database import get_connection

import redis
import json
import os


redis_client = redis.Redis(
    host=os.getenv(
        "REDIS_HOST",
        "localhost"
    ),
    port=6379,
    decode_responses=True
)



# -----------------------------
# 대시보드 요약 Cache
# -----------------------------
def get_dashboard_summary():


    cache_key = "dashboard:summary"


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



            cursor.execute("""
                SELECT COUNT(*) AS total_products
                FROM products
            """)

            total_products = cursor.fetchone()["total_products"]




            cursor.execute("""
                SELECT COUNT(*) AS low_stock
                FROM products
                WHERE stock <= 5
            """)

            low_stock = cursor.fetchone()["low_stock"]




            cursor.execute("""
                SELECT COALESCE(SUM(quantity),0) AS today_inbound
                FROM history
                WHERE type = 'IN'
                AND created_at::date = CURRENT_DATE
            """)

            today_inbound = cursor.fetchone()["today_inbound"]




            cursor.execute("""
                SELECT COALESCE(SUM(quantity),0) AS today_outbound
                FROM history
                WHERE type = 'OUT'
                AND created_at::date = CURRENT_DATE
            """)

            today_outbound = cursor.fetchone()["today_outbound"]



            result = {

                "total_products":
                total_products,

                "today_inbound":
                today_inbound,

                "today_outbound":
                today_outbound,

                "low_stock":
                low_stock

            }



            redis_client.set(

                cache_key,

                json.dumps(result),

                ex=300

            )



            return result



    finally:

        conn.close()





# -----------------------------
# 재고 차트 Cache
# -----------------------------
def get_inventory_chart():


    cache_key = "dashboard:inventory-chart"


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


            cursor.execute("""
                SELECT name, stock
                FROM products
                ORDER BY barcode
            """)


            result = cursor.fetchall()



            redis_client.set(

                cache_key,

                json.dumps(result),

                ex=300

            )



            return result



    finally:

        conn.close()





# -----------------------------
# 최근 입출고 기록 Cache
# -----------------------------
def get_recent_history():


    cache_key = "dashboard:recent-history"


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


            cursor.execute("""
                SELECT
                    h.barcode,
                    p.name AS product_name,
                    h.type,
                    h.quantity,
                    h.worker,
                    TO_CHAR(
                        h.created_at,
                        'HH24:MI'
                    ) AS time
                FROM history h
                LEFT JOIN products p
                ON h.barcode = p.barcode
                ORDER BY h.created_at DESC
                LIMIT 5
            """)


            result = cursor.fetchall()



            redis_client.set(

                cache_key,

                json.dumps(result),

                ex=60

            )



            return result



    finally:

        conn.close()





# -----------------------------
# 재고 부족 상품 Cache
# -----------------------------
def get_low_stock_products():


    cache_key = "dashboard:low-stock"



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


            cursor.execute("""
                SELECT
                    barcode,
                    name,
                    stock,
                    location
                FROM products
                WHERE stock <= 5
                ORDER BY stock ASC
                LIMIT 5
            """)



            result = cursor.fetchall()



            redis_client.set(

                cache_key,

                json.dumps(result),

                ex=300

            )



            return result



    finally:

        conn.close()
