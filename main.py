from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# ⚠️ Tokeningizni alohida saqlash tavsiya qilinadi
TOKEN = "8142593958:AAFt9U9ayRmzL4iZSo_-1LYgMaPSBMww5Eg"
ADMINS = [6736873215]

# Bot va Dispatcher yaratish
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# Foydalanuvchilar ro'yxati
USERS = set()

# Foydalanuvchi xabar yuborsa, IDni saqlash
@dp.message_handler()
async def save_users(message: types.Message):
    USERS.add(message.from_user.id)

# Admin /broadcast buyrug'i berganda xabar yuborish uchun tayyorlash
@dp.message_handler(commands=['broadcast'], user_id=ADMINS)
async def broadcast_start(message: types.Message):
    await message.answer("📢 Broadcast uchun xabar yuboring:")

# Admin xabarini barcha foydalanuvchilarga yuborish
@dp.message_handler(user_id=ADMINS)
async def broadcast_send(message: types.Message):
    success, failed = 0, 0
    for user_id in USERS:
        try:
            await bot.send_message(user_id, message.text)
            success += 1
        except Exception as e:
            failed += 1
            print(f"Xatolik {user_id} da: {e}")

    await message.answer(f"✅ Yuborildi: {success}\n❌ Xatolik: {failed}")

# Botni ishga tushirish
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)