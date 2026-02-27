from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


async def show_products(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 SmartAdminBot Lite – $49", callback_data="buy_google")],
        [InlineKeyboardButton(text="🔥 SmartAdminBot Pro – $79", callback_data="buy_meta")],
    ])

    await message.answer(
        "🔥 Choose your SmartAdminBot version:\n\n"
        "🚀 Lite – Ready-to-use advertising system\n"
        "🔥 Pro – Advanced automation + scaling tools\n\n"
        "Select your version below:",
        reply_markup=keyboard
    )


@router.message(Command("start"))
async def start_handler(message: Message):
    await show_products(message)


@router.message(Command("products"))
async def products_handler(message: Message):
    await show_products(message)
