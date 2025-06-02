import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# توکن ربات (از متغیر محیطی یا به صورت مستقیم)
TOKEN = os.getenv('BOT_TOKEN') or "توکن_ربات_شما"

# ساختار داده‌های آموزشی
CHAPTERS = {
    1: {
        'title': 'مجموعه‌ها و احتمال',
        'lessons': {
            1: {
                'title': 'مفهوم مجموعه',
                'content': '📖 مجموعه به گروهی از اشیا گفته می‌شود که ویژگی مشترکی دارند.\n\nمثال:\n• مجموعه اعداد طبیعی کمتر از ۵: {1,2,3,4}',
                'video': 'https://example.com/set-theory'
            },
            2: {
                'title': 'انواع مجموعه',
                'content': '📖 انواع مجموعه:\n1. مجموعه متناهی (مثل {1,2,3})\n2. مجموعه نامتناهی (مثل اعداد طبیعی)\n3. مجموعه تهی ({} یا ∅)',
                'video': 'https://example.com/set-types'
            }
        },
        'exercises': {
            1: {
                'question': 'کدام گزینه یک مجموعه است؟',
                'options': ['الف) {1,2,3}', 'ب) 1,2,3'],
                'answer': 0
            }
        }
    }
}

# --- توابع مدیریت منو ---
def start(update: Update, context: CallbackContext):
    """شروع ربات و نمایش منوی اصلی"""
    keyboard = [
        [InlineKeyboardButton("📖 درسنامه", callback_data="menu_lessons_1")],
        [InlineKeyboardButton("✏️ تمرین", callback_data="menu_practice_1")],
        [InlineKeyboardButton("📝 آزمون", callback_data="menu_exam_1")]
    ]
    if update.message:
        update.message.reply_text(
            "📚 ربات آموزش ریاضی نهم\n\nفصل ۱: مجموعه‌ها و احتمال\nلطفاً بخش مورد نظر را انتخاب کنید:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        update.callback_query.edit_message_text(
            "📚 ربات آموزش ریاضی نهم\n\nفصل ۱: مجموعه‌ها و احتمال\nلطفاً بخش مورد نظر را انتخاب کنید:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def handle_menu(update: Update, context: CallbackContext):
    """مدیریت کلیک روی منوی اصلی"""
    query = update.callback_query
    query.answer()
    data = query.data.split('_')
    
    if data[1] == 'lessons':
        show_lessons_menu(update, int(data[2]))
    elif data[1] == 'practice':
        start_practice(update, int(data[2]))
    elif data[1] == 'exam':
        start_exam(update, int(data[2]))

def show_lessons_menu(update: Update, chapter: int):
    """نمایش لیست درسنامه‌های یک فصل"""
    query = update.callback_query
    lessons = CHAPTERS[chapter]['lessons']
    keyboard = [
        [InlineKeyboardButton(lessons[i]['title'], callback_data=f"lesson_{chapter}_{i}")]
        for i in lessons
    ]
    keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")])
    
    query.edit_message_text(
        f"📚 درسنامه‌های فصل {chapter}:\n\nلطفاً درس مورد نظر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def show_lesson_content(update: Update, context: CallbackContext):
    """نمایش محتوای یک درس خاص"""
    query = update.callback_query
    query.answer()
    data = query.data.split('_')
    chapter = int(data[1])
    lesson = int(data[2])
    
    lesson_data = CHAPTERS[chapter]['lessons'][lesson]
    
    keyboard = [
        [InlineKeyboardButton("🎥 تماشای ویدیو", url=lesson_data['video'])],
        [InlineKeyboardButton("🔙 برگشت", callback_data=f"menu_lessons_{chapter}")]
    ]
    
    query.edit_message_text(
        f"📖 {lesson_data['title']}\n\n{lesson_data['content']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def start_practice(update: Update, chapter: int):
    """شروع بخش تمرینات"""
    query = update.callback_query
    query.answer()
    exercise = CHAPTERS[chapter]['exercises'][1]  # اولین تمرین
    keyboard = [
        [InlineKeyboardButton(option, callback_data=f"ex_answer_{chapter}_1_{i}")]
        for i, option in enumerate(exercise['options'])
    ]
    keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")])
    
    query.edit_message_text(
        f"✏️ تمرین فصل {chapter}:\n\n{exercise['question']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def handle_exercise_answer(update: Update, context: CallbackContext):
    """پاسخ به سوالات تمرین"""
    query = update.callback_query
    query.answer()
    data = query.data.split('_')
    chapter = int(data[2])
    exercise_num = int(data[3])
    selected_option = int(data[4])
    
    exercise = CHAPTERS[chapter]['exercises'][exercise_num]
    if selected_option == exercise['answer']:
        feedback = "✅ پاسخ صحیح!"
    else:
        feedback = "❌ پاسخ نادرست!"
    
    keyboard = [[InlineKeyboardButton("🔙 برگشت", callback_data=f"menu_practice_{chapter}")]]
    query.edit_message_text(
        f"{feedback}\n\n✏️ تمرین فصل {chapter}:\n\n{exercise['question']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- تنظیمات اصلی ربات ---
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    # دستورات
    dp.add_handler(CommandHandler("start", start))
    
    # مدیریت callback‌ها
    dp.add_handler(CallbackQueryHandler(handle_menu, pattern="^menu_"))
    dp.add_handler(CallbackQueryHandler(show_lesson_content, pattern="^lesson_"))
    dp.add_handler(CallbackQueryHandler(start_practice, pattern="^menu_practice_"))
    dp.add_handler(CallbackQueryHandler(handle_exercise_answer, pattern="^ex_answer_"))
    dp.add_handler(CallbackQueryHandler(start, pattern="^back_to_main"))
    
    updater.start_polling()
    logger.info("ربات شروع به کار کرد...")
    updater.idle()

if __name__ == "__main__":
    main()
