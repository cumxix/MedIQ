from email import message
from unittest import result

from pharmacy_service import find_nearby_pharmacies
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from keyboards import (
    main_keyboard,
    location_keyboard
)
from database import (
    search_medicine,
    search_medicines,
    search_interaction,
    save_history,
    get_history,
    save_reminder,
    clear_history
)

router = Router()

#Drug Interactions

interaction_users = set()
reminder_users = {}
search_users = set()
search_results = {}


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
    "👋 Welcome to MedIQ",
    reply_markup=main_keyboard
)


@router.message(Command("search"))
async def search_command(message: Message):
    reminder_users.pop(message.from_user.id, None)
    interaction_users.discard(message.from_user.id)
    search_users.add(message.from_user.id)
    await message.answer("🔍 Please enter the medicine name.")


@router.message(Command("about"))
async def about_command(message: Message):
    await message.answer(
    "🤖 MedIQ\n\n"
    "💊 Smart Medicine Assistant\n\n"
    "Developed by:\n"
    "Maryam Hadi\n\n"
    "Thank you for using MedIQ ❤️"
)
    

@router.message(lambda message: message.text == "🔍 Search Medicine")
async def search(message: Message):
    search_users.add(message.from_user.id)
    await message.answer("🔍 Please enter the medicine name.")


@router.message(lambda message: message.text == "💊 Drug Interactions")
async def interactions(message: Message):

    interaction_users.add(message.from_user.id)

    await message.answer(
        "💊 Please enter the medicine name."
    )


@router.message(lambda message: message.text == "⏰ Medication Reminder")
async def reminder(message: Message):

    reminder_users[message.from_user.id] = {}

    await message.answer("💊 Please enter the medicine name.")


@router.message(lambda message: message.text == "📍 Nearby Pharmacies")
async def pharmacies(message: Message):
    await message.answer(
        "📍 Please share your location.",
        reply_markup=location_keyboard
    )


@router.message(lambda message: message.text == "📄 Medicine History")
async def history(message: Message):

    history = get_history(message.from_user.id)

    if not history:
        await message.answer("📄 No search history.")
        return

    text = "📄 Last Searches\n\n"

    for medicine_name, search_time in history:
        text += f"💊 {medicine_name}\n🕒 {search_time}\n\n"

    await message.answer(text)



@router.message(lambda message: message.text == "ℹ️ About")
async def about(message: Message):
    await message.answer(
        "🤖 MedIQ\n\n"
        "💊 Smart Medicine Assistant\n\n"
        "Features:\n"
        "🔍 Search Medicine\n"
        "💊 Drug Interactions\n"
        "⏰ Medication Reminder\n"
        "📍 Nearby Pharmacies\n"
        "📄 Medicine History\n\n"
        "Developed by:\n"
        "Maryam Hadi\n\n"
        "Thank you for using MedIQ ❤️"
    )



@router.message(lambda message: message.location is not None)
async def receive_location(message: Message):

    latitude = message.location.latitude
    longitude = message.location.longitude

    pharmacies = find_nearby_pharmacies(latitude, longitude)

    if not pharmacies:
        await message.answer("❌ No nearby pharmacies found.")
        return

    text = "📍 Nearby Pharmacies\n\n"

    for i, pharmacy in enumerate(pharmacies, start=1):
        text += (
            f"{i}. 💊 {pharmacy['name']}\n"
            f"🗺️ {pharmacy['link']}\n\n"
        )

    await message.answer(text)


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
    "📖 MedIQ Help\n\n"
    "How to use the bot:\n\n"
    "🔍 Search Medicine\n"
    "Search for medicine information.\n\n"
    "💊 Drug Interactions\n"
    "Check medicine interactions.\n\n"
    "⏰ Medication Reminder\n"
    "Set reminders for your medicines.\n\n"
    "📍 Nearby Pharmacies\n"
    "Find nearby pharmacies.\n\n"
    "📄 Medicine History\n"
    "View your previous searches."
)
@router.message()
async def medicine_search(message: Message):

    if message.text and message.text.startswith("/"):
        return

    buttons = [
        "🔍 Search Medicine",
        "💊 Drug Interactions",
        "⏰ Medication Reminder",
        "📍 Nearby Pharmacies",
        "📄 Medicine History",
        "ℹ️ About"
    ]

    if message.text in buttons:
        return

    # ==========================
    # Search Medicine
    # ==========================
    if message.from_user.id in search_users:
        search_users.remove(message.from_user.id)
        results = search_medicines(message.text)

        if len(results) == 0:
            await message.answer("❌ Medicine not found.")
            return

        medicine = results[0]
        save_history(message.from_user.id, medicine[0])

        await message.answer(
            f"💊 Brand: {medicine[0]}\n\n"
            f"🧪 Generic: {medicine[1]}\n\n"
            f"📌 Uses:\n{medicine[2]}\n\n"
            f"💉 Dose:\n{medicine[3]}\n\n"
            f"⚠️ Side Effects:\n{medicine[4]}\n\n"
            f"🔶 Precautions:\n{medicine[5]}\n\n"
            f"🚫 Contraindications:\n{medicine[6]}\n\n"
            f"🔄 Drug Interactions:\n{medicine[7]}\n\n"
            f"💊 Form: {medicine[8]}\n"
            f"📏 Strength: {medicine[9]}"
        )

        return

    # ==========================
    # Medication Reminder
    # ==========================
    if message.from_user.id in reminder_users:

        data = reminder_users[message.from_user.id]

        if "medicine" not in data:
            data["medicine"] = message.text
            await message.answer("⏰ Enter reminder time (HH:MM)\n\nExample: 08:30")
            return

        reminder_time = message.text

        save_reminder(
            message.from_user.id,
            data["medicine"],
            reminder_time
        )

        del reminder_users[message.from_user.id]

        await message.answer(
            f"✅ Reminder saved!\n\n💊 Medicine: {data['medicine']}\n⏰ Time: {reminder_time}"
        )

        return

    # ==========================
    # Drug Interactions
    # ==========================
    if message.from_user.id in interaction_users:

        interaction_users.remove(message.from_user.id)

        result = search_interaction(message.text)

        if result is None:
            await message.answer("❌ Medicine not found.")
            return

        await message.answer(
            f"💊 {result[0]}\n\n"
            f"🔄 Drug Interactions:\n\n{result[1]}"
        )

        return
    
