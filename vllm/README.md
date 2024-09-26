
# vllm部署工具

### 1.使用本地model


### 2. 安装vllm
```
pip install vllm 
```

### 3. 使用vllm

3.1 推理 
```
python infer_test.py
```

3.2 部署服务
```
bash run_vllm_server.sh
```

3.3 调用服务
```
# 1.使用openai 风格的客户端调用
python request.py

# 2. 使用gradio客户端
bash run_gradio_client.sh

```





