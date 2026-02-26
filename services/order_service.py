import json
from pathlib import Path

ORDERS_FILE = Path("data/orders.json")


def load_orders():
    if not ORDERS_FILE.exists():
        return {}

    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_orders(data):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def order_exists(order_id: str) -> bool:
    orders = load_orders()
    return order_id in orders


def save_order(order_id: str, telegram_id: str, product_key: str):
    orders = load_orders()

    orders[order_id] = {
        "telegram_id": telegram_id,
        "product": product_key,
        "status": "completed"
    }

    save_orders(orders)