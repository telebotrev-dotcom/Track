import os
import json
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# BOT_TOKEN dihapus dari pembacaan environment agar bisa langsung isi manual
TOKEN = "8028427483:AAFw14rdTJe-pJdg1PqKqENmiz_OROloLI8"  # <-- masukkan token bot Telegram kamu di sini (jangan bagikan ke siapa pun)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👾 *RevTracker Bot*\n\n"
        "/ip [ip] - Track IP\n"
        "/phone [phone] - Track Phone\n"
        "/username [username] - Check Username Social Media",
        parse_mode="Markdown"
    )

async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /ip [ip address]")
        return
    ip = context.args[0]
    req_api = requests.get(f"http://ipwho.is/{ip}")
    ip_data = json.loads(req_api.text)
    if not ip_data['success']:
        await update.message.reply_text("IP not found or invalid.")
        return

    lat = ip_data['latitude']
    lon = ip_data['longitude']
    maps_link = f"https://www.google.com/maps/@{lat},{lon},8z"
    result = (
        f"🌐 *IP Info*\n"
        f"IP: `{ip}`\n"
        f"Country: {ip_data['country']} ({ip_data['country_code']})\n"
        f"Region: {ip_data['region']}\n"
        f"City: {ip_data['city']}\n"
        f"Lat/Lon: {lat}, {lon}\n"
        f"Maps: [View Map]({maps_link})\n"
        f"ISP: {ip_data['connection']['isp']}\n"
        f"ORG: {ip_data['connection']['org']}\n"
        f"ASN: {ip_data['connection']['asn']}"
    )
    await update.message.reply_text(result, parse_mode="Markdown", disable_web_page_preview=True)

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /phone [+62xxx]")
        return
    num = context.args[0]
    parsed_number = phonenumbers.parse(num, "ID")
    region_code = phonenumbers.region_code_for_number(parsed_number)
    jenis_provider = carrier.name_for_number(parsed_number, "en")
    location = geocoder.description_for_number(parsed_number, "id")
    timezone1 = timezone.time_zones_for_number(parsed_number)
    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    result = (
        f"📱 *Phone Info*\n"
        f"Number: `{formatted_number}`\n"
        f"Location: {location}\n"
        f"Region: {region_code}\n"
        f"Provider: {jenis_provider}\n"
        f"Timezone: {', '.join(timezone1)}"
    )
    await update.message.reply_text(result, parse_mode="Markdown")

async def username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /username [username]")
        return
    username = context.args[0]
    social_media = [
        {"url": "https://www.facebook.com/{}", "name": "Facebook"},
        {"url": "https://www.twitter.com/{}", "name": "Twitter"},
        {"url": "https://www.instagram.com/{}", "name": "Instagram"},
        {"url": "https://www.github.com/{}", "name": "GitHub"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
        {"url": "https://www.youtube.com/{}", "name": "Youtube"},
    ]
    results = []
    for site in social_media:
        url = site['url'].format(username)
        response = requests.get(url)
        if response.status_code == 200:
            results.append(f"✅ {site['name']}: {url}")
        else:
            results.append(f"❌ {site['name']}: Not Found")
    await update.message.reply_text("\n".join(results))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ip", ip))
    app.add_handler(CommandHandler("phone", phone))
    app.add_handler(CommandHandler("username", username))
    app.run_polling()
