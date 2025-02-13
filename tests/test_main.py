import sys
import os

# Добавляем корневую папку проекта в путь Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import AsyncMock, MagicMock

# Функция обработки сообщений
from main import handle_message


class TestBot(unittest.IsolatedAsyncioTestCase):
    """
    Тестирование бота для проверки правильности работы функции handle_message
    """
    async def test_handle_message(self) -> None:
        """
        Проверка того, что метод handle_message корректно обрабатывает 
        сообщение и вызывает reply_text.
        """
        # Поддельный объект update
        mock_update = AsyncMock()
        # Поддельный объект update.message
        mock_update.message = AsyncMock()
        # Эмулируем сообщение от пользователя
        mock_update.message.text = "Привет"
        # Подменяем метод ответа
        # Теперь он не отправляет реальное сообщение,
        # а просто записывает вызовы
        mock_update.message.reply_text = AsyncMock()

        # Мокаем контекст
        # Необходим, чтобы handle_message() работал
        # без настоящего бота
        mock_context = MagicMock() 

        try:
            # Тестируем handle_message() с поддельными данными
            await handle_message(mock_update, mock_context)  
        except Exception as e:
            # Если handle_message() сломается, ошибка выведется в консоль
            print(f"Ошибка в handle_message: {e}")
        # Проверяем, был ли вызов reply_text()
        print(f"Было ли вызвано reply_text: {mock_update.message.reply_text.called}")
        # Проверяем, что бот ответил и reply_text() вызвался ровно 1 раз
        mock_update.message.reply_text.assert_called_once()

if __name__ == "__main__":
    unittest.main()