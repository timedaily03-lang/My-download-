import os
import asyncio
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# GitHub Secrets-லிருந்து விபரங்களை எடுக்கிறது
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# பழைய செஷன் கோப்பு பிரச்சனையைத் தவிர்க்க "new_bot_session" எனப் பெயர் மாற்றியுள்ளேன்
app = Client("new_bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.regex(r'http'))
async def download_video(client, message):
    url = message.text
    status_msg = await message.reply("⚡ Processing... Video download aagittu irukku!")
    
    try:
        ydl_opts = {
            'outtmpl': 'video.mp4',
            'format': 'best',
            'quiet': True
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        await status_msg.edit("✅ Download complete! Uploading to Telegram...")
        await message.reply_video("video.mp4", caption="Unga video ready! ✨")
        
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit(f"❌ Error: {e}")

print("Bot is starting...")
app.run()
