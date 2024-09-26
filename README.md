
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

# vllm部署大模型--快速开始--不需要量化

### 1.使用本地model
```
  your modelpath
```
### 2. 安装vllm
```
pip install vllm 
```

### 3. 使用vllm

3.1 推理测试
```
python infer_test.py
```

3.2 部署服务
```
bash run_vllm_server.sh
```

3.3 调用服务
```
# 1.使用openai风格的客户端调用
python request.py

# 2. 使用gradio客户端
bash run_gradio_client.sh

```


# LLaMA-Factory微调大模型🦕
1.安装项目的依赖包
```bash
pip install -e .
```
2.快速微调，推理，导出模型，以Llama3为例子<br><br>
Tip🌼:不确定的，对于所有“基座”（Base）模型，template 参数可以是 default, alpaca, vicuna 等任意值。<br>
但“对话”（Instruct/Chat）模型请务必使用对应的模板。请务必在训练和推理时采用完全一致的模板。
```bash
llamafactory-cli train examples/train_lora/llama3_lora_sft.yaml
llamafactory-cli chat examples/inference/llama3_lora_sft.yaml
llamafactory-cli export examples/merge_lora/llama3_lora_sft.yaml
```
启动可视化终端微调
```bash
cd LLaMA-Factory
llamafactory-cli webui
```
# llama.cpp量化部署大模型🦕
1.编译CPP文件
基于CUDA
```bash
cd llama.cpp
cmake -B build_cuda -DLLAMA_CUDA=ON

cmake --build build_cuda --config Release -j 12
```

2.转化safetensors模型格式为gguf并量化为Q8_0
```bash
python convert-hf-to-gguf.py  /modelspath/xxx --outfile  /outmodel/modelname-q8_0-v1.gguf --outtype q8_0
```
3.终端运行gguf格式模型
```bash
cd llama.cpp/build_cuda/bin/
./llama-cli -m /modelpath/xxxx.gguf -cnv
```
4.开启服务器
```bash
./llama-server -m our_model.gguf --port 8080

# Basic web UI can be accessed via browser: http://localhost:8080
```
5.连接开启的服务器
```bash
python request.py
```
6.对gguf格式Q8_0模型再量化为Q4_1

```bash
cd llama.cpp/build_cuda/bin
./quantize --allow-requantize /modelspath/xxx-q8_0-v2_1.gguf /outmodelspath/xxx-q4_1-v1.gguf Q4_1
