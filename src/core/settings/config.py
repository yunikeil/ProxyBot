from dotenv import load_dotenv
import os

# Загрузка переменных из .env файла

current_file_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
env_path = os.path.join(root_path, ".env")

load_dotenv(dotenv_path=env_path, override=True)

DEBUG: bool = os.getenv("DEBUG").lower() == "true"
DROP_TABLES: bool = os.getenv("DROP_TABLES").lower() == "true"
ECHO_SQL: bool = os.getenv("ECHO_SQL").lower() == "true"

BOT_VERSION: str = os.getenv("BOT_VERSION")
ADMIN_IDS: list[int] = list(map(int, os.getenv("ADMIN_IDS").strip().split(",")))

TG_LOG_TOKEN: str = os.getenv("TG_LOG_TOKEN")
TG_WARNING_LOG_CHANNEL: str = os.getenv("TG_WARNING_LOG_CHANNEL")
TG_ERROR_LOG_CHANNEL: str = os.getenv("TG_ERROR_LOG_CHANNEL")
