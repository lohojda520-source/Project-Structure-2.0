from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


async def show_products(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Google Ads – $49", callback_data="buy_google")],
        [InlineKeyboardButton(text="Meta Ads – $79", callback_data="buy_meta")]
    ])

    await message.answer(
        "🚀 Digital Marketing Systems\n\n"
        "💰 Google Ads – $49\n"
        "📈 Meta Ads – $79\n\n"
        "Select an option below:",
        reply_markup=keyboard
    )


@router.message(Command("start"))
async def start_handler(message: Message):
    await show_products(message)


@router.message(Command("products"))
async def products_handler(message: Message):
    await show_products(message)
