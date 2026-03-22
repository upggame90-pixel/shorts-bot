import telebot
from openai import OpenAI

BOT_TOKEN = "8612605172:AAH868OsgYsdWtm8gcf6d2Kw6TWGySVvOMA"
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