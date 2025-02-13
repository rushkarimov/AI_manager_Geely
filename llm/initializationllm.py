import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import re

# Загрузка токена из .env файла
load_dotenv()

# Инициализация переменных с http ссылкой и API ключом
base_url = os.getenv("base_url")
api_key = os.getenv("api_key")

# Инициализация LLM
llm = ChatOpenAI(base_url=base_url, # Введите http ссылку на порт с локально развернутой LLM
                 api_key=api_key # Введите API ключ
                ) 