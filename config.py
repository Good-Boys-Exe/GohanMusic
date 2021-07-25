from os import getenv
from dotenv import load_dotenv

load_dotenv()
que = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME")
admins = {}
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_USERNAME = getenv("BOT_USERNAME")
ASSISTANT_NAME = getenv("ASSISTANT_NAME")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "GroupMusicRandom")
OWNER = getenv("OWNER", "GB_03101999")
STICKER_ID = getenv("STICKER_ID", "CAACAgUAAxkBAAFF-Bdg-i8JvMgppo9DCVkFV9pPVSprzgACdwIAAsgM0VdqqiQQ6Hdw7CAE")

DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))

COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ . , - ? : ; $ !").split())

SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
