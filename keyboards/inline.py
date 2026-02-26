from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ==============================
# MAIN SALES KEYBOARD
# ==============================

def main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📘 Google Ads – $49\nPDF Instruction (English Version)",
                    callback_data="buy_google"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📙 Meta Ads – $79\nPDF Instruction (English Version)",
                    callback_data="buy_meta"
                )
            ]
        ]
    )


# ==============================
# PAYMENT CONFIRM KEYBOARD
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
