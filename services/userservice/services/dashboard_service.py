from config.database import get_connection


def get_dashboard_summary():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            # 전체 상품 수
            cursor.execute("""
                SELECT COUNT(*) AS total_products
                FROM products
            """)
            total_products = cursor.fetchone()["total_products"]

            # 재고 부족 상품 수
            cursor.execute("""
                SELECT COUNT(*) AS low_stock
                FROM products
                WHERE stock <= 5
            """)
            low_stock = cursor.fetchone()["low_stock"]

            # 오늘 입고 수량 합계
            cursor.execute("""
                SELECT COALESCE(SUM(quantity), 0) AS today_inbound
                FROM history
                WHERE type = 'IN'
                AND DATE(created_at) = CURDATE()
            """)
            today_inbound = cursor.fetchone()["today_inbound"]

            # 오늘 출고 수량 합계
            cursor.execute("""
                SELECT COALESCE(SUM(quantity), 0) AS today_outbound
                FROM history
                WHERE type = 'OUT'
                AND DATE(created_at) = CURDATE()
            """)
            today_outbound = cursor.fetchone()["today_outbound"]

            return {
                "total_products": total_products,
                "today_inbound": today_inbound,
                "today_outbound": today_outbound,
                "low_stock": low_stock
            }

    finally:
        conn.close()


def get_inventory_chart():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            # 상품별 재고 차트용 데이터
            cursor.execute("""
                SELECT name, stock
                FROM products
                ORDER BY barcode
            """)
            return cursor.fetchall()

    finally:
        conn.close()


def get_recent_history():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            # 최근 입출고 이력
            cursor.execute("""
                SELECT 
                    h.barcode,
                    p.name AS product_name,
                    h.type,
                    h.quantity,
                    h.worker,
                    DATE_FORMAT(h.created_at, '%H:%i') AS time
                FROM history h
                LEFT JOIN products p ON h.barcode = p.barcode
                ORDER BY h.created_at DESC
                LIMIT 5
            """)
            return cursor.fetchall()

    finally:
        conn.close()


def get_low_stock_products():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            # 재고 부족 상품 목록
            cursor.execute("""
                SELECT barcode, name, stock, location
                FROM products
                WHERE stock <= 5
                ORDER BY stock ASC
                LIMIT 5
            """)
            return cursor.fetchall()

    finally:
        conn.close()
