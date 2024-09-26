from pymilvus import MilvusClient
from embedding import generate_embeddings
from pymilvus import model
from pymilvus.model.hybrid import BGEM3EmbeddingFunction


from pymilvus import (
    AnnSearchRequest,
    WeightedRanker,
)

def dense_search(col, query_dense_embedding, limit=1):
    search_params = {"metric_type": "IP", "params": {}}
    res = col.search(
        [query_dense_embedding],
        anns_field="dense_vector",
        limit=limit,
        output_fields=["text"],
        param=search_params,
    )[0]
    return [hit.get("text") for hit in res]


def sparse_search(col, query_sparse_embedding, limit=1):
    search_params = {
        "metric_type": "IP",
        "params": {},
    }
    res = col.search(
        [query_sparse_embedding],
        anns_field="sparse_vector",
        limit=limit,
        output_fields=["text"],
        param=search_params,
    )[0]
    return [hit.get("text") for hit in res]


def hybrid_search(
    col,
    query_dense_embedding,
    query_sparse_embedding,
    sparse_weight=1.0,
    dense_weight=1.0,
    limit=1,
):
    dense_search_params = {"metric_type": "IP", "params": {}}
    dense_req = AnnSearchRequest(
        query_dense_embedding, "dense_vector", dense_search_params, limit=limit
    )
    sparse_search_params = {"metric_type": "IP", "params": {}}
    sparse_req = AnnSearchRequest(
        query_sparse_embedding, "sparse_vector", sparse_search_params, limit=limit
    )
    rerank = WeightedRanker(sparse_weight, dense_weight)
    res = col.hybrid_search(
        [sparse_req, dense_req], rerank=rerank, limit=limit, output_fields=["text"]
    )[0]
    # context = []
    # for hits in res:
    #         context.append(hits['entity']['text'])
    # return context
    return [hit.get("text") for hit in res]

def search_relevant_news(question):

    client = MilvusClient(uri="http://localhost:19530")
    #embedding_fn = model.DefaultEmbeddingFunction()
    question_vector= generate_embeddings([question])##encode_querise
    search_params = {
        "metric_type": "L2",  # 欧氏距离（L2距离）
        "params": {"nprobe": 10},
    }
    res = client.search(
         collection_name="new_demo",  # target collection
         data=question_vector,  # query vector
         limit=2,  # number of returned entities
         output_fields=["text"],  # specifies fields to be returned

     )
    context=[]
    for hits in res:
         for hit in hits:
             #print(f"text: {hit['entity'].get('text')}")
             context.append(hit['entity']['text'])
    return context
def query_relevant_news(question):

    client = MilvusClient(uri="http://localhost:19530")
    #embedding_fn = model.DefaultEmbeddingFunction()
    # bge_m3_ef = BGEM3EmbeddingFunction(
    #     model_name='BAAI/bge-m3',  # Specify the model name
    #     device='cuda:0',  # Specify the device to use, e.g., 'cpu' or 'cuda:0'
    #     use_fp16=False  # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
    # )
    # question_vector= bge_m3_ef.encode_queries([question])##encode_querise
    res = client.query(
         collection_name="new_demo",  # target collection
         data=question,  # query vectors
         limit=1,  # number of returned entities
         output_fields=["text"],  # specifies fields to be returned

     )
    context=[]
    for hits in res:
            context.append(hits['text'])
    return context
