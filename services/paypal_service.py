import os
import requests
from requests.auth import HTTPBasicAuth

from config import PAYPAL_CLIENT_ID, PAYPAL_SECRET, PAYPAL_BASE

APP_BASE_URL = os.getenv("APP_BASE_URL")


# ==============================
# GET ACCESS TOKEN
# ==============================

def get_access_token():
    response = requests.post(
        f"{PAYPAL_BASE}/v1/oauth2/token",
        headers={"Accept": "application/json"},
        data={"grant_type": "client_credentials"},
        auth=HTTPBasicAuth(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
    )

    response.raise_for_status()
    return response.json()["access_token"]


# ==============================
# CREATE ORDER
# ==============================

def create_payment(product_name: str, price: float, telegram_id: str, product_key: str):

    access_token = get_access_token()

    response = requests.post(
        f"{PAYPAL_BASE}/v2/checkout/orders",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": f"{price:.2f}"
                },
                "description": product_name,
                "custom_id": f"{telegram_id}|{product_key}"
            }],
            "application_context": {
                "return_url": f"{APP_BASE_URL}/success",
                "cancel_url": f"{APP_BASE_URL}/cancel"
            }
        }
    )

    response.raise_for_status()
    data = response.json()

    for link in data["links"]:
        if link["rel"] == "approve":
            return link["href"]

    return None


# ==============================
# CAPTURE PAYMENT
# ==============================

def capture_payment(order_id: str):

    access_token = get_access_token()

    response = requests.post(
        f"{PAYPAL_BASE}/v2/checkout/orders/{order_id}/capture",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
    )

    response.raise_for_status()
    return response.json()