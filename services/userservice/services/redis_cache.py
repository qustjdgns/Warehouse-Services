from config.redis import redis_client

import json



def set_cache(
    key,
    data,
    expire=300
):

    redis_client.set(

        key,

        json.dumps(
            data,
            ensure_ascii=False
        ),

        ex=expire

    )





def get_cache(key):


    data = redis_client.get(
        key
    )


    if data is None:

        return None



    return json.loads(
        data
    )





def delete_cache(key):


    redis_client.delete(
        key
    )
