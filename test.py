TOKEN = "8569608114:AAEjiWyzgJJhznxtO8m0o8c3AKNo0XHZNRI"  # Replace with your own token
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()