from telegram import ReplyKeyboardMarkup


start_message_text = "Hello World"


def get_start_command_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[["/main"]], resize_keyboard=True, one_time_keyboard=False
    )
