from pymilvus import model
import os
import time
from pymilvus.model.hybrid import BGEM3EmbeddingFunction
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
from tqdm import tqdm
##本地知识库的向量化
def prepare_data(path, batch_size=24):
    batch_docs = []
    for file in os.listdir(path):
        with open(path + '/' + file, 'r', encoding='utf-8') as f:
            batch_docs.append(f.read())
            if len(batch_docs) == batch_size:
                yield batch_docs
                batch_docs = []
    if batch_docs:
        yield batch_docs


def generate_embeddings(news):
    embedding_vec = model.DefaultEmbeddingFunction()
    return embedding_vec.encode_documents(news)

def generate_embeddings_BGM3(news):
    bge_m3_ef = BGEM3EmbeddingFunction(  ##支持8192长度的输入文本
        model_name='BAAI/bge-m3',  # Specify the model name
        device='cuda:0',  # Specify the device to use, e.g., 'cpu' or 'cuda:0'
        use_fp16=False  # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
    )
    embedding_vec = bge_m3_ef.encode_documents(news)
    return embedding_vec

use_bge_m3=True

if __name__ == '__main__':
    # 初始化和连接Milvus数据库
    print("***************    start connecting to Milvus   *************")
    connections.connect(uri="http://localhost:19530")
    # Specify the data schema for the new Collection
    fields = [
        # Use auto generated id as primary key
        FieldSchema(
            name="id", dtype=DataType.VARCHAR, is_primary=True, auto_id=True, max_length=100
        ),
        # Store the original text to retrieve based on semantically distance
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=5000),
        # Milvus now supports both sparse and dense vectors,
        # we can store each in a separate field to conduct hybrid search on both vectors
        FieldSchema(name="sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
        FieldSchema(name="dense_vector", dtype=DataType.FLOAT_VECTOR, dim=1024),
    ]
    # 创建集合：指定集合名称和向量维度
    col_name="new_demo"
    if utility.has_collection(col_name):
        Collection(col_name).drop()
    col=Collection(name=col_name, schema=CollectionSchema(fields=fields),consistency_level="Strong")
    assert col

    # To make vector search efficient, we need to create indices for the vector fields
    print("**************     start create index  ****************")
    # 构建索引
    sparse_index = {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "IP"}
    col.create_index("sparse_vector", sparse_index)
    dense_index = {"index_type": "AUTOINDEX", "metric_type": "IP"}
    col.create_index("dense_vector", dense_index)
    col.load()

    print("**************     start create collection data  ****************")
    start_time = time.time();
    print("**************     start link embedding model  ****************")
   ##use bge_m3
    if use_bge_m3:
         bge_m3_ef = BGEM3EmbeddingFunction(  ##支持8192长度的输入文本
         model_name='BAAI/bge-m3',  # Specify the model name
         device='cuda:0',  # Specify the device to use, e.g., 'cpu' or 'cuda:0'
         use_fp16=False  # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
     )
    #lens=0
    # 加载语料和向量编码
    print("**************     start  embedding  ****************")
    for news in tqdm((prepare_data('/tmp/mycode/DashVectorALi/CEC-Corpus/raw corpus/allSourceText')),desc="Creat embedding"):
        # 加载embedding模型This will use a small embedding model "paraphrase-albert-small-v2" (~50MB).
        vectors = bge_m3_ef.encode_documents(news)
        # data=[
        #     {"id":i+lens,"sparse_vecto":vectors["dense"][i],"dense_vector":vectors["sparse"][i],"text":news[i]}
        #     for i in range (len(vectors["dense"]))
        # ]
        data=[
            news,
            vectors["sparse"],
            vectors["dense"],
        ]
        # 写入 milvus 数据库
        col.insert(data=data)
        #lens += len(news)
    end_time = time.time();
