from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from handlers.products import show_products  # функція з products.py

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await show_products(message)
