from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔍 Search Medicine"),
            KeyboardButton(text="💊 Drug Interactions"),
        ],
        [
            KeyboardButton(text="⏰ Medication Reminder"),
            KeyboardButton(text="📍 Nearby Pharmacies"),
        ],
        [
            KeyboardButton(text="📄 Medicine History"),
            KeyboardButton(text="🗑️ Clear History"),
        ],
        [
            KeyboardButton(text="⭐ Favorite Medicines"),
        ],
        [
            KeyboardButton(text="ℹ️ About"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose an option..."
)


# ==========================
# Location Keyboard
# ==========================

location_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="📍 Send My Location",
                request_location=True
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# ==========================
# Favorite Keyboard
# ==========================

favorite_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⭐ Add to Favorites"),
            KeyboardButton(text="🗑️ Remove from Favorites"),
        ],
        [
            KeyboardButton(text="🔙 Main Menu"),
        ],
    ],
    resize_keyboard=True
)