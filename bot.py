import threading
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8051897019:AAGoKF_s5t3AWuWn6XtZXzGB0vPnjohyTRM"

# Веб-сервер-заглушка
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running')

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    httpd = HTTPServer(("0.0.0.0", port), DummyServer)
    httpd.serve_forever()

# Главное меню
main_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Офф. сайт ПДР", url="https://рф-поиск.рф/")],
    [InlineKeyboardButton("Поисковые отряды Тюмени", callback_data="category_tymen")],
    [InlineKeyboardButton("Полезные материалы", callback_data="category_materials")]
])

WELCOME_TEXT = (
    "Поисковое движение России — общероссийское общественное поисковое движение, цель которого — "
    "увековечить память погибших при защите Отечества. Движение создано в апреле 2013 года и работает в 84 субъектах "
    "Российской Федерации, объединяя 1500 поисковых отрядов страны. Организуются экспедиции в места боёв Великой "
    "Отечественной войны, массовых захоронений мирных жителей. Они также помогают людям в поиске их погибших или "
    "пропавших без вести близких, ведут работу в архивах для установления личностей найденных на полях сражений.\n\n"
    "Выберите раздел:"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("media/i (1).webp", "rb") as photo:
        if update.message:
            await update.message.reply_photo(
                photo=InputFile(photo),
                caption=WELCOME_TEXT,
                reply_markup=main_keyboard
            )
        else:
            await update.callback_query.message.reply_photo(
                photo=InputFile(photo),
                caption=WELCOME_TEXT,
                reply_markup=main_keyboard
            )

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
        with open("media/i (2).webp", "rb") as photo:
            await query.message.reply_photo(
                photo=InputFile(photo),
                caption=text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

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

# Запуск
threading.Thread(target=run_dummy_server).start()

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.run_polling()
