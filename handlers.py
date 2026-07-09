from email import message
from unittest import result

from pharmacy_service import find_nearby_pharmacies
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from keyboards import (
    main_keyboard,
    location_keyboard,
    favorite_keyboard
)
from database import (
    search_medicine,
    search_medicines,
    search_interaction,
    save_history,
    get_history,
    save_reminder,
    clear_history,
    add_favorite,
    get_favorites,
    remove_favorite
)

router = Router()

#Drug Interactions

interaction_users = set()
reminder_users = {}
search_users = set()
search_results = {}
waiting_for_selection = set()
clear_history_users = set()
last_medicine = {}

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
        "✨ Features:\n"
        "🔍 Search Medicine\n"
        "📋 Multiple Search Results\n"
        "💊 Drug Interactions\n"
        "⏰ Medication Reminder\n"
        "📍 Nearby Pharmacies\n"
        "📄 Search History\n"
        "🗑️ Clear History\n"
        "⭐ Favorite Medicines\n\n"
        "👩‍💻 Developed by:\n"
        "Maryam Hadi\n\n"
        "Thank you for using MedIQ 🤍"
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

@router.message(lambda message: message.text == "⭐ Favorite Medicines")
async def show_favorites(message: Message):
    favorites = get_favorites(message.from_user.id)

    if not favorites:
        await message.answer(
            "⭐ No favorite medicines yet."
        )
        return

    text = "⭐ Your Favorite Medicines:\n\n"

    for i, favorite in enumerate(favorites, start=1):
        text += f"{i}. {favorite[0]}\n"

    await message.answer(text)    


@router.message(lambda message: message.text == "🗑️ Clear History")
async def clear_history_handler(message: Message):
    clear_history_users.add(message.from_user.id)

    await message.answer(
        "⚠️ Are you sure you want to clear your search history?\n\n"
        "Type: YES to confirm\n"
        "Type: NO to cancel"
    )

@router.message(
    lambda message:
    message.from_user.id in clear_history_users
    and message.text
    and message.text.upper() == "YES"
)
async def confirm_clear_history(message: Message):
    clear_history_users.remove(message.from_user.id)
    clear_history(message.from_user.id)

    await message.answer(
        "✅ Search history cleared successfully."
    )

@router.message(
    lambda message:
    message.from_user.id in clear_history_users
    and message.text
    and message.text.upper() == "NO"
)
async def cancel_clear_history(message: Message):
    clear_history_users.remove(message.from_user.id)

    await message.answer(
        "❌ Clear history cancelled."
    )
@router.message(lambda message: message.text == "ℹ️ About")
async def about(message: Message):
    await message.answer(
        "🤖 MedIQ\n\n"
        "💊 Smart Medicine Assistant\n\n"
        "✨ Features:\n"
        "🔍 Search Medicine\n"
        "📋 Multiple Search Results\n"
        "💊 Drug Interactions\n"
        "⏰ Medication Reminder\n"
        "📍 Nearby Pharmacies\n"
        "📄 Search History\n"
        "🗑️ Clear History\n"
        "⭐ Favorite Medicines\n\n"
        "👩🏻‍💻 Developed by:\n"
        "Maryam Hadi\n\n"
        "Thank you for using MedIQ 🤍"
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
        "How to use MedIQ:\n\n"

        "🔍 Search Medicine\n"
        "Search by brand name or generic name.\n\n"

        "📋 Multiple Search Results\n"
        "If more than one medicine is found, choose the number of the medicine you want.\n\n"

        "💊 Drug Interactions\n"
        "Check possible interactions between medicines.\n\n"

        "⏰ Medication Reminder\n"
        "Save reminders for your medicines.\n\n"

        "📍 Nearby Pharmacies\n"
        "Find nearby pharmacies using your location.\n\n"

        "📄 Search History\n"
        "View your recent medicine searches.\n\n"

        "🗑️ Clear History\n"
        "Clear your search history after confirming with YES.\n\n"

        "⭐ Favorite Medicines\n"
        "View your saved favorite medicines.\n\n"

        "⭐ Add to Favorites\n"
        "Search for a medicine, then add it to your favorites.\n\n"

        "🗑️ Remove from Favorites\n"
        "Search for a medicine, then remove it from your favorites.\n\n"

        "💡 Tip:\n"
        "You can search using the full medicine name or part of its name."
    )
@router.message(lambda message: message.text == "⭐ Add to Favorites")
async def add_to_favorites(message: Message):
    medicine_name = last_medicine.get(message.from_user.id)

    if not medicine_name:
        await message.answer(
            "❌ Please search for a medicine first."
        )
        return

    add_favorite(
        message.from_user.id,
        medicine_name
    )

    await message.answer(
        f"✅ {medicine_name} added to favorites."
    )


@router.message(lambda message: message.text == "🗑️ Remove from Favorites")
async def remove_from_favorites(message: Message):
    medicine_name = last_medicine.get(message.from_user.id)

    if not medicine_name:
        await message.answer(
            "❌ Please search for a medicine first."
        )
        return

    remove_favorite(
        message.from_user.id,
        medicine_name
    )

    await message.answer(
        f"✅ {medicine_name} removed from favorites."
    ) 

@router.message(lambda message: message.text == "🔙 Main Menu")
async def back_to_main_menu(message: Message):
    await message.answer(
        "🏠Back to Main Menu",
        reply_markup=main_keyboard
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
    "🗑️ Clear History",
    "⭐ Favorite Medicines",
    "⭐ Add to Favorites",
    "🗑️ Remove from Favorites",
    "🔙 Main Menu",
    "ℹ️ About"

    ]

    if message.text in buttons:
        return
    # ==========================
    # Multiple Results Selection
    # ==========================
    if (
        message.from_user.id in waiting_for_selection
        and message.text.isdigit()
    ):
        index = int(message.text) - 1
        results = search_results.get(message.from_user.id, [])

        if index < 0 or index >= len(results):
            await message.answer("❌ Invalid number. Please choose a number from the list.")
            return

        medicine = results[index]
        last_medicine[message.from_user.id] = medicine[0]
        waiting_for_selection.remove(message.from_user.id)
        search_results.pop(message.from_user.id, None)

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
            f"📏 Strength: {medicine[9]}",
            reply_markup=favorite_keyboard
        )
        

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

        if len(results) > 1:
            search_results[message.from_user.id] = results
            waiting_for_selection.add(message.from_user.id)

            text = "🔍 Multiple medicines found:\n\n"

            for i, med in enumerate(results[:10], start=1):
                text += f"{i}. {med[0]}\n"

            text += "\nReply with the medicine number."

            await message.answer(text)
            return

        medicine = results[0]
        last_medicine[message.from_user.id] = medicine[0]
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
        f"📏 Strength: {medicine[9]}",
        reply_markup=favorite_keyboard

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
    
