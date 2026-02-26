from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "contact_premium")
async def premium_contact(callback: CallbackQuery):
    await callback.answer()

    await callback.message.answer(
        "💎 PREMIUM PACKAGE\n\n"
        "Personal setup & private sales.\n\n"
        "📩 Contact me directly to proceed.\n\n"
        "@your_username"
    )
