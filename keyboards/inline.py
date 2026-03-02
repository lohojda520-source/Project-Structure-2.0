from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ==============================
# START
# ==============================

def start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 View Plans",
                    callback_data="show_plans"
                )
            ]
        ]
    )


# ==============================
# PLANS
# ==============================

def plans_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 SmartAdminBot Lite – $49",
                    callback_data="buy_lite"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔥 SmartAdminBot Pro – $99",
                    callback_data="buy_pro"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅ Back",
                    callback_data="back_to_start"
                )
            ]
        ]
    )


# ==============================
# CONFIRM
# ==============================

def confirm_keyboard(plan_key: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Proceed to Payment",
                    callback_data=f"confirm_{plan_key}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅ Back",
                    callback_data="show_plans"
                )
            ]
        ]
    )


# ==============================
# PAYMENT
# ==============================

def payment_link_keyboard(payment_url: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Complete Payment",
                    url=payment_url
                )
            ]
        ]
    )
