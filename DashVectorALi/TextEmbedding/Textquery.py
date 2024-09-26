import json
import dashscope
from dashscope import TextEmbedding
from dashvector import Client, Doc
##1.数据的准备我们将从这个数据集中提取title，方便后续进行embedding并构建检索服务
def prepare_data(path, size):
    with open(path, 'r', encoding='utf-8') as f:
        batch_docs = []
        for line in f:
            batch_docs.append(json.loads(line.strip()))
            if len(batch_docs) == size:
                yield batch_docs[:]
                batch_docs.clear()

        if batch_docs:
            yield batch_docs

# 2.通过 DashScope 生成 Embedding 向量
# DashScope灵积模型服务通过标准的API提供了多种模型服务。
# 其中支持文本Embedding的模型中文名为通用文本向量，
# 英文名为text-embedding-v1。我们可以方便的通过DashScope API调用来获得一段输入文本的embedding向量


dashscope.api_key='sk-869a8bd1d9404142893f16c8da8b3202'

def generate_embeddings(text):
    rsp = TextEmbedding.call(model=TextEmbedding.Models.text_embedding_v1,
                             input=text)
    
    embeddings = [record['embedding'] for record in rsp.output['embeddings']]
    return embeddings if isinstance(text, list) else embeddings[0]


# 查看下embedding向量的维数，后面使用 DashVectorALi 检索服务时会用到，目前是1536
print(len(generate_embeddings('hello')))

# 3.通过 DashVectorALi 构建检索：向量入库
# DashVectorALi 向量检索服务上的数据以集合（Collection）为单位存储，写入向量之前，我们首先需要先创建一个集合来管理数据集。
# 创建集合的时候，需要指定向量维度，这里的每一个输入文本经过DashScope上的text_embedding_v1模型产生的向量，维度统一均为1536。



# 初始化 DashVectorALi client
client = Client(
  api_key='sk-6JT6rEZyd3PHF5GIdWVHi1egkmLef43726A0248A511EF94929E3B7F8A78BB',
  endpoint='vrs-cn-k963u8r13000b7.dashvector.cn-shanghai.aliyuncs.com'
)

# 指定集合名称和向量维度
rsp = client.create('sample', 1536)
assert rsp

collection = client.get('sample')
assert collection

batch_size = 10
for docs in list(prepare_data('QBQTC/dataset/train.json', batch_size)):
    # 批量 embedding
    embeddings = generate_embeddings([doc['title'] for doc in docs])

    # 批量写入数据
    rsp = collection.insert(
        [
            Doc(id=str(doc['id']), vector=embedding, fields={"title": doc['title']}) 
            for doc, embedding in zip(docs, embeddings)
        ]
    )
    assert rsp


