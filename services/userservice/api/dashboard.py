from flask import Blueprint, jsonify

from services.dashboard_service import (
    get_dashboard_summary,
    get_inventory_chart,
    get_recent_history,
    get_low_stock_products
)


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)



@dashboard_bp.route(
    "/dashboard/summary",
    methods=["GET"]
)
def dashboard_summary():

    return jsonify(
        get_dashboard_summary()
    )




@dashboard_bp.route(
    "/dashboard/inventory-chart",
    methods=["GET"]
)
def dashboard_inventory_chart():

    return jsonify(
        get_inventory_chart()
    )




@dashboard_bp.route(
    "/dashboard/recent-history",
    methods=["GET"]
)
def dashboard_recent_history():

    return jsonify(
        get_recent_history()
    )




@dashboard_bp.route(
    "/dashboard/low-stock",
    methods=["GET"]
)
def dashboard_low_stock():

    return jsonify(
        get_low_stock_products()
    )
