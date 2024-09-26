# ref:
# https://llamahub.ai/l/readers/llama-index-readers-file?from=

import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.readers.file import PDFReader

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.milvus import MilvusVectorStore
#模型导出器  可以使用功能将模型导出为 OpenVINO IR 格式，并从本地文件夹加载模型
#from llama_index.embeddings.huggingface_openvino import OpenVINOEmbedding



#load pdf
# parser = PDFReader()
# file_extractor = {".pdf": parser}
# documents = SimpleDirectoryReader(
#    "/tmp/mycode/rag/pdf", file_extractor=file_extractor
# ).load_data()
    


##1. emb
Settings.embed_model = OllamaEmbedding(model_name="qwen2")
# ollama_embedding=Settings.embed_model
# pass_embedding = ollama_embedding.get_text_embedding_batch(
#     ["This is a passage!", "This is another passage"], show_progress=True
# )
# print(pass_embedding)
#
# query_embedding = ollama_embedding.get_query_embedding("Where is blue?")
# print(query_embedding)

# ## 2.本地导出模型 为OpenVINO IR 格式，并从本地文件夹加载模型
# OpenVINOEmbedding.create_and_save_openvino_model(
#     "/tmp/models/embedding-models/bge-small-en-v1.5", "./bge_ov"
# )
# #加载导出的模型
# ov_embed_model = OpenVINOEmbedding(folder_name="./bge_ov", device="cpu")
# ##测试
# embeddings = ov_embed_model.get_text_embedding("Hello World!")
# print(len(embeddings))
# print(embeddings[:5])


# llm
Settings.llm = Ollama(model="qwen2", request_timeout=360)

##加载一组文档并从中构建索引
if not os.path.exists("../db/pdf-db"):
    index = VectorStoreIndex.from_documents(
        documents,show_progress=True
    )
    index.storage_context.persist(persist_dir="../db/pdf-db")
    
else:
    storage_context = StorageContext.from_defaults(persist_dir="../db/pdf-db")
    index = load_index_from_storage(storage_context)

#query_engine = index.as_query_olengine()
#query_engine = index.as_query_engine()
#response = query_engine.query("2019年8月14日晚瑞幸咖啡发布上市后首份财报有什么内容？")
# 执行查询并获取响应
# while True:
#     userinput = input("question: ")
#     if userinput.lower() in ["bye", "quit", "exit"]:  # 我们输入bye/quit/exit等均退出客户端
#         print("\n BYE BYE!")
#         break               #2019年8月14日晚瑞幸咖啡发布上市后首份财报有什么内容？
#     question = userinput #'星巴克在金融危机后关闭了大概多少家门店？'"如果我想获得澳洲500签证，TOEFL最少要考多少分？有哪些必要的条件？"
#     response = query_engine.query(question)
#     print(f'answer: {response}')

# #聊天引擎,用于与数据进行对话 （多次来回，而不是一个单一的问答,流式传输响应)
chat_engine = index.as_chat_engine()
while True:
     userinput = input("\nquestion: ")
     if userinput.lower() in ["bye", "quit", "exit"]:  # 我们输入bye/quit/exit等均退出客户端
        print("\n BYE BYE!")
        break               #2019年8月14日晚瑞幸咖啡发布上市后首份财报有什么内容？
     question = userinput #'星巴克在金融危机后关闭了大概多少家门店？'"如果我想获得澳洲500签证，TOEFL最少要考多少分？有哪些必要的条件？"
     streaming_response = chat_engine.stream_chat(question)
     print(f'answer: ')
     for token in streaming_response.response_gen:
         print(token, end="")

     #print(f'answer: {response}')