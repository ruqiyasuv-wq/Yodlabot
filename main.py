from aiogram import Bot, Dispatcher, executor, types
import re
import os

# ===== TOKEN =====
TOKEN = "8142593958:AAFt9U9ayRmzL4iZSo_-1LYgMaPSBMww5Eg"

# ===== Bot va Dispatcher =====
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ===== Havola tekshirish patternlari =====
INSTAGRAM_PATTERN = r"(https?://(www\.)?instagram\.com/[\w/-]+)"
YOUTUBE_PATTERN = r"(https?://(www\.)?youtube\.com/watch\?v=[\w-]+)"

# ===== /start buyrug'i =====
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Bot ishlayapti ✅\nInstagram yoki YouTube havolasini yuboring")

# ===== Havola tekshirish =====
@dp.message_handler()
async def link_handler(message: types.Message):
    text = message.text

    insta_match = re.search(INSTAGRAM_PATTERN, text)
    yt_match = re.search(YOUTUBE_PATTERN, text)

    if insta_match:
        await message.reply(f"📸 Instagram havolasi qabul qilindi:\n{insta_match.group(0)}")
    elif yt_match:
        await message.reply(f"▶️ YouTube video havolasi qabul qilindi:\n{yt_match.group(0)}")
    else:
        await message.reply("Havola topilmadi. Iltimos, Instagram yoki YouTube havolasi yuboring.")

# ===== Ishga tushirish =====
if __name__ == "__main__":
    print("Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)