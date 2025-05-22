import threading
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8051897019:AAGoKF_s5t3AWuWn6XtZXzGB0vPnjohyTRM"

# Главное меню


# Фоновый веб-сервер-заглушка
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running')

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    httpd = HTTPServer(("0.0.0.0", port), DummyServer)
    httpd.serve_forever()



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Офф. сайт ПДР", url="https://рф-поиск.рф/")],
        [InlineKeyboardButton("Поисковые отряды Тюмени", callback_data="category_tymen")],
        [InlineKeyboardButton("Полезные материалы", callback_data="category_materials")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text("Выберите раздел:", reply_markup=reply_markup)
    else:
        await update.callback_query.message.edit_text("Выберите раздел:", reply_markup=reply_markup)

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "category_tymen":
        text = (
            "Здесь указаны Поисковые отряды ТОЛЬКО состоящие в ОПЦ\n\n"
            "(здесь будут указаны находящиеся в самой Тюмени самые популярные, "
            "если вам надо области, то лучше перейти на сайт самого ОПЦ и посмотреть там...)"
        )
        keyboard = [
            [InlineKeyboardButton("ОПЦ", url="https://poisk-tyumen.ru/")],
            [InlineKeyboardButton('ВПО "Кречет"', url="https://vk.com/club9613984?from=groups")],
            [InlineKeyboardButton("Cавояр", url="https://vk.com/savoyar72")],
            [InlineKeyboardButton("Память-Сердца", url="https://vk.com/club17624181")],
            [InlineKeyboardButton("Феникс", url="https://vk.com/public173598260")],
            [InlineKeyboardButton("🔙 Назад в главное меню", callback_data="main_menu")],
        ]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "category_materials":
        keyboard = [
            [InlineKeyboardButton("ВИПЦ", url="https://v-ipc.org/zapros/form/")],
            [InlineKeyboardButton("Память Народа", url="https://pamyat-naroda.ru/")],
            [InlineKeyboardButton("Мемориал", url="https://obd-memorial.ru/html/")],
            [InlineKeyboardButton("Книга Памяти Тюмень", url="https://память.72to.ru/")],
            [InlineKeyboardButton("🔙 Назад в главное меню", callback_data="main_menu")],
        ]
        await query.message.edit_text("Полезные материалы:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "main_menu":
        await start(update, context)

# Запуск заглушки в фоновом потоке
threading.Thread(target=run_dummy_server).start()

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
