import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from services.paypal_service import capture_payment
from services.delivery_service import deliver_product
from services.order_service import order_exists, save_order

# 🔥 ДОДАЙ ЦЕ
from handlers.funnel import router as funnel_router
from handlers.products import router as products_router
from handlers.payments import router as payments_router


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in Railway Variables!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 🔥 Funnel ОБОВʼЯЗКОВО перший
dp.include_router(funnel_router)
dp.include_router(products_router)
dp.include_router(payments_router)

PORT = int(os.environ.get("PORT", 8000))


async def success_handler(request):
    order_id = request.query.get("token")

    if not order_id:
        return web.Response(text="Missing order ID")

    if order_exists(order_id):
        return web.Response(text="Order already processed.")

    try:
        # 🔥 ТУТ ТЕЖ БУВ БАГ — НЕ БУЛО await
        data = await capture_payment(order_id)

        if data.get("status") != "COMPLETED":
            return web.Response(text="Payment not completed.")

        capture_data = data["purchase_units"][0]["payments"]["captures"][0]
        custom_id = capture_data["custom_id"]

        telegram_id, product_key = custom_id.split("|")

        save_order(order_id, telegram_id, product_key)

        await deliver_product(bot, int(telegram_id), product_key)

        return web.Response(text="Payment successful. Check your Telegram.")

    except Exception as e:
        print("Payment error:", e)
        return web.Response(text="Error processing payment.")


async def cancel_handler(request):
    return web.Response(text="Payment cancelled.")


async def main():
    app = web.Application()
    app.router.add_get("/success", success_handler)
    app.router.add_get("/cancel", cancel_handler)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    print(f"Server running on port {PORT}")
    print("Bot started...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
