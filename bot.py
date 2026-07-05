import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import router
from reminder_service import reminder_worker

from database import (
    create_history_table,
    create_reminder_table
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)


async def main():
    create_history_table()
    create_reminder_table()

    # تشغيل خدمة التذكيرات
    asyncio.create_task(reminder_worker(bot))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())