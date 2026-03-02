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
                        },
                        # 🔥 ОСЬ ГОЛОВНЕ
                        "custom_id": f"{user_id}|{product_key}"
                    }
                ],
                "application_context": {
                    "return_url": f"{APP_BASE_URL}/success",
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
