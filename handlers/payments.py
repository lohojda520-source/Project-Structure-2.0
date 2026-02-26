from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.payment_service import create_payment
from data.products import PRODUCTS

router = Router()


@router.callback_query(F.data.startswith("buy_"))
async def buy_handler(callback: CallbackQuery):
    await callback.answer()

    product_key = callback.data.split("_")[1]

    if product_key not in PRODUCTS:
        await callback.message.answer("Product not found.")
        return

    product = PRODUCTS[product_key]

    approval_url = await create_payment(   # ← якщо async
        product_name=product["name"],
        price=product["price"],
        telegram_id=str(callback.from_user.id),
        product_key=product_key
    )

    await callback.message.answer(
        f"💳 Complete your payment below:\n\n{approval_url}"
    )
