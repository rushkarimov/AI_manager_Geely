import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import unittest
from agent.agent import generate_answer_with_faiss


class TestIntegration(unittest.TestCase):

    def test_faiss_response(self) -> None:
        """
        Проверяем, что FAISS выдает не пустой ответ
        """
        # Вопрос
        query = "Какие есть модели Geely?"
        # Ответ
        response = generate_answer_with_faiss(query)
        # Проверка на str
        self.assertIsInstance(response, str)
        # Проверка, что длина ответа больше 5 символов
        self.assertGreater(len(response), 5)

if __name__ == "__main__":
    unittest.main()