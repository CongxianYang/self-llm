# git clone https://github.com/ggerganov/llama.cpp
# ollama部署--快速开始

### 常用命令
```
ollama run llama3   # 拉取llama3模型并执行
ollama list         # 显示模型列表
ollama rm llama3    # 删除llama3模型
ollama pull         # 拉取ollama线上存在的模型，并不执行

```
### 1.创建使用本地model

1.1 构建 Modelfile 文件
```
FROM PATH_TO_YOUR__GGUF_MODEL

# set the temperature to 1 [higher is more creative, lower is more coherent]
PARAMETER temperature 1

# set the system message
SYSTEM """
You are Mario from Super Mario Bros. Answer as Mario, the assistant, only.
"""
```

1.2 加载模型从 Modelfile 文件
```
  ollama create NAME -f ./Modelfile

# NAME: 在ollama中显示的名称
# ./Modelfile: 绝对或者相对路径
```
## tips: ollama并不支持所有从llama.cpp中导出的模型S
### 2. 启动服务
```
ollama server  
```

### 3. 使用对话模式

3.1 流式调用
```
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?"
}'
```

3.2 非流式调用
```
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

3.3 带上下文调用（多轮对话）
```
curl http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "messages": [
    {
      "role": "user",
      "content": "why is the sky blue?"
    },
    {
      "role": "assistant",
      "content": "due to rayleigh scattering."
    },
    {
      "role": "user",
      "content": "how is that different than mie scattering?"
    }
  ],
  "stream": false
}'

```

