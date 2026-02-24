import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# GitHub Secrets
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 'bot_session' என்ற பெயரில் தற்காலிகமாகச் சேமிக்கும்
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

@app.on_message(filters.regex(r'http'))
async def download_video(client, message):
    url = message.text
    status = await message.reply("⏳ Processing your request...")
    
    try:
        ydl_opts = {
            'outtmpl': 'video.mp4',
            'format': 'best',
            'quiet': True,
            'no_warnings': True
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        await message.reply_video("video.mp4", caption="Unga video ready! ✨")
        os.remove("video.mp4")
        await status.delete()
        
    except Exception as e:
        await status.edit(f"❌ Error: {str(e)}")

app.run()
