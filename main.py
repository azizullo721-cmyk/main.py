import telebot
from telebot import types
import json
import os
import random

TOKEN = "8736264121:AAEjakFQgi_L18w9b4eBUC9AyJOui_Fq8zM"

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"

# -------------------- DATA --------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

users = load_data()

def check_user(user):
    uid = str(user.id)
    if uid not in users:
        users[uid] = {
            "name": user.first_name,
            "coin": 100,
            "win": 0,
            "lose": 0,
            "level": 1
        }
        save_data(users)

# -------------------- MENU --------------------
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🎮 O'yinlar", "👤 Profilim")
    markup.row("💰 Pullarim", "🏆 Reyting")
    markup.row("🎁 Bonus", "⚙️ Sozlamalar")
    return markup

# -------------------- START --------------------
@bot.message_handler(commands=['start'])
def start(message):
    check_user(message.from_user)
    bot.send_message(
        message.chat.id,
        f"Assalomu alaykum {message.from_user.first_name} 👋\n"
        f"Botga xush kelibsiz!",
        reply_markup=main_menu()
    )

# -------------------- PROFILE --------------------
@bot.message_handler(func=lambda m: m.text == "👤 Profilim")
def profile(message):
    uid = str(message.from_user.id)
    u = users[uid]

    text = f"""
👤 Profilingiz

🆔 ID: {uid}
📛 Ism: {u['name']}
💰 Coin: {u['coin']}
🏆 G'alaba: {u['win']}
💀 Mag'lubiyat: {u['lose']}
⭐ Level: {u['level']}
"""
    bot.send_message(message.chat.id, text)

# -------------------- COIN --------------------
@bot.message_handler(func=lambda m: m.text == "💰 Pullarim")
def coin(message):
    uid = str(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"💰 Sizning puliingiz: {users[uid]['coin']} coin"
    )

# -------------------- BONUS --------------------
@bot.message_handler(func=lambda m: m.text == "🎁 Bonus")
def bonus(message):
    uid = str(message.from_user.id)
    reward = random.randint(10, 50)
    users[uid]["coin"] += reward
    save_data(users)

    bot.send_message(
        message.chat.id,
        f"🎁 Siz bonus oldingiz!\n+{reward} coin"
    )

# -------------------- RATING --------------------
@bot.message_handler(func=lambda m: m.text == "🏆 Reyting")
def rating(message):
    top = sorted(users.items(), key=lambda x: x[1]["coin"], reverse=True)

    text = "🏆 TOP O'yinchilar:\n\n"
    for i, user in enumerate(top[:10], start=1):
        text += f"{i}. {user[1]['name']} - {user[1]['coin']} coin\n"

    bot.send_message(message.chat.id, text)

# -------------------- GAMES --------------------
@bot.message_handler(func=lambda m: m.text == "🎮 O'yinlar")
def games(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🎲 Omad o'yini", "🔢 Son topish")
    markup.row("✊ Tosh Qaychi Qog'oz")
    markup.row("⬅️ Orqaga")
    bot.send_message(
        message.chat.id,
        "🎮 O'yin tanlang:",
        reply_markup=markup
    )

# -------------------- LUCK GAME --------------------
@bot.message_handler(func=lambda m: m.text == "🎲 Omad o'yini")
def luck(message):
    uid = str(message.from_user.id)
    num = random.randint(1, 10)

    if num >= 7:
        users[uid]["coin"] += 30
        users[uid]["win"] += 1
        result = "🎉 Siz yutdingiz! +30 coin"
    else:
        users[uid]["coin"] -= 10
        users[uid]["lose"] += 1
        result = "😢 Siz yutqazdingiz! -10 coin"

    save_data(users)
    bot.send_message(message.chat.id, result)

# -------------------- BACK --------------------
@bot.message_handler(func=lambda m: m.text == "⬅️ Orqaga")
def back(message):
    bot.send_message(
        message.chat.id,
        "🏠 Asosiy menyu",
        reply_markup=main_menu()
    )

# -------------------- SETTINGS --------------------
@bot.message_handler(func=lambda m: m.text == "⚙️ Sozlamalar")
def settings(message):
    bot.send_message(
        message.chat.id,
        "⚙️ Sozlamalar bo'limi keyinroq qo'shiladi."
    )

# -------------------- ALL OTHER --------------------
@bot.message_handler(func=lambda m: True)
def other(message):
    bot.send_message(
        message.chat.id,
        "❗ Menyudan foydalaning.",
        reply_markup=main_menu()
    )

print("Bot ishga tushdi...")
bot.infinity_polling()
