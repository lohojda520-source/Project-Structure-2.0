from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# ==============================
# KEYBOARDS
# ==============================

def plans_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 SmartAdminBot Lite – $49", callback_data="buy_lite")],
        [InlineKeyboardButton(text="🔥 SmartAdminBot Pro – $79", callback_data="buy_pro")],
    ])


def confirm_keyboard(plan: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Proceed to Payment", callback_data=f"confirm_{plan}")],
        [InlineKeyboardButton(text="⬅ Back", callback_data="back_to_plans")]
    ])


# ==============================
# START
# ==============================

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "🚀 Welcome to SmartAdminBot\n\n"
        "Automation system for traffic, leads & sales inside Telegram.\n\n"
        "• One-time payment\n"
        "• Instant delivery\n"
        "• Lifetime access\n\n"
        "Tap below to choose your plan 👇",
        reply_markup=plans_keyboard()
    )


@router.message(Command("products"))
async def products_handler(message: Message):
    await start_handler(message)


# ==============================
# SHOW PLANS (back button)
# ==============================

@router.callback_query(F.data == "back_to_plans")
async def back_to_plans(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔥 Choose your SmartAdminBot version:\n\n"
        "🚀 Lite – Ready-to-use advertising system\n"
        "🔥 Pro – Advanced automation + scaling tools\n\n"
        "Select your version below:",
        reply_markup=plans_keyboard()
    )


# ==============================
# SELECT PLAN
# ==============================

@router.callback_query(F.data == "buy_lite")
async def choose_lite(callback: CallbackQuery):
    await callback.message.edit_text(
        "You selected: 🚀 SmartAdminBot Lite – $49\n\n"
        "After payment you will receive:\n"
        "• Product file\n"
        "• Setup guide\n"
        "• Lifetime updates\n\n"
        "Proceed to payment?",
        reply_markup=confirm_keyboard("google")  # залишаємо твої ключі
    )


@router.callback_query(F.data == "buy_pro")
async def choose_pro(callback: CallbackQuery):
    await callback.message.edit_text(
        "You selected: 🔥 SmartAdminBot Pro – $79\n\n"
        "After payment you will receive:\n"
        "• Product file\n"
        "• Setup guide\n"
        "• Lifetime updates\n\n"
        "Proceed to payment?",
        reply_markup=confirm_keyboard("meta")  # залишаємо твої ключі
    )
