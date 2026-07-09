from flask import Blueprint, request, jsonify

from services.product_service import (
    get_products,
    get_product,
    create_product,
    update_product,
    delete_product
)



products_bp = Blueprint(
    "products",
    __name__
)





@products_bp.route(
    "/products",
    methods=["GET"]
)
def products():

    return jsonify(
        get_products()
    )





@products_bp.route(
    "/products/<barcode>",
    methods=["GET"]
)
def product_detail(barcode):


    product = get_product(
        barcode
    )



    if product is None:

        return jsonify({

            "error":
            "상품을 찾을 수 없습니다."

        }),404




    return jsonify(
        product
    )






@products_bp.route(
    "/products",
    methods=["POST"]
)
def product_create():


    data = request.get_json()



    if not data:

        return jsonify({

            "error":
            "JSON 데이터가 필요합니다."

        }),400




    success, message = create_product(

        data.get("barcode"),

        data.get("name"),

        data.get("stock",0),

        data.get("location")

    )



    if not success:

        return jsonify({

            "error":
            message

        }),400




    return jsonify({

        "message":
        message

    })






@products_bp.route(
    "/products/<barcode>",
    methods=["PUT"]
)
def product_update(barcode):


    data = request.get_json()



    if not data:

        return jsonify({

            "error":
            "JSON 데이터가 필요합니다."

        }),400




    success, message = update_product(

        barcode,

        data.get("name"),

        data.get("stock"),

        data.get("location")

    )



    if not success:

        return jsonify({

            "error":
            message

        }),400




    return jsonify({

        "message":
        message

    })







@products_bp.route(
    "/products/<barcode>",
    methods=["DELETE"]
)
def product_delete(barcode):


    success, message = delete_product(
        barcode
    )



    if not success:

        return jsonify({

            "error":
            message

        }),400




    return jsonify({

        "message":
        message

    })
