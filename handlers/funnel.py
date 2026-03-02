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
        [InlineKeyboardButton(text="⬅ Back", callback_data="back_to_plans")]
    ])


# ==============================
# START (IDEAL SALES TEXT)
# ==============================

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "🚀 Welcome to SmartAdminBot\n\n"
        "Turn Telegram into a fully automated sales machine.\n\n"
        "✔ Capture leads automatically\n"
        "✔ Reply instantly 24/7\n"
        "✔ Close sales on autopilot\n"
        "✔ Works in any niche\n\n"
        "Already sold to 38+ users this month 🚀\n\n"
        "• One-time payment\n"
        "• Instant delivery\n"
        "• Lifetime access\n"
        "• No monthly fees\n\n"
        "Choose your plan below 👇\n"
        "⚡ Early pricing may increase soon",
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
        "🚀 Welcome to SmartAdminBot\n\n"
        "Turn Telegram into a fully automated sales machine.\n\n"
        "✔ Capture leads automatically\n"
        "✔ Reply instantly 24/7\n"
        "✔ Close sales on autopilot\n"
        "✔ Works in any niche\n\n"
        "Already sold to 38+ users this month 🚀\n\n"
        "• One-time payment\n"
        "• Instant delivery\n"
        "• Lifetime access\n"
        "• No monthly fees\n\n"
        "Choose your plan below 👇\n"
        "⚡ Early pricing may increase soon",
        reply_markup=plans_keyboard()
    )


# ==============================
# SELECT PLAN
# ==============================

@router.callback_query(F.data == "buy_google")
async def choose_lite(callback: CallbackQuery):
    await callback.message.edit_text(
        "You selected: 🚀 SmartAdminBot Lite – $49\n\n"
        "Includes:\n"
        "• Ready-to-use system\n"
        "• Setup instructions\n"
        "• Lifetime access\n\n"
        "Proceed to payment?",
        reply_markup=confirm_keyboard("google")
    )


@router.callback_query(F.data == "buy_meta")
async def choose_pro(callback: CallbackQuery):
    await callback.message.edit_text(
        "You selected: 🔥 SmartAdminBot Pro – $79 (Best Value)\n\n"
        "Includes:\n"
        "• Advanced automation system\n"
        "• Scaling framework\n"
        "• Priority updates\n"
        "• Lifetime access\n\n"
        "Proceed to payment?",
        reply_markup=confirm_keyboard("meta")
    )
