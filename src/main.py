import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from src.config import TELEGRAM_BOT_TOKEN
from src.application.agents.fraud_agent import FraudShieldAgent

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

agent = FraudShieldAgent()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        " **Identifica tu fraude**\n"
        "_Agente de orientación frente al fraude digital_\n\n"
        "¿Te llegó un mensaje, enlace, audio o llamada que parece sospechosa?\n\n"
        "1. **Pega o cuenta:** Envíame el mensaje, enlace o foto de una captura / código QR de pago.\n"
        "2. **Revisa el resultado:** Te daré el nivel de riesgo (Bajo, Medio o Alto) contrastado con datos abiertos y trazabilidad verificable.\n"
        "3. **Actúa con seguridad:** Te diré qué hacer y dónde denunciar."
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""
    chat_id = update.effective_chat.id
    
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    bot_response = agent.analyze_case(user_text=user_text)
    await update.message.reply_text(bot_response)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    caption = update.message.caption or ""
    
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()
    
    bot_response = agent.analyze_case(user_text=caption, image_bytes=bytes(photo_bytes))
    await update.message.reply_text(bot_response)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print(" Bot 'Identifica tu fraude' iniciado y escuchando...")

    if __name__ == "__main__":
        logger.info("Bot 'Identifica tu fraude' iniciado y escuchando...")   
        # drop_pending_updates=True limpia mensajes en cola acumulados durante caídas de red
         app.run_polling(drop_pending_updates=True, poll_interval=1.0)

if __name__ == "__main__":
    main()