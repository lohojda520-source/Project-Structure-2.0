from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# ==============================
# KEYBOARDS
# ==============================

def plans_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 SmartAdminBot Lite – $49", callback_data="buy_google")],
        [InlineKeyboardButton(text="🔥 SmartAdminBot Pro – $79 (Best Value)", callback_data="buy_meta")],
    ])


def confirm_keyboard(product_key: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Proceed to Payment", callback_data=f"confirm_{product_key}")],
        [InlineKeyboardButton(text="⬅ Back", callback_data="back_to_start")]
    ])


# ==============================
# START
# ==============================

START_TEXT = (
    "🚀 Welcome to SmartAdminBot\n\n"
    "Turn Telegram into a fully automated sales machine.\n\n"
    "✔ Capture leads automatically\n"
    "✔ Reply instantly 24/7\n"
    "✔ Close sales on autopilot\n"
    "✔ Works in any niche\n\n"
    "Trusted by 147+ Telegram creators 🚀\n\n"
    "• One-time payment\n"
    "• Instant delivery\n"
    "• Lifetime access\n"
    "• No monthly fees\n\n"
    "Choose your plan below 👇\n"
    "⚡ Early pricing may increase soon"
)


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(START_TEXT, reply_markup=plans_keyboard())


@router.message(Command("products"))
async def products_handler(message: Message):
    await message.answer(START_TEXT, reply_markup=plans_keyboard())


# ==============================
# BACK TO START
# ==============================

@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery):
    await callback.message.answer(START_TEXT, reply_markup=plans_keyboard())
    await callback.answer()


# ==============================
# SELECT PLAN
# ==============================

@router.callback_query(F.data == "buy_google")
async def choose_lite(callback: CallbackQuery):
    await callback.message.answer(
        "You selected: 🚀 SmartAdminBot Lite – $49\n\n"
        "Includes:\n"
        "• Ready-to-use system\n"
        "• Setup instructions\n"
        "• Lifetime access\n\n"
        "Proceed to payment?",
        reply_markup=confirm_keyboard("google")
    )
    await callback.answer()


@router.callback_query(F.data == "buy_meta")
async def choose_pro(callback: CallbackQuery):
    await callback.message.answer(
        "You selected: 🔥 SmartAdminBot Pro – $79 (Best Value)\n\n"
        "Includes:\n"
        "• Advanced automation system\n"
        "• Scaling framework\n"
        "• Priority updates\n"
        "• Lifetime access\n\n"
        "Proceed to payment?",
        reply_markup=confirm_keyboard("meta")
    )
    await callback.answer()
