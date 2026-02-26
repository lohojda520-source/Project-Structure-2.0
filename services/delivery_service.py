from aiogram import Bot
from data.products import PRODUCTS

async def deliver_product(bot: Bot, telegram_id: int, product_key: str):
    product = PRODUCTS[product_key]

    with open(product["file"], "rb") as file:
        await bot.send_document(
            chat_id=telegram_id,
            document=file,
            caption=f"✅ Your purchase: {product['name']}"
        )