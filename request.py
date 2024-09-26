#连接开启的服务器
from openai import OpenAI

# 注意服务端端口，因为是本地，所以不需要api_key
client = OpenAI(base_url="http://localhost:36935/v1",
                api_key="token-abc123")#EMPTY  not-needed

# 对话历史：设定系统角色是一个只能助理，同时提交“自我介绍”问题
history = [
    {"role": "system", "content": "你是小小羊同学，你是由上海帆扬宇亿科技公司开发设计的，你旨在为用户提供更好的关键词提取。"},
    {"role": "user", "content": "请用中文进行自我介绍，要求不能超过5句话，总字数不超过100个字。"},
]
print("\033[92;1m")

# 首次自我介绍完毕，接下来是等代码我们的提示
while True:
    completion = client.chat.completions.create(
        model="/tmp/mycode/LLaMA-Factory/merge/models/Llama3-8B-Chinese-Chat-qadata",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}

    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)
    print("\033[91;1m")

    userinput = input("> ")
    if userinput.lower() in ["bye", "quit", "exit"]:  # 我们输入bye/quit/exit等均退出客户端
        print("\033[0mBYE BYE!")
        break

    history.append({"role": "user", "content": userinput})
    print("\033[92;1m")
