import aiohttp
import base64
import os


PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
PAYPAL_BASE = os.getenv("PAYPAL_BASE")
APP_BASE_URL = os.getenv("APP_BASE_URL")


# ==============================
# GET PAYPAL ACCESS TOKEN
# ==============================

async def get_access_token():
    auth = base64.b64encode(
        f"{PAYPAL_CLIENT_ID}:{PAYPAL_SECRET}".encode()
    ).decode()

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{PAYPAL_BASE}/v1/oauth2/token",
            headers={
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"grant_type": "client_credentials"},
        ) as response:
            data = await response.json()

            if "access_token" not in data:
                raise Exception(f"PayPal Auth Error: {data}")

            return data["access_token"]


# ==============================
# CREATE PAYMENT ORDER
# ==============================

async def create_payment(user_id: int, product_key: str):
    access_token = await get_access_token()

    amount = get_product_price(product_key)

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{PAYPAL_BASE}/v2/checkout/orders",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "USD",
                            "value": f"{amount:.2f}"
                        }
                    }
                ],
                "application_context": {
                    "return_url": f"{APP_BASE_URL}/success?user_id={user_id}&product={product_key}",
                    "cancel_url": f"{APP_BASE_URL}/cancel"
                }
            },
        ) as response:
            data = await response.json()

            if "links" not in data:
                raise Exception(f"PayPal Order Error: {data}")

            for link in data["links"]:
                if link["rel"] == "approve":
                    return link["href"]

            raise Exception("Approval link not found")


# ==============================
# CAPTURE PAYMENT AFTER SUCCESS
# ==============================

async def capture_payment(order_id: str):
    access_token = await get_access_token()

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{PAYPAL_BASE}/v2/checkout/orders/{order_id}/capture",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        ) as response:
            data = await response.json()

            if data.get("status") != "COMPLETED":
                raise Exception(f"Payment capture failed: {data}")

            return data


# ==============================
# PRODUCT PRICE LOGIC
# ==============================

def get_product_price(product_key: str) -> float:
    prices = {
        "google": 49.00,
        "meta": 79.00,
        "premium": 197.00
    }

    return prices.get(product_key, 49.00)
