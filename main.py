from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# ⚠️ Test token va admin ID
TOKEN = "8142593958:AAFt9U9ayRmzL4iZSo_-1LYgMaPSBMww5Eg"
ADMINS = [6736873215]

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

USERS = set()

# Foydalanuvchi yozsa ID saqlanadi va javob beriladi
@dp.message_handler()
async def save_users(message: types.Message):
    USERS.add(message.from_user.id)
    await message.reply("Salom! Xabaringiz qabul qilindi.")

# Admin /broadcast buyruq
@dp.message_handler(commands=['broadcast'], user_id=ADMINS)
async def broadcast_start(message: types.Message):
    await message.reply("📢 Xabar yuboring:")

# Admin yozgan xabarni barcha foydalanuvchilarga yuborish
@dp.message_handler(user_id=ADMINS)
async def broadcast_send(message: types.Message):
    success, failed = 0, 0
    for user_id in USERS:
        try:
            await bot.send_message(user_id, message.text)
            success += 1
        except:
            failed += 1
    await message.reply(f"✅ Yuborildi: {success}\n❌ Xatolik: {failed}")

if __name__ == "__main__":
    print("Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)