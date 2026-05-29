import logging
import sys
import os

# Avval path ni qo'shish
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram.ext import Application
from config import BOT_TOKEN
from db import init_db
from services.cache_service import load_all_to_cache
from handlers.admin import get_admin_handlers
from handlers.user import get_user_handlers
from handlers.channel import get_channel_handlers

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    init_db()
    load_all_to_cache()
    bot_info = await application.bot.get_me()
    logger.info(f"✅ Bot ishga tushdi: @{bot_info.username}")


def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ BOT_TOKEN topilmadi!")
        sys.exit(1)

    try:
        app = (
            Application.builder()
            .token(BOT_TOKEN)
            .post_init(post_init)
            .build()
        )

        for handler in get_admin_handlers():
            app.add_handler(handler)
        for handler in get_user_handlers():
            app.add_handler(handler)
        for handler in get_channel_handlers():
            app.add_handler(handler)

        logger.info("🎬 Movie Code Bot polling boshlandi...")
        app.run_polling(drop_pending_updates=True)

    except Exception as e:
        logger.error(f"❌ XATO: {type(e).__name__}: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
