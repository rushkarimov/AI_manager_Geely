import pandas as pd
from langchain.document_loaders import DataFrameLoader


# Загрузка документа в Pandas
doc = pd.read_excel("rag/table/Geely_vetros.xlsx")

# Загрузка DataFrame в loader
loader = DataFrameLoader(doc, page_content_column="Text")
documents = loader.load()