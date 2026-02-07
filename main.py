from aiogram import Bot, Dispatcher, executor, types

# ===== TOKEN =====
TOKEN = "8142593958:AAFt9U9ayRmzL4iZSo_-1LYgMaPSBMww5Eg"

# ===== Bot va Dispatcher =====
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ===== /start buyrug'i =====
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Bot ishlayapti ✅")

# ===== Har qanday xabar =====
@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(f"Siz yozdingiz: {message.text}")

# ===== Ishga tushirish =====
if __name__ == "__main__":
    print("Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)