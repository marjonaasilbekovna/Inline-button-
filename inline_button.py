from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

phones_inf_mapping = {
    "apple_16_pro": "Apple 16 pro",
    "samsung_21_ultra": "Samsung 21 ultra",
    "redmi_13": "Redmi 13",
    "honor_x6a": "Honor x6a",
    "infinix_smatr_8": "Infinix smart 8"
}

menu_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Apple 16 pro", callback_data="apple_16_pro"), 
            InlineKeyboardButton(text="Samsung 21 ultra", callback_data="samsung_21_ultra")
        ],
        [
            InlineKeyboardButton(text="Redmi 13", callback_data="redmi_13"), 
            InlineKeyboardButton(text="Honor x6a", callback_data="honor_x6a")
        ],
        [
            InlineKeyboardButton(text="Infinix smart 8", callback_data="infinix_smatr_8")
        ]
    ]
)
