# core/send_message.py

import requests
from config.settings import BOT_TOKEN, CHAT_ID

def send_contact_message(name, email, phone, subject, message, created_at):
    text = (
        f"✉️ *Yangi Kontakt Murojaati!*\n\n"
        f"👤 Ismi: {name}\n"
        f"📧 Email: {email}\n"
        f"📞 Telefon: {phone}\n"
        f"📌 Mavzu: {subject}\n"
        f"📝 Xabar: {message}\n"
        f"📅 Sana: {created_at.strftime('%Y-%m-%d %H:%M')}"
    )
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    )

def send_registration_message(first_name, last_name, email, phone, course_title, created_at):
    text = (
        f"📝 *Yangi Ro'yxatdan O‘tuvchi!*\n\n"
        f"👤 F.I.Sh: {first_name} {last_name}\n"
        f"📧 Email: {email}\n"
        f"📞 Telefon: {phone}\n"
        f"🎓 Kurs: {course_title}\n"
        f"📅 Sana: {created_at.strftime('%Y-%m-%d %H:%M')}"
    )
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    )
