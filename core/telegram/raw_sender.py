import json
from typing import Literal

import httpx

from core.logging.helpers import create_logger


tg_logger = create_logger("telegram")


async def split_message(text: str, max_length: int = 4069):
    if len(text) <= max_length:
        return [text]
    else:
        split_index = text.rfind("\n", 0, max_length)
        if split_index == -1:
            split_index = max_length
        chunk = text[:split_index]
        remaining = text[split_index:]
        if chunk.count("```") % 2 != 0:
            chunk = chunk + "```"
            remaining = "```shell" + remaining

        return [chunk] + await split_message(remaining)


async def send_telegram_message(
    bot_token: str,
    chat_id: int,
    text: str,
    *,
    parse_mode: Literal["MarkdownV2"] = "MarkdownV2",
    need_info_log: bool = False,
    need_error_log: bool = False,
    need_keyboard: bool = True,
):
    target_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    headers = {"Content-Type": "application/json"}

    chunks = await split_message(text)

    for i, chunk in enumerate(chunks):
        inline_keyboard = None
        if (i == len(chunks) - 1) and need_keyboard:
            inline_keyboard = {
                "inline_keyboard": [
                    [{"text": "Нажми меня", "url": "https://example.com"}]
                ]
            }

        data = {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": parse_mode,
            "disable_web_page_preview": False,
            "disable_notification": False,
        }
        if inline_keyboard:
            data["reply_markup"] = inline_keyboard

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    target_url, headers=headers, data=json.dumps(data)
                )
                if (response.status_code == 200) and need_info_log:
                    tg_logger.info(f"Telegram message sent to {chat_id}")
                elif response.status_code != 200 and need_error_log:
                    tg_logger.error(
                        f"Telegram message not sended: {response.status_code}; Response_text:\n{response.text}"
                    )
        except BaseException:
            # Various errors related to the rate limits
            pass
