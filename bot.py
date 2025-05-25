import telebot
from telebot import types

API_TOKEN = '7266088024:AAHSAaXeZF6PA7AxXxW4_aFsEQNN8ljPdmI'

bot = telebot.TeleBot(API_TOKEN)

user_state = {}

main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add("📘 درسنامه اجتماع", "📗 درسنامه اشتراک")
main_menu.add("📝 تمرین اجتماع", "🧮 تمرین اشتراک")
main_menu.add("📊 آزمون ۵سؤالی", "🔁 شروع دوباره")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_state[message.chat.id] = {}
    bot.send_message(message.chat.id, "سلام! به ربات آموزش مجموعه‌ها خوش اومدی ✨\nیکی از گزینه‌های زیر رو انتخاب کن:", reply_markup=main_menu)

# ---------- درسنامه‌ها ----------
@bot.message_handler(func=lambda message: message.text == "📘 درسنامه اجتماع")
def darsname_etehad(message):
    text = "در ریاضیات، اجتماع دو مجموعه شامل همه‌ی اعضایی است که در حداقل یکی از دو مجموعه وجود دارند.\nمثلاً اگر A = {1,2,3} و B = {3,4,5} باشد، آن‌گاه A ∪ B = {1,2,3,4,5} است."
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.text == "📗 درسنامه اشتراک")
def darsname_eshtarak(message):
    text = "در ریاضیات، اشتراک دو مجموعه شامل اعضایی است که در هر دو مجموعه مشترک هستند.\nمثلاً اگر A = {1,2,3} و B = {3,4,5} باشد، آن‌گاه A ∩ B = {3} است."
    bot.send_message(message.chat.id, text)

# ---------- تمرین‌ها ----------
@bot.message_handler(func=lambda message: message.text == "📝 تمرین اجتماع")
def exercise_etehad(message):
    user_state[message.chat.id] = {"mode": "etehad_ex", "step": 1}
    bot.send_message(message.chat.id, "اگر A = {1, 2} و B = {2, 3} باشد، اجتماع A و B چیست؟")

@bot.message_handler(func=lambda message: message.text == "🧮 تمرین اشتراک")
def exercise_eshtarak(message):
    user_state[message.chat.id] = {"mode": "eshtarak_ex", "step": 1}
    bot.send_message(message.chat.id, "اگر A = {2, 4, 6} و B = {1, 2, 3} باشد، اشتراک A و B چیست؟")

# ---------- آزمون ----------
@bot.message_handler(func=lambda message: message.text == "📊 آزمون ۵سؤالی")
def start_quiz(message):
    user_state[message.chat.id] = {
        "mode": "quiz",
        "quiz_step": 1,
        "score": 0
    }
    bot.send_message(message.chat.id, "آزمون شروع شد! سوال ۱:\nاگر A = {1,2} و B = {2,3} باشد، A ∪ B چیست؟")

# ---------- پاسخ‌دهی ----------
@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    state = user_state.get(message.chat.id, {})
    if state.get("mode") == "etehad_ex":
        if state["step"] == 1:
            if message.text == "{1, 2, 3}":
                bot.send_message(message.chat.id, "✅ درست گفتی!")
            else:
                bot.send_message(message.chat.id, "❌ پاسخ نادرست. جواب درست: {1, 2, 3}")
            user_state[message.chat.id] = {}
    elif state.get("mode") == "eshtarak_ex":
        if state["step"] == 1:
            if message.text == "{2}":
                bot.send_message(message.chat.id, "✅ عالیه!")
            else:
                bot.send_message(message.chat.id, "❌ نه، جواب صحیح: {2}")
            user_state[message.chat.id] = {}
    elif state.get("mode") == "quiz":
        step = state["quiz_step"]
        score = state["score"]
        answers = {
            1: "{1, 2, 3}",
            2: "{3}",
            3: "{1,2,3,4}",
            4: "{2,4}",
            5: "{1,3}"
        }
        if message.text == answers[step]:
            score += 1
            bot.send_message(message.chat.id, "✅ درست بود!")
        else:
            bot.send_message(message.chat.id, f"❌ نه! جواب درست: {answers[step]}")

        if step < 5:
            user_state[message.chat.id] = {"mode": "quiz", "quiz_step": step+1, "score": score}
            next_questions = {
                2: "سؤال ۲:\nاگر A = {1,2,3} و B = {3,4} باشد، A ∩ B چیست؟",
                3: "سؤال ۳:\nاگر A = {1,2} و B = {2,3,4} باشد، A ∪ B چیست؟",
                4: "سؤال ۴:\nاگر A = {2,4,6} و B = {1,2,4} باشد، A ∩ B چیست؟",
                5: "سؤال ۵:\nاگر A = {1,3} و B = {1,3} باشد، A ∪ B چیست؟"
            }
            bot.send_message(message.chat.id, next_questions[step+1])
        else:
            bot.send_message(message.chat.id, f"✅ آزمون تمام شد! امتیاز شما: {score}/5")
            user_state[message.chat.id] = {}
    elif message.text == "🔁 شروع دوباره":
        send_welcome(message)
    else:
        bot.send_message(message.chat.id, "لطفاً یکی از گزینه‌ها رو از منو انتخاب کن.")

bot.infinity_polling()
