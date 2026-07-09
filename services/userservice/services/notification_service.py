from config.redis import redis_client

import json



def save_low_stock_notification(event):


    key = "notifications:low-stock"



    notifications = []



    cached = redis_client.get(
        key
    )



    if cached:


        notifications = json.loads(
            cached
        )



    notifications.append(

        {

            "barcode":
            event.get("barcode"),

            "name":
            event.get("name"),

            "stock":
            event.get("stock")

        }

    )



    # 최근 20개만 유지

    notifications = notifications[-20:]



    redis_client.set(

        key,

        json.dumps(
            notifications
        ),

        ex=3600

    )



    return True
