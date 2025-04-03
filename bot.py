import requests
import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, F
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton

# Получаем токен из переменных окружения
TOKEN = "7629991596:AAHkBKWyvz7T2MdaItlQcL90YnOi0Zh11tY"
YOOMONEY_WALLET = "4100118178122985"  # Укажи свой YooMoney кошелек
YOOMONEY_AMOUNT = "500"  # Укажи сумму оплаты

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
CURRENCY = "XTR"

@dp.message()
async def command_start_handler(message: Message):
    # Создаем ссылку на оплату через YooMoney
    yoomoney_payment_link = (
        f"https://yoomoney.ru/quickpay/confirm.xml?receiver={YOOMONEY_WALLET}"
        f"&sum={YOOMONEY_AMOUNT}&quickpay-form=shop&paymentType=AC"
    )

    # Создаем кнопки
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить", url=yoomoney_payment_link)]
    ])
    welcome_text = (
        "Тариф: фулл\n"
        "Стоимость: 500.00 🇷🇺RUB\n"
        "Срок действия: 1 месяц\n\n"
        "Вы получите доступ к следующим ресурсам:\n"
        "• Мой кайф (канал)"
    )

    await message.answer(welcome_text, reply_markup=keyboard)



@dp.callback_query()
async def handle_payment_callback(callback_query):
    if callback_query.data == "pay_stars":
        await bot.send_invoice(
            chat_id=callback_query.from_user.id,
            title="Подписка на 30 дней (30-Day Subscription)",
            description="Оплатить и получить ссылку (Pay and get a link)",
            payload="access_to_private",
            currency="XTR",
            prices=[LabeledPrice(label="XTR", amount=450)]
        )

@dp.pre_checkout_query()
async def pre_checkout_handler(event: PreCheckoutQuery):
    await event.answer(True)

@dp.message()
async def successful_payment(message: Message):
    link = await bot.create_chat_invite_link(-1002291268265, member_limit=1)
    await message.answer(f"Твоя ссылка: (Your link:)\n{link.invite_link}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
