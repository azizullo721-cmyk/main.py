import telebot

TOKEN = "8736264121:AAEjakFQgi_L18w9b4eBUC9AyJOui_Fq8zM"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "🎮 Salom! O'yin bot ishga tushdi!")

bot.infinity_polling()
