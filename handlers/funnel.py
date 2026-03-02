from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

router = Router()

# ==============================
# KEYBOARDS
# ==============================

def plans_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🚀 SmartAdminBot Lite – $49",
                callback_data="select_lite"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔥 SmartAdminBot Pro – $79 (Best Value)",
                callback_data="select_pro"
            )
        ]
    ])


def confirm_keyboard(product_key: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💳 Proceed to Payment",
                callback_data=f"buy_{product_key}"  # йде в payments.py
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅ Back",
                callback_data="back_to_plans"
            )
        ]
    ])


# ==============================
# START
# ==============================

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "🚀 Welcome to SmartAdminBot\n\n"
        "Turn Telegram into an automated sales machine.\n\n"
        "✔ Capture leads automatically\n"
        "✔ Reply instantly 24/7\n"
        "✔ Close sales on autopilot\n\n"
        "• One-time payment\n"
        "• Instant delivery\n"
        "• Lifetime access\n\n"
        "Choose your plan below 👇",
        reply_markup=plans_keyboard()
    )


@router.message(Command("products"))
async def products_handler(message: Message):
    await start_handler(message)


# ==============================
# BACK TO PLANS
# ==============================

@router.callback_query(F.data == "back_to_plans")
async def back_to_plans(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔥 Choose your SmartAdminBot version:\n\n"
        "🚀 Lite — Ready-to-use advertising system\n"
        "🔥 Pro — Advanced automation + scaling tools\n\n"
        "One-time payment. Instant delivery.\n\n"
        "Select your version below:",
        reply_markup=plans_keyboard()
    )


# ==============================
# SELECT PLAN
# ==============================

@router.callback_query(F.data == "select_lite")
async def select_lite(callback: CallbackQuery):
    await callback.message.edit_text(
        "You selected: 🚀 SmartAdminBot Lite – $49\n\n"
        "After payment you will receive:\n"
        "• Full product file\n"
        "• Setup guide\n"
        "• Lifetime updates\n\n"
        "⚡ Instant automated delivery\n\n"
        "Proceed to payment?",
        reply_markup=confirm_keyboard("google")
    )


@router.callback_query(F.data == "select_pro")
async def select_pro(callback: CallbackQuery):
    await callback.message.edit_text(
        "You selected: 🔥 SmartAdminBot Pro – $79\n\n"
        "After payment you will receive:\n"
        "• Full product file\n"
        "• Setup guide\n"
        "• Lifetime updates\n"
        "• Advanced automation modules\n\n"
        "⚡ Instant automated delivery\n\n"
        "Proceed to payment?",
        reply_markup=confirm_keyboard("meta")
    )
