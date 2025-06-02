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

TOKEN = os.getenv('BOT_TOKEN') or "توکن_ربات_شما"

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
        },
        'exams': {
            1: {
                'title': 'آزمون پایانی فصل',
                'description': 'این آزمون شامل 10 سوال از مباحث فصل می‌باشد'
            }
        }
    }
}

def start(update: Update, context: CallbackContext):
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
    query = update.callback_query
    query.answer()
    data = query.data.split('_')
    
    try:
        if data[1] == 'lessons':
            show_lessons_menu(update, int(data[2]))
        elif data[1] == 'practice':
            start_practice(update, int(data[2]))
        elif data[1] == 'exam':
            start_exam(update, int(data[2]))
    except Exception as e:
        logger.error(f"خطا در handle_menu: {e}")
        query.edit_message_text("⚠️ خطایی رخ داد. لطفاً دوباره امتحان کنید.")

def show_lessons_menu(update: Update, chapter: int):
    query = update.callback_query
    lessons = CHAPTERS[chapter]['lessons']
    keyboard = [
        [InlineKeyboardButton(lessons[i]['title'], callback_data=f"lesson_{chapter}_{i}")]
        for i in lessons
    ]
    keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")])
    
    query.edit_message_text(
        f"📚 درسنامه‌های فصل {chapter}:\n\nلطفاً درس مورد نظر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard))
    )

def show_lesson_content(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data.split('_')
    
    try:
        chapter = int(data[1])
        lesson = int(data[2])
        lesson_data = CHAPTERS[chapter]['lessons'][lesson]
        
        keyboard = [
            [InlineKeyboardButton("🎥 تماشای ویدیو", url=lesson_data['video'])],
            [InlineKeyboardButton("🔙 برگشت", callback_data=f"menu_lessons_{chapter}")]
        ]
        
        query.edit_message_text(
            f"📖 {lesson_data['title']}\n\n{lesson_data['content']}",
            reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as e:
        logger.error(f"خطا در show_lesson_content: {e}")
        query.edit_message_text("⚠️ خطا در نمایش درس. لطفاً دوباره امتحان کنید.")

def start_practice(update: Update, chapter: int):  # اصلاح تایپو (حذف r اضافه)
    query = update.callback_query
    query.answer()
    
    try:
        exercise = CHAPTERS[chapter]['exercises'][1]
        keyboard = [
            [InlineKeyboardButton(option, callback_data=f"ex_answer_{chapter}_1_{i}")]
            for i, option in enumerate(exercise['options'])
        ]
        keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")])
        
        query.edit_message_text(
            f"✏️ تمرین فصل {chapter}:\n\n{exercise['question']}",
            reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as e:
        logger.error(f"خطا در start_practice: {e}")
        query.edit_message_text("⚠️ خطا در نمایش تمرین. لطفاً دوباره امتحان کنید.")

def start_exam(update: Update, chapter: int):  # تابع جدید اضافه شد
    query = update.callback_query
    query.answer()
    
    try:
        exam = CHAPTERS[chapter]['exams'][1]
        keyboard = [
            [InlineKeyboardButton("شروع آزمون", callback_data=f"start_exam_{chapter}_1")],
            [InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")]
        ]
        
        query.edit_message_text(
            f"📝 {exam['title']}\n\n{exam['description']}",
            reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as e:
        logger.error(f"خطا در start_exam: {e}")
        query.edit_message_text("⚠️ خطا در نمایش آزمون. لطفاً دوباره امتحان کنید.")

def handle_exercise_answer(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    try:
        data = query.data.split('_')
        chapter = int(data[2])
        exercise_num = int(data[3])
        selected_option = int(data[4])
        
        exercise = CHAPTERS[chapter]['exercises'][exercise_num]
        feedback = "✅ پاسخ صحیح!" if selected_option == exercise['answer'] else "❌ پاسخ نادرست!"
        
        keyboard = [[InlineKeyboardButton("🔙 برگشت", callback_data=f"menu_practice_{chapter}")]]
        query.edit_message_text(
            f"{feedback}\n\n✏️ تمرین فصل {chapter}:\n\n{exercise['question']}",
            reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as e:
        logger.error(f"خطا در handle_exercise_answer: {e}")
        query.edit_message_text("⚠️ خطا در پردازش پاسخ. لطفاً دوباره امتحان کنید.")

def error_handler(update: Update, context: CallbackContext):
    logger.error(msg="خطا در پردازش دستور:", exc_info=context.error)
    if update and update.effective_message:
        update.effective_message.reply_text("⚠️ خطای سیستمی رخ داد. لطفاً بعداً تلاش کنید.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    dp.add_error_handler(error_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_menu, pattern="^menu_"))
    dp.add_handler(CallbackQueryHandler(show_lesson_content, pattern="^lesson_"))
    dp.add_handler(CallbackQueryHandler(start_practice, pattern="^menu_practice_"))
    dp.add_handler(CallbackQueryHandler(start_exam, pattern="^menu_exam_"))
    dp.add_handler(CallbackQueryHandler(handle_exercise_answer, pattern="^ex_answer_"))
    dp.add_handler(CallbackQueryHandler(start, pattern="^back_to_main"))
    
    updater.start_polling()
    logger.info("✅ ربات با موفقیت شروع به کار کرد...")
    updater.idle()

if __name__ == "__main__":
    main()
