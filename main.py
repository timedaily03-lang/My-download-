import os
import asyncio
import time
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# GitHub Secrets
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

@app.on_message(filters.regex(r'http'))
async def download_video(client, message):
    url = message.text
    status = await message.reply("🚀 **Processing... வீடியோவைத் தேடுகிறேன்.**")
    
    file_name = f"video_{int(time.time())}.mp4"
    
    # 403 Forbidden தவிர்க்க பிரத்யேக செட்டிங்ஸ்
    ydl_opts = {
        'outtmpl': file_name,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.youtube.com/',
        'http_headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        await status.edit("📤 **பதிவேற்றம் செய்யப்படுகிறது...**")
        await message.reply_video(file_name, caption="**Unga video ready! ✨**")
        
        if os.path.exists(file_name):
            os.remove(file_name)
        await status.delete()
        
    except Exception as e:
        await status.edit(f"❌ **மன்னிக்கவும்!** மீண்டும் முயற்சிக்கவும் அல்லது புதிய cookies.txt அப்லோட் செய்யவும்.\n\n`{str(e)[:100]}`")

print("Bot is alive...")
app.run()
