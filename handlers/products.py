from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


async def show_products(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Google Ads – $49", callback_data="buy_google")],
        [InlineKeyboardButton(text="Facebook Ads – $79", callback_data="buy_meta")],
        [InlineKeyboardButton(text="Premium – $997", callback_data="buy_premium")]
    ])

    await message.answer(
        "🔥 Choose your package:\n\n"
        "💰 Google Ads – Starter package\n"
        "📈 Facebook Ads – Growth package\n"
        "🚀 Premium – Full Marketing Suite\n\n"
        "Select an option below:",
        reply_markup=keyboard
    )


@router.message(Command("start"))
async def start_handler(message: Message):
    await show_products(message)


@router.message(Command("products"))
async def products_handler(message: Message):
    await show_products(message)
