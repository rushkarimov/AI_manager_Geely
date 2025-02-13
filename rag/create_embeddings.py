from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.tools.retriever import create_retriever_tool

from rag.load_table import documents


# Загрузка модели для векторизации текста из HuggingFace
embeddings_model = HuggingFaceEmbeddings(model_name="cointegrated/LaBSE-en-ru")

# Создание эмбендингов с помощью FAISS
db_embed = FAISS.from_documents(documents, embeddings_model)

# Создание ретривера
retriever = db_embed.as_retriever(search_type="similarity",  # тип поиска похожих документов
                                  k=5,  # количество возвращаемых документов (Default: 4)
                                  score_threshold=None,  # минимальный порог для поиска "similarity_score_threshold"
                                 )


# Загрузка документов в BM25 (сами документы, не эмбеддинги)
bm25 = BM25Retriever.from_documents(documents)

# Указание количества возвращаемых документов
bm25.k = 5


# Создание ансамбля ретриверов
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25, retriever],  # список ретриверов
    weights=[
        0.4,
        0.6,
    ],  # веса, на которые домножается скор документа от каждого ретривера
)