import asyncio
from datetime import datetime

from database import (
    get_active_reminders,
    disable_reminder
)


async def reminder_worker(bot):
    while True:

        current_time = datetime.now().strftime("%H:%M")

        reminders = get_active_reminders()

        for reminder in reminders:

            reminder_id = reminder[0]
            user_id = reminder[1]
            medicine_name = reminder[2]
            reminder_time = reminder[3]

            if reminder_time == current_time:

                try:
                    await bot.send_message(
                        user_id,
                        f"⏰ Medication Reminder\n\n"
                        f"💊 Medicine: {medicine_name}\n\n"
                        f"It's time to take your medicine."
                    )

                    disable_reminder(reminder_id)

                except Exception as e:
                    print(e)

        await asyncio.sleep(60)