from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from services.payment_service import create_payment
from keyboards.inline import payment_link_keyboard

router = Router()


# ==============================
# GOOGLE ADS PURCHASE
# ==============================

@router.callback_query(F.data == "buy_google")
async def buy_google(callback: CallbackQuery):
    await callback.answer()

    payment_url = await create_payment(
        user_id=callback.from_user.id,
        product_key="google"
    )

    await callback.message.answer(
        "💳 Complete your payment below:",
        reply_markup=payment_link_keyboard(payment_url)
    )


# ==============================
# META ADS PURCHASE
# ==============================

@router.callback_query(F.data == "buy_meta")
async def buy_meta(callback: CallbackQuery):
    await callback.answer()

    payment_url = await create_payment(
        user_id=callback.from_user.id,
        product_key="meta"
    )

    await callback.message.answer(
        "💳 Complete your payment below:",
        reply_markup=payment_link_keyboard(payment_url)
    )


# ==============================
# PREMIUM CONTACT
# ==============================

@router.callback_query(F.data == "contact_premium")
async def contact_premium(callback: CallbackQuery):
    await callback.answer()

    await callback.message.answer(
        "💎 Premium Package\n\n"
        "Please contact me directly to proceed with private sales.\n\n"
        "📩 @your_username"
    )
