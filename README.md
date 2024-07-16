# LLaMA-Factory微调🦕
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
# llama.cpp量化部署模型🦕
1.编译CPP文件
基于CUDA
```bash
cd llama.cpp
cmake -B build_cuda -DLLAMA_CUDA=ON
cmake --build build_cuda --config Release -j 12
```

2.转化safetensors模型格式为gguf并量化为Q8_0
```bash
python convert_hf_to_gguf.py  /modelspath/xxx --outfile  /outmodel/modelname-q8_0-v1.gguf --outtype q8_0
```
3.终端运行gguf格式模型
```bash
cd llama.cpp/build_cuda/bin/
./llama-cli -m modelpath/xxxx.gguf -cnv
./llama-cli -m modelpath/xxxx.gguf -p "You are a helpful assistant" -cnv --in-prefix 'User: ' --reverse-prompt 'User:'
```
4.开启服务器
```bash
./llama-server -m our_model.gguf --port 8080

# Basic web UI can be accessed via browser: http://localhost:8080
```
5.用脚本连接服务器
```bash
cd tools
python request1.py
```
6.对gguf格式Q8_0模型再量化为Q4_1

```bash
cd llama.cpp/build_cuda/bin
./quantize --allow-requantize /modelspath/xxx-q8_0-v2_1.gguf /outmodelspath/xxx-q4_1-v1.gguf Q4_1
