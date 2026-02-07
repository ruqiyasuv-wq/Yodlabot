import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

# ====== ENV dan olish ======
TOKEN = os.getenv("TOKEN")
ADMINS = list(map(int, os.getenv("ADMINS").split(",")))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

USERS_FILE = "users.json"

# ====== Foydalanuvchilarni yuklash ======
try:
    with open(USERS_FILE, "r") as f:
        USERS = set(json.load(f))
except FileNotFoundError:
    USERS = set()

# ====== Foydalanuvchi xabar yuborsa, ID saqlash ======
@dp.message_handler()
async def save_users(message: types.Message):
    USERS.add(message.from_user.id)
    with open(USERS_FILE, "w") as f:
        json.dump(list(USERS), f)

# ====== Admin /broadcast ======
@dp.message_handler(commands=['broadcast'], user_id=ADMINS)
async def broadcast_start(message: types.Message):
    await message.reply("📢 Broadcast uchun xabar yuboring (matn, rasm yoki fayl yuborishingiz mumkin):")

# ====== Admin xabarini barcha foydalanuvchilarga yuborish ======
@dp.message_handler(user_id=ADMINS, content_types=types.ContentType.ANY)
async def broadcast_send(message: types.Message):
    success, failed = 0, 0
    for user_id in USERS:
        try:
            if message.text:
                await bot.send_message(user_id, message.text)
            elif message.photo:
                await bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption)
            elif message.document:
                await bot.send_document(user_id, message.document.file_id, caption=message.caption)
            success += 1
        except:
            failed += 1
    await message.reply(f"✅ Yuborildi: {success}\n❌ Xatolik: {failed}")

# ====== Admin /stats ======
@dp.message_handler(commands=['stats'], user_id=ADMINS)
async def stats(message: types.Message):
    await message.reply(f"👥 Foydalanuvchilar soni: {len(USERS)}")

# ====== Webhook setup ======
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 5000))
WEBHOOK_PATH = f"/{TOKEN}/"
WEBHOOK_URL_FULL = f"{WEBHOOK_URL}{WEBHOOK_PATH}"

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL_FULL)
    print(f"Webhook set to {WEBHOOK_URL_FULL}")

async def on_shutdown(dp):
    await bot.delete_webhook()
    print("Webhook deleted")

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )