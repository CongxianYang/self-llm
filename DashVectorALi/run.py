
import dashscope

from search import search_relevant_news
from answer import answer_question
##知识问答
if __name__ == '__main__':
    dashscope.api_key = 'sk-869a8bd1d9404142893f16c8da8b3202'
while True:
    userinput = input("question: ") 
    if userinput.lower() in ["bye", "quit", "exit"]:  # 我们输入bye/quit/exit等均退出客户端
        print("\n BYE BYE!")
        break
    question = userinput #'云南瑞丽市抗震救灾情况怎么样'
    context = search_relevant_news(question)
    answer = answer_question(question, context)

    print(f'answer: {answer}')
    