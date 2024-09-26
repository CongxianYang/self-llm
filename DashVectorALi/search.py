from dashvector import Client
from embedding import generate_embeddings
#2.知识点的提取   
#将CEC-Corpus 数据集所有新闻报道写入DashVector服务后，
#可以进行快速的向量检索。实现这个检索，我们同样将提问的问题进行文本向量化后，
#再在DashVector服务中检索最相关的知识点
def search_relevant_news(question):
     #初始化 dashvectory client
    client=Client(
        api_key='sk-6JT6rEZyd3PHF5GIdWVHi1egkmLef43726A0248A511EF94929E3B7F8A78BB',
        endpoint='vrs-cn-k963u8r13000b7.dashvector.cn-shanghai.aliyuncs.com'
     )

     # 获取刚刚存入的集合
    collection = client.get('news_embedings')
    assert collection

    # 向量检索：指定 topk = 1 
    rsp = collection.query(generate_embeddings(question), output_fields=['raw'],
                           topk=1)
    assert rsp
    return rsp.output[0].fields['raw']