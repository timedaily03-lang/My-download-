import os
import asyncio
import time
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# GitHub Secrets-ல் இருந்து தகவல்களை எடுக்கிறது
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# பாட் செட்டிங்ஸ்
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

@app.on_message(filters.regex(r'http'))
async def download_video(client, message):
    url = message.text
    status = await message.reply("⏳ **வீடியோ தயார் செய்யப்படுகிறது... கொஞ்சம் காத்திருங்கள்.**")
    
    # தற்காலிக கோப்பு பெயர்
    file_name = f"video_{int(time.time())}.mp4"
    
    try:
        # மேம்படுத்தப்பட்ட டவுன்லோட் செட்டிங்ஸ்
        ydl_opts = {
            'outtmpl': file_name,
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'geo_bypass': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'ignoreerrors': False,
            'addheader': 'Accept-Language: en-US,en;q=0.9',
        }
        
        # cookies.txt இருந்தால் அதைச் சேர்த்துக் கொள்ளும்
        if os.path.exists('cookies.txt'):
            ydl_opts['cookiefile'] = 'cookies.txt'

        # டவுன்லோட் செய்தல்
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # வீடியோவை அனுப்புதல்
        await message.reply_video(file_name, caption="**Unga video ready! ✨**")
        
        # சர்வரில் இருந்து வீடியோவை நீக்குதல்
        if os.path.exists(file_name):
            os.remove(file_name)
            
        await status.delete()
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}") # GitHub logs-ல் பார்க்க உதவும்
        
        if "login required" in error_msg.lower() or "rate-limit" in error_msg.lower():
            await status.edit("❌ **பிளாக் செய்யப்பட்டுள்ளது. இதற்கு 'cookies.txt' கொடுத்தால் மட்டுமே வேலை செய்யும்.**")
        elif "Cloudflare" in error_msg:
            await status.edit("❌ **Cloudflare பாதுகாப்பு இருப்பதால் இந்தத் தளத்தில் டவுன்லோட் செய்ய முடியாது.**")
        else:
            await status.edit(f"❌ **தவறு:** `{error_msg[:100]}`")

print("Bot is starting...")
app.run()
