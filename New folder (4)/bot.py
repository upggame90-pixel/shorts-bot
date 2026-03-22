import telebot
from openai import OpenAI

BOT_TOKEN = "8113329011:AAHItuhD5exD_GjEBf03RNHvsz-h5EH97O8"
OPENROUTER_API_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = OPENROUTER_API_KEY,
)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, """
Salom! Men Shorts yordamchi botiman ✋

Menga istalgan mavzuni yozing, men sizga:
✅ 45 soniyalik tayyor senariy
✅ Har bir sahna uchun rasm promptlari
✅ Sarlavha va hashtaglar
yozib beraman!
""")

@bot.message_handler(content_types=['text'])
def get_scenario(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        prompt = f"""
        Menga {message.text} mavzusida YouTube Short uchun to'liq senariy yoz.
        40-45 soniyalik, juda qiziqarli, boshlashda kuchli hook bo'lsin.
        Oxirida 3 ta eng yaxshi hashtag va sarlavha ham qo'sh.
        Faqat o'zbek tilida yoz, boshqa hech nima yozma.
        """
        
        javob = client.chat.completions.create(
            model = "google/gemini-2.0-flash-001",
            messages = [
                {"role": "user", "content": prompt}
            ],
        )

        bot.reply_to(message, javob.choices[0].message.content)

    except Exception as e:
        bot.reply_to(message, f"Xato yuz berdi: {str(e)}")


print("✅ Bot ishlayapti!")
bot.infinity_polling()
