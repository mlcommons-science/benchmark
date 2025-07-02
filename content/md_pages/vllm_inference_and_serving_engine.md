# vLLM Inference and Serving Engine

**Date**: 2023-09-12

**Expiration**: 

**Valid**: yes

**Name**: vLLM Inference and Serving Engine

**URL**: https://github.com/vllm-project/vllm/tree/main/benchmarks

**Domain**: LLM; HPC/inference

**Focus**: High-throughput, memory-efficient inference and serving engine for LLMs

**Keywords**: LLM inference, PagedAttention, CUDA graph, streaming API, quantization

**Description**: vLLM is a fast, high-throughput, memory-efficient inference and serving engine for large language models,  featuring PagedAttention, continuous batching, and support for quantized and pipelined model execution.  Benchmarks compare it to TensorRT-LLM, SGLang, and others. :contentReference oaicite:1 {index=1} 

**Task Types**: Inference Benchmarking

**AI Capability**: Throughput, latency, memory efficiency

**Metrics**: Tokens/sec, Time to First Token  TTFT , Memory footprint

**Models**: LLaMA, Mixtral, FlashAttention-based models

**Notes**: Incubated by LF AI and Data; achieves up to 24× throughput over HuggingFace Transformers :contentReference oaicite:2 {index=2}

**Citation**:

-
  - type: inproceedings
  - id: kwon2023efficient
  - year: 2023
  - booktitle: SOSP 2023
  - author: Woosuk Kwon, others
  - title: Efficient Memory Management for Large Language Model Serving with PagedAttention
  - bibtex: |
      @inproceedings{kwon2023efficient,
        title={Efficient Memory Management for Large Language Model Serving with PagedAttention},
        author={Woosuk Kwon and others},
        booktitle={SOSP 2023},
        year={2023}
      }

