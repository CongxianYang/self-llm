from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding


# 加载数据
documents = SimpleDirectoryReader("/tmp/mycode/rag/docs").load_data()

# Emb
Settings.embed_model = OllamaEmbedding(model_name="qwen2")  

# Post processing
Settings.llm = Ollama(model="qwen2", request_timeout=360)  


index = VectorStoreIndex.from_documents(
    documents
)

query_engine = index.as_query_engine()


# 执行查询并获取响应
response = query_engine.query("霸王茶姬香港店什么时候开业？店长薪酬多少？门店店员培训期间的工资大约多少？")
print(response)  