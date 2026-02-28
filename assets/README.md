# =====================================================
# SmartAdminBot Lite
# Main Application File
# Production Version
# aiogram 3.7+ compatible
# =====================================================

import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import (
    BOT_TOKEN,
    ADMIN_ID,
    UPGRADE_CONTACT,
    PRODUCT_NAME,
    VERSION,
    MODE,
    LITE_USER_LIMIT,
    ENABLE_STATS,
    ENABLE_WATERMARK,
    ENABLE_UPGRADE_BUTTON,
    SHOW_STARTUP_LOG,
)

from database import init_db, add_user, get_users_count, get_all_users
from keyboards import admin_keyboard


# =====================================================
# GLOBAL VARIABLES
# =====================================================

START_TIME = datetime.now()

if BOT_TOKEN == "PASTE_YOUR_BOT_TOKEN_HERE":
    raise ValueError("Please insert your BOT_TOKEN inside config.py")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()


# =====================================================
# UTILITY FUNCTIONS
# =====================================================

def clean_username(username: str) -> str:
    return username.replace("@", "")


def upgrade_keyboard():
    if not ENABLE_UPGRADE_BUTTON:
        return None

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💎 Upgrade to Pro",
                    url=f"https://t.me/{clean_username(UPGRADE_CONTACT)}",
                )
            ]
        ]
    )


def lite_banner():
    if not ENABLE_WATERMARK:
        return ""

    return (
        "\n\n━━━━━━━━━━━━━━\n"
        f"⚡ <b>{PRODUCT_NAME} {VERSION}</b>\n"
        f"💰 Upgrade → @{clean_username(UPGRADE_CONTACT)}"
    )


# =====================================================
# START COMMAND
# =====================================================

@dp.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id

    try:
        users_count = get_users_count()

        users_raw = get_all_users()
        users = [u[0] if isinstance(u, tuple) else u for u in users_raw]

        if user_id in users:
            text = (
                "━━━━━━━━━━━━━━━━━━\n"
                f"🚀 <b>{PRODUCT_NAME} {VERSION}</b>\n\n"
                f"👥 Users: {users_count}/{LITE_USER_LIMIT}\n"
                "⚡ Status: Active\n"
                "━━━━━━━━━━━━━━━━━━"
                + lite_banner()
            )
            await message.answer(text)
            return

        if MODE == "LITE" and users_count >= LITE_USER_LIMIT:
            keyboard = upgrade_keyboard()
            text = (
                "🚫 <b>User limit reached!</b>\n\n"
                f"The Lite version supports only {LITE_USER_LIMIT} users.\n"
                "Upgrade to Pro to remove all limitations."
            )

            if keyboard:
                await message.answer(text, reply_markup=keyboard)
            else:
                await message.answer(text)
            return

        add_user(user_id)

        text = (
            "━━━━━━━━━━━━━━━━━━\n"
            f"🚀 <b>{PRODUCT_NAME} {VERSION}</b>\n\n"
            f"👥 Users: {users_count + 1}/{LITE_USER_LIMIT}\n"
            "⚡ Status: Active\n"
            "━━━━━━━━━━━━━━━━━━"
            + lite_banner()
        )

        await message.answer(text)

    except Exception as e:
        print("Start handler error:", e)
        await message.answer("⚠️ An unexpected error occurred.")


# =====================================================
# ABOUT COMMAND
# =====================================================

@dp.message(Command("about"))
async def about_handler(message: Message):
    text = (
        f"📦 <b>{PRODUCT_NAME}</b>\n"
        f"Version: {VERSION}\n\n"
        "<b>Lite Version Includes:</b>\n"
        f"• User limit: {LITE_USER_LIMIT}\n"
        "• Admin panel\n"
        "• Statistics\n"
        "• Basic controls\n\n"
        "<b>Pro Version Includes:</b>\n"
        "• Unlimited users\n"
        "• Broadcast system\n"
        "• User management\n"
        "• Advanced settings\n"
        + lite_banner()
    )

    await message.answer(text)


# =====================================================
# VERSION COMMAND
# =====================================================

@dp.message(Command("version"))
async def version_handler(message: Message):
    uptime = datetime.now() - START_TIME

    text = (
        f"🔎 <b>{PRODUCT_NAME}</b>\n"
        f"Version: {VERSION}\n"
        f"Uptime: {uptime}"
        + lite_banner()
    )

    await message.answer(text)


# =====================================================
# ADMIN PANEL
# =====================================================

@dp.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Access denied.")
        return

    text = (
        f"🔐 <b>{PRODUCT_NAME} | Admin Panel</b>\n"
        f"Version: {VERSION}\n\n"
        f"Mode: {MODE}\n"
        f"User Limit: {LITE_USER_LIMIT}\n\n"
        "Please choose an action:"
    )

    await message.answer(text, reply_markup=admin_keyboard())


# =====================================================
# CALLBACK HANDLERS
# =====================================================

@dp.callback_query(lambda c: c.data == "stats")
async def stats(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    if not ENABLE_STATS:
        await callback.answer("Statistics are disabled.", show_alert=True)
        return

    count = get_users_count()
    uptime = datetime.now() - START_TIME

    text = (
        f"📊 <b>Statistics</b>\n\n"
        f"Users: {count}/{LITE_USER_LIMIT}\n"
        f"Uptime: {uptime}\n"
        f"Version: {VERSION}"
        + lite_banner()
    )

    await callback.message.edit_text(text, reply_markup=admin_keyboard())


@dp.callback_query(lambda c: c.data in ["broadcast", "users", "settings"])
async def pro_locked_features(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    await callback.answer("🔒 This feature is available in the Pro version only.", show_alert=True)


@dp.callback_query(lambda c: c.data == "close")
async def close_admin(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    await callback.message.delete()


# =====================================================
# MAIN FUNCTION
# =====================================================

async def main():
    try:
        init_db()

        if SHOW_STARTUP_LOG:
            print("=================================")
            print(f"{PRODUCT_NAME} {VERSION}")
            print("Status: RUNNING")
            print("Mode:", MODE)
            print("User Limit:", LITE_USER_LIMIT)
            print("=================================")

        await dp.start_polling(bot)

    except Exception as e:
        print("Startup error:", e)


if __name__ == "__main__":
    asyncio.run(main())