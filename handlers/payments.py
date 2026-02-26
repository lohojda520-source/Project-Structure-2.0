from aiogram import Router, F
from aiogram.types import CallbackQuery
from paypal_service import create_payment
from data.products import PRODUCTS

router = Router()

@router.callback_query(F.data.startswith("buy_"))
async def buy_handler(callback: CallbackQuery):
    product_key = callback.data.split("_")[1]
    product = PRODUCTS[product_key]

    approval_url = create_payment(
        product_name=product["name"],
        price=product["price"],
        telegram_id=str(callback.from_user.id),
        product_key=product_key
    )

    await callback.message.answer(
        f"Complete payment:\n{approval_url}"
    )