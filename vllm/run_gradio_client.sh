#!/bin/bash


python gradio_chat_client.py --model-url "http://localhost:8000/v1" \
    --model "/tmp/mycode/LLaMA-Factory/merge/models/Llama3-8B-Chinese-Chat-qadata" \
    --host "127.0.0.1" \
    #--port 8000