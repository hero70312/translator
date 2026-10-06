import asyncio
import logging
import os
import re

import deepl
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

CHINESE_CHARACTERS = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
MAX_MESSAGE_LENGTH = 4000


def split_message(text: str) -> list[str]:
    return [text[index : index + MAX_MESSAGE_LENGTH] for index in range(0, len(text), MAX_MESSAGE_LENGTH)]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "你好！直接傳送文字即可翻譯。\n"
        "中文會翻成印尼文，印尼文會翻成繁體中文。"
    )


async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None or not message.text:
        return

    text = message.text.strip()
    if not text:
        return

    if CHINESE_CHARACTERS.search(text):
        source_lang, target_lang = "ZH", "ID"
    else:
        source_lang, target_lang = "ID", "ZH-HANT"

    translator: deepl.Translator = context.application.bot_data["translator"]
    try:
        result = await asyncio.to_thread(
            translator.translate_text,
            text,
            source_lang=source_lang,
            target_lang=target_lang,
        )
    except deepl.DeepLException:
        logger.exception("Translation request failed")
        await message.reply_text("翻譯服務暫時無法使用，請稍後再試。")
        return

    for part in split_message(result.text):
        await message.reply_text(part)


def main() -> None:
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    deepl_auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not telegram_token or not deepl_auth_key:
        raise SystemExit("請設定 TELEGRAM_BOT_TOKEN 和 DEEPL_AUTH_KEY。")

    application = Application.builder().token(telegram_token).build()
    application.bot_data["translator"] = deepl.Translator(deepl_auth_key)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))
    application.run_polling()


if __name__ == "__main__":
    main()