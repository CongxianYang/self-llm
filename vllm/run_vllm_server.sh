#!/bin/bash

python -m vllm.entrypoints.openai.api_server \
    --model /tmp/mycode/LLaMA-Factory/merge/models/Llama3-8B-Chinese-Chat-qadata  \
    --tensor-parallel-size 1 \
    --trust-remote-code \
    --api-key token-abc123 \
    --port  36935



# python -m vllm.entrypoints.openai.api_server \
#     --model /root/autodl-tmp/models/glm-4-9b-chat \
#     --tensor-parallel-size 2 \
#     --max-model-len 32768 \
#     --trust-remote-code