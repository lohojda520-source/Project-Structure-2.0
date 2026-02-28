# =====================================================
# SmartAdminBot Lite v1.6
# Main Bot File
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
# GLOBALS
# =====================================================

START_TIME = datetime.now()

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


# =====================================================
# UTILITIES
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
        users = get_all_users()
        users_count = get_users_count()

        if user_id in users:
            await message.answer(
                "━━━━━━━━━━━━━━━━━━\n"
                f"🚀 <b>{PRODUCT_NAME} {VERSION}</b>\n\n"
                f"👥 Users: {users_count}/{LITE_USER_LIMIT}\n"
                "⚡ Status: Active\n"
                "━━━━━━━━━━━━━━━━━━"
                + lite_banner()
            )
            return

        if MODE == "LITE" and users_count >= LITE_USER_LIMIT:
            await message.answer(
                "🚫 <b>User limit reached!</b>\n\n"
                f"Lite version supports only {LITE_USER_LIMIT} users.\n"
                "Upgrade to Pro to remove limits.",
                reply_markup=upgrade_keyboard(),
            )
            return

        add_user(user_id)

        await message.answer(
            "━━━━━━━━━━━━━━━━━━\n"
            f"🚀 <b>{PRODUCT_NAME} {VERSION}</b>\n\n"
            f"👥 Users: {users_count + 1}/{LITE_USER_LIMIT}\n"
            "⚡ Status: Active\n"
            "━━━━━━━━━━━━━━━━━━"
            + lite_banner()
        )

    except Exception as e:
        await message.answer("⚠️ An unexpected error occurred.")
        print("Start error:", e)


# =====================================================
# ABOUT
# =====================================================

@dp.message(Command("about"))
async def about_handler(message: Message):
    await message.answer(
        f"📦 <b>{PRODUCT_NAME}</b>\n"
        f"Version: {VERSION}\n\n"
        "<b>Lite Includes:</b>\n"
        f"• User limit: {LITE_USER_LIMIT}\n"
        "• Admin panel\n"
        "• Statistics\n"
        "• Broadcast system\n\n"
        "<b>Pro Includes:</b>\n"
        "• Unlimited users\n"
        "• Advanced analytics\n"
        "• Auto moderation\n"
        "• User export\n"
        + lite_banner()
    )


# =====================================================
# VERSION
# =====================================================

@dp.message(Command("version"))
async def version_handler(message: Message):
    uptime = datetime.now() - START_TIME

    await message.answer(
        f"🔎 <b>{PRODUCT_NAME}</b>\n"
        f"Version: {VERSION}\n"
        f"Uptime: {uptime}"
        + lite_banner()
    )


# =====================================================
# ADMIN PANEL
# =====================================================

@dp.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Access denied.")
        return

    await message.answer(
        f"🔐 <b>{PRODUCT_NAME} | Admin Panel</b>\n"
        f"Version: {VERSION}\n\n"
        f"Mode: {MODE}\n"
        f"User Limit: {LITE_USER_LIMIT}\n\n"
        "Choose an action:",
        reply_markup=admin_keyboard(),
    )


# =====================================================
# CALLBACKS
# =====================================================

@dp.callback_query(lambda c: c.data == "stats")
async def stats(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    if not ENABLE_STATS:
        await callback.answer("Statistics disabled.", show_alert=True)
        return

    count = get_users_count()
    uptime = datetime.now() - START_TIME

    await callback.message.edit_text(
        f"📊 <b>Statistics</b>\n\n"
        f"Users: {count}/{LITE_USER_LIMIT}\n"
        f"Uptime: {uptime}\n"
        f"Version: {VERSION}"
        + lite_banner(),
        reply_markup=admin_keyboard(),
    )


@dp.callback_query(lambda c: c.data in ["analytics", "automod", "export"])
async def pro_locked(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    await callback.answer("🔒 Available in Pro version only.", show_alert=True)


# =====================================================
# MAIN
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