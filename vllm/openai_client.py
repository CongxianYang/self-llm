from openai import OpenAI

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "token-abc123"
openai_api_base = "http://localhost:36935/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

def instruct():
    """ instruct 模式
    """
    completion = client.completions.create(
        model="/tmp/mycode/LLaMA-Factory/merge/models/Llama3-8B-Chinese-Chat-qadata",
        prompt="魔镜魔镜，谁是世界上最美丽的人呢？"
    )

    print("Completion result:", completion.choices[0].text)


def chat():
    """ chat 模式
    """
    completion = client.chat.completions.create(
      model="/tmp/mycode/LLaMA-Factory/merge/models/Llama3-8B-Chinese-Chat-qadata",
      messages=[
        {"role": "user", "content": "谁是世界上最美丽的人呢？"}
      ]
    )

    print(completion.choices[0].message)
    
    
if __name__ == "__main__":
    #instruct()
    chat()