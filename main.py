import os
import asyncio
import time
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# GitHub Secrets மூலம் வரும் தகவல்கள்
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# பாட்டைத் தொடங்குதல்
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

@app.on_message(filters.regex(r'http'))
async def download_video(client, message):
    url = message.text
    status = await message.reply("⏳ **வீடியோ தயார் செய்யப்படுகிறது... கொஞ்சம் காத்திருங்கள்.**")
    
    file_name = f"video_{int(time.time())}.mp4"
    
    try:
        # ffmpeg எரரைத் தவிர்க்க மற்றும் குக்கீஸைப் பயன்படுத்த செட்டிங்ஸ்
        ydl_opts = {
            'outtmpl': file_name,
            # 'best[ext=mp4]' என்பது ffmpeg இல்லாமல் டவுன்லோட் செய்ய உதவும்
            'format': 'best[ext=mp4]/best', 
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'geo_bypass': True,
            # உங்கள் கோப்புகளில் cookies.txt இருந்தால் அதைப் பயன்படுத்தும்
            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'referer': 'https://www.google.com/',
        }
        
        # டவுன்லோட் செய்யும் பகுதி
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # வீடியோவை டெலிகிராமிற்கு அனுப்புதல்
        await message.reply_video(file_name, caption="**Unga video ready! ✨**")
        
        # வேலை முடிந்ததும் வீடியோவை சர்வரிலிருந்து நீக்குதல்
        if os.path.exists(file_name):
            os.remove(file_name)
        await status.delete()
        
    except Exception as e:
        error_msg = str(e)
        # பிளாக் செய்யப்பட்டால் வரும் எரர் மெசேஜ்
        if "403" in error_msg or "blocked" in error_msg.lower():
            await status.edit("❌ **பிளாக் செய்யப்பட்டுள்ளது. இதற்கு 'cookies.txt' கொடுத்தால் மட்டுமே வேலை செய்யும்.**")
        elif "Cloudflare" in error_msg:
            await status.edit("❌ **இந்த இணையதளம் பாதுகாப்பானது (Cloudflare), அதனால் டவுன்லோட் செய்ய முடியவில்லை.**")
        else:
            await status.edit(f"❌ **தவறு:** `{error_msg[:100]}`")

print("Bot is starting...")
app.run()
