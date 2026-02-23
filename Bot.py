import os
import asyncio
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# Unga Details
API_ID = 33067910
API_HASH = "9d8f59413d03f6a9239d4af8279641c2"
BOT_TOKEN = "8173807659:AAE4TAD8wKqLI9Gs4VI0S-4z0nYAemho_2s"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.regex(r'http'))
async def download_video(client, message):
    url = message.text
    status_msg = await message.reply("⚡ Processing... Video download aagittu irukku, konjam wait pannunga!")
    
    try:
        # Download settings
        ydl_opts = {
            'outtmpl': 'video.mp4',
            'format': 'best',
            'quiet': True
        }
        
        # Video-ah download pannuthu
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Telegram-kku video anupputhu
        await status_msg.edit("✅ Download complete! Ippo Telegram-kku upload aaguthu...")
        await message.reply_video("video.mp4", caption="Unga video ready! ✨")
        
        # File-ah delete panni space clean pannuthu
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit(f"❌ Error: Link thappa irukalam illa server busy-ah irukalam.\nDetailed Error: {e}")

print("Bot is running... Go to Telegram and send a link!")
app.run()
