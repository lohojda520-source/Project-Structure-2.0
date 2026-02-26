from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):

    text = (
        "📢 *IMPORTANT INFORMATION*\n\n"
        "Advertising platforms constantly update their algorithms and interfaces.\n\n"
        "All materials are aligned with the latest updates of Google Ads and Meta Ads.\n\n"
        "🛡 Validity guarantee — 60 days or until major interface changes occur.\n\n"
        "━━━━━━━━━━━━━━━\n"
        "*Choose a package below:* 👇"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Google Ads – $49", callback_data="buy_google")],
        [InlineKeyboardButton(text="Meta Ads – $79", callback_data="buy_meta")],
        [InlineKeyboardButton(text="Premium – $997", callback_data="buy_premium")]
    ])

    await message.answer(
        text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
