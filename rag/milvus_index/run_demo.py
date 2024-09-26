from answer_prompt import answer_question_prompt
from search import query_relevant_news,hybrid_search,search_relevant_news
from pymilvus.model.hybrid import BGEM3EmbeddingFunction
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
##知识问答
if __name__ == '__main__':
   bge_m3_ef = BGEM3EmbeddingFunction(
        model_name='BAAI/bge-m3',  # Specify the model name
        device='cuda:0',  # Specify the device to use, e.g., 'cpu' or 'cuda:0'
        use_fp16=False  # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
    )
   connections.connect(uri="http://localhost:19530")
   col=Collection(name="new_demo")
##encode_querise
   while True:
      print("\n")
      userinput = input("question: ")
      if userinput.lower() in ["bye", "quit", "exit"]:  # 我们输入bye/quit/exit等均退出客户端
          print("\n BYE BYE!")
          break

      #在八大处公园附近的实兴北街和八大处街交叉口，一辆水泥搅拌车将一骑自行车女孩卷进车轮下,女孩怎么样了？
      #贵阳市区有强烈震感,是真的吗？情况怎么样？
      #两名中国游客在澳大利亚塔斯马尼亚公路上与另一辆汽车发生头对头碰撞，死亡的女子多少岁？
      #２08国道乌兰察布市察哈尔右翼后旗大陆号收费站发生一起交通事故，现场情况怎么样？
      #4月8日晚，东莞市桥头镇北京师范大学东莞石竹附属学校发生了什么事情？
      #3月18日上午8时30分，兴庆区丽景北街发生一起交通事故，是真的吗？
      #丽江束河古镇发生火灾了吗？
      #云南省德宏傣族景颇族自治州盈江县发生了什么？
      #兰州市张掖路的泰生大厦顶部发生火灾了吗？救援情况怎么样？

      question_vector = bge_m3_ef([userinput])
      context = hybrid_search(col,question_vector["dense"],question_vector["sparse"])
      answer_question_prompt(userinput, context)