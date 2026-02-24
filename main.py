import os
import asyncio
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# GitHub Secrets-ல் இருந்து தகவல்களை எடுக்கிறது
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# செஷன் கோப்பு சிக்கலைத் தவிர்க்க in_memory=True பயன்படுத்தப்படுகிறது
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

@app.on_message(filters.regex(r'http'))
async def download_video(client, message):
    url = message.text
    status = await message.reply("⏳ **வீடியோ தயார் செய்யப்படுகிறது... கொஞ்சம் காத்திருங்கள்.**")
    
    try:
        # டவுன்லோட் செய்வதற்கான மேம்படுத்தப்பட்ட செட்டிங்ஸ்
        ydl_opts = {
            'outtmpl': 'video.mp4',
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'geo_bypass': True,
            # பிரவுசர் போல காட்ட இந்த User-Agent உதவும்
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            # ஒருவேளை நீங்கள் cookies.txt சேர்த்தால் இது வேலை செய்யும்
            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None
        }
        
        # வீடியோவை டவுன்லோட் செய்கிறது
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # டெலிகிராமிற்கு வீடியோவை அனுப்புகிறது
        await message.reply_video("video.mp4", caption="**Unga video ready! ✨**")
        
        # அனுப்பிய பிறகு சர்வரில் இருந்து வீடியோவை நீக்குகிறது
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")
            
        await status.delete()
        
    except Exception as e:
        # எரர் வந்தால் அதைத் தெரிவிக்கும்
        error_msg = str(e)
        if "Sign in to confirm you're not a bot" in error_msg:
            await status.edit("❌ **YouTube பிளாக் செய்துவிட்டது. இதற்கு 'cookies.txt' கட்டாயம் தேவை.**")
        elif "Cloudflare" in error_msg:
            await status.edit("❌ **இந்த இணையதளம் பாதுகாப்பானது (Cloudflare), அதனால் டவுன்லோட் செய்ய முடியவில்லை.**")
        else:
            await status.edit(f"❌ **தவறு நடந்துள்ளது:** `{error_msg[:100]}`")

print("Bot is starting...")
app.run()
