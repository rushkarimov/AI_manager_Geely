import sys
import os

from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.chains import LLMChain

from llm.initializationllm import llm
from memory.memory import memory
from rag.create_embeddings import ensemble_retriever
from fewshot.few_shot import  examples

from utils.logger import setup_logger


logger = setup_logger()

def generate_answer_with_faiss(user_query: str) -> str:
    """
    Формирует ответ на пользовательский запрос, используя FAISS и Few-shot примеры
    :param user_query: str - вопрос пользователя;
    :return: str - ответ, сгенерированный моделью.
    """

    # Поиск ближайших 3-х документов с использованием ансамбля ретриверов
    retrieved_results = ensemble_retriever.get_relevant_documents(user_query)
    result_list = [f"Документ №{idx + 1}:\n{doc.page_content}" for idx, doc in enumerate(retrieved_results[:3])]
    result_str = "\n\n".join(result_list)

    # Создаем PromptTemplate для примера
    example_prompt = PromptTemplate(
        input_variables=["question", "answer"],
        template="Вопрос: {question}\nОтвет: {answer}\n"
    )

    # Переменная с историей 5-ти последних вопросов и ответов
    history = "\n".join([msg.content for msg in memory.chat_memory.messages[-10:]])

    # Создаем FewShotPromptTemplate
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=f"""
    Вы полезный и профессиональный менеджер автосалона Geely из России.
    Вы разговариваете только на русском языке.
    Помогайте пользователям с их запросами об автомобилях, доступности и функциях как знающий и дружелюбный менеджер.
    Вы знаете и можете помочь только со следующими автомобилями Geely, имеющимися в наличии:
    - Emgrand
    - Preface
    - Coolray
    - Cityray
    - Atlas
    - Okavango
    - Monjaro
        
    Пожалуйста, убедитесь, что:
    1. Ваши ответы лаконичны и профессиональны.
    2. Предоставляйте только ту информацию, которая имеет отношение к запросу пользователя.
    3. Отвечайте коротко из 5-10 слов.

    В ответ на данный вопрос может помочь следующая информация:
    {result_str}
    
    История диалога:
    {history}

    Примеры:\n""",
    suffix="\nТеперь ваш вопрос: {input}\nОтвет:"
    )

    
    # Используем ансамбль ретриверов в цепочке
    chain = LLMChain(
        prompt=few_shot_prompt,
        llm=llm,
        memory=memory
    )

    # Формируем полный запрос с контекстом и примерами
    prompt = few_shot_prompt.format(input=user_query)

    # Логируем текст prompt
    logger.info(f"Промпт запроса: {prompt}")

    # Генерация ответа
    answer = chain.run(user_query)

    return answer