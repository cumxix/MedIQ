import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from database import (
    get_active_reminders,
    disable_reminder,
    get_user_timezone
)


async def reminder_worker(bot):
    while True:

        reminders = get_active_reminders()

        for reminder in reminders:

            reminder_id = reminder[0]
            user_id = reminder[1]
            medicine_name = reminder[2]
            reminder_time = reminder[3]

            # Get the user's saved time zone
            user_timezone = get_user_timezone(user_id)

            try:
                current_time = datetime.now(
                    ZoneInfo(user_timezone)
                ).strftime("%H:%M")

            except Exception:
                current_time = datetime.now(
                    ZoneInfo("Asia/Baghdad")
                ).strftime("%H:%M")

            if reminder_time == current_time:

                try:
                    await bot.send_message(
                        chat_id=user_id,
                        text=(
                            "⏰ Medication Reminder\n\n"
                            f"💊 Medicine: {medicine_name}\n\n"
                            "It's time to take your medicine."
                        )
                    )

                    disable_reminder(reminder_id)

                except Exception as e:
                    print(f"Reminder error: {e}")

        await asyncio.sleep(10)