from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ContextTypes

from core.database import get_session
from .addons import start_message_text, get_start_command_keyboard


def get_start_command():
    names = ["start"]

    async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            text=start_message_text, reply_markup=get_start_command_keyboard()
        )
        
    return CommandHandler(command=names, callback=command)


handlers = [get_start_command()]