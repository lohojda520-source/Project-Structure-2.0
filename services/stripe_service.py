import stripe
from config import STRIPE_SECRET_KEY, BASE_URL
from data.products import PRODUCTS

stripe.api_key = STRIPE_SECRET_KEY

def create_checkout_session(product_key, telegram_id):
    product = PRODUCTS[product_key]

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": product["name"],
                },
                "unit_amount": product["price"],
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"{BASE_URL}/success",
        cancel_url=f"{BASE_URL}/cancel",
        metadata={
            "telegram_id": telegram_id,
            "product_key": product_key
        }
    )

    return session.url