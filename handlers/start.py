from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message()
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Google Ads – $49", callback_data="buy_google")],
        [InlineKeyboardButton(text="Facebook Ads – $79", callback_data="buy_facebook")],
        [InlineKeyboardButton(text="Premium – $997", callback_data="buy_premium")]
    ])

    await message.answer(
        "Choose a product:",
        reply_markup=keyboard
    )