
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
from dotenv import load_dotenv
from agent.agent import generate_answer_with_faiss
import re
from utils.logger import setup_logger
import requests
import json


# Логирование в файл bot.log
logger = setup_logger("bot.log")

# Загрузка токена из .env файла
load_dotenv()

# Инициализация токена telegram бота
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start от пользователя
    :param update: Update - объект обновления
    сдержащий сообщение пользователя;
    :param context: ContextTypes.DEFAULT_TYPE - 
    объект контекста для для управления состоянием бота;
    :return: None
    """
    # Извлечение информации о пользователе, который отправил команду
    user = update.effective_user
    # Логирование информации о пользователе
    logger.info(f"Команда /start от пользователя: {user.first_name} {user.last_name} ({user.id})")
    # Отправка сообщения пользователю в ответ на /start
    await update.message.reply_text(
        f"Здравствуйте, {user.first_name}! Я AI менеджер автосалона Geely. Чем могу помочь?",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик текстовых сообщений от пользователя
    :param update: Update - объект обновления
    сдержащий сообщение пользователя;
    :param context: ContextTypes.DEFAULT_TYPE - 
    объект контекста для для управления состоянием бота;
    :return: None
    """
    user_message = update.message.text
    # Логирование сообщения от пользователя
    logger.info(f"Получено сообщение от пользователя {update.effective_user.id}: {user_message}")
    try:
        # Генерация ответа
        response = generate_answer_with_faiss(user_message)
        
        # Проверяем, что response является строкой
        if isinstance(response, str):
            match = re.search(r"</think>\n\n(.+)", response, re.DOTALL)
            answer = match.group(1) if match else response
            response_text = answer  # Используем ответ напрямую
        else:
            response_text = "Ответ в неизвестном формате."
        # Логирование сообщения отправляемое пользователю
        logger.info(f"Отправляем ответ пользователю: {response_text}")
        # Отправляем ответ пользователю
        await update.message.reply_text(response_text)

    except Exception as e:
        # Логирование ошибки при обработке запроса от пользователя
        logger.error(f"Ошибка при обработке запроса от {update.effective_user.id}: {e}")
        # Обрабатываем ошибки и отправляем сообщение об ошибке
        await update.message.reply_text(f"Произошла ошибка при обработке вашего запроса: {e}")


if __name__ == "__main__":
    
    # Создание экземпляра бота с переданным токеном
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()
    
    # Устанавливаем тайм-аут опроса сервера telegram в 60 секунд
    app.bot.request.timeout = 60

    # Обработка сообщения /start от пользователя
    app.add_handler(CommandHandler("start", start))

    # Обработка текстовых сообщений от пользователя
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    app.run_polling()