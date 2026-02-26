from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from services.paypal_service import create_payment
from data.products import PRODUCTS

router = Router()


@router.callback_query(F.data.startswith("buy_"))
async def buy_handler(callback: CallbackQuery):
    await callback.answer()

    product_key = callback.data.replace("buy_", "")
    product = PRODUCTS.get(product_key)

    if not product:
        await callback.message.answer("❌ Product not found.")
        return

    approval_url = create_payment(
        product_name=product["name"],
        price=product["price"],
        telegram_id=str(callback.from_user.id),
        product_key=product_key
    )

    if not approval_url:
        await callback.message.answer("❌ Failed to create PayPal payment.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Pay with PayPal", url=approval_url)]
    ])

    await callback.message.answer(
        "Click the button below to complete your payment:",
        reply_markup=keyboard
    )
