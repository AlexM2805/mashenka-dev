import telebot
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import time
import threading

# === 1. Токен бота ===
TOKEN = "7773860055:AAFNyJn0qGRsphnIuMrZxCBaO2-ROV0YVbY"
bot = telebot.TeleBot(TOKEN)

# === 2. Подключение к Google Таблице ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Формула Машеньки: Вес, Объёмы, Чудеса").sheet1

# === 3. Обработка сообщений от Машеньки ===
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Привет, Машенька! 🌸 Отправь мне свои данные построчно:\n\nпример:\n79.3\n73\n98\n55")

@bot.message_handler(func=lambda message: True)
def handle_data(message):
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    user_input = message.text.split('\n')
    while len(user_input) < 4:
        user_input.append('')
    sheet.append_row([now] + user_input)
    bot.send_message(message.chat.id, "📝 Записал! Ты умничка, Машенька! 💚")

# === 4. Напоминалки ===
def morning_reminder():
    bot.send_message(7773860055, "☀️ Доброе утро, Машенька! Не забудь взвеситься и записать данные 🧹")

def evening_reminder():
    bot.send_message(7773860055, "🌙 Вечерняя кашка, 15 мин спорта и обнимашки от Нафани! ✨")

def schedule_messages():
    schedule.every().day.at("07:00").do(morning_reminder)
    schedule.every().day.at("21:00").do(evening_reminder)
    while True:
        schedule.run_pending()
        time.sleep(1)

# === 5. Запуск ===
threading.Thread(target=schedule_messages).start()
bot.polling()