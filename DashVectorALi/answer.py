from dashscope import Generation
#构造 Prompt 向LLM(通义千问)提问
# 在通过提问搜索到相关的知识点后，我们就可以将 “提问 + 知识点” 按照特定的模板作为 
# prompt 向LLM发起提问了。在这里我们选用的LLM是通义千问，这是阿里巴巴自主研发的超大规模语言模型，能够在用户自然语言输入的基础上
# 通过自然语言理解和语义分析，理解用户意图。
# 可以通过提供尽可能清晰详细的指令（prompt)，
# 来获取更符合预期的结果。这些能力都可以通过通义千问API来获得,我们这里设计的提问模板格式为：请基于我提供的内容回答问题。内容是{___}，我的问题是{___}
def answer_question(question, context):
    prompt = f'''请基于```内的内容回答问题。"
	```
	{context}
	```
	我的问题是：{question}。
    '''
    
    rsp = Generation.call(model='qwen-turbo', prompt=prompt)
    return rsp.output.text