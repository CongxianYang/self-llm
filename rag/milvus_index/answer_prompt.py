openai_api_key = "token-abc123"
openai_api_base = "http://localhost:36935/v1"
from openai import  OpenAI

def answer_question_prompt(question, context):
    prompt = f'''请基于```内的内容回答问题。"
	```
	{context}
	```
	我的问题是：{question}。
    '''
    client_llm = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )
    completion = client_llm.chat.completions.create(
        model="/tmp/mycode/LLaMA-Factory/merge/models/Llama3-8B-Chinese-Chat-qadata",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature = 0.7,
        stream=True,
    )
    #ai_message = {"role": "assistant", "content": ""}
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            #ai_message["content"] += chunk.choices[0].delta.content
    #return completion.choices[0].message
