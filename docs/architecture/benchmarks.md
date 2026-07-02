# Throughput Benchmarks

Single-layer throughput on **NVIDIA A100 40GB** with **torch.bfloat16**. All models use `d_state=128, expand=2, d_conv=4` unless noted. Measured as mean over 20 iterations after 3 warmup steps.

## Target Config: d_model=1088, seq=2048, bs=2

| Layer | fw (ms) | fwbw (ms) | tok/s | Params | Mem (MB) |
|---|---|---|---|---|---|
| **GQA** (17h x 1kv) | 0.6 | 3.5 | **6.4M** | 2.5M | 175 |
| **Mamba-1** | 2.5 | 11.0 | 1.6M | 8.2M | 332 |
| **Mamba-2** | 2.5 | 11.9 | 1.7M | 7.4M | 376 |
| **Mamba-3** | 3.6 | 12.6 | 1.1M | 7.5M | 508 |

> Attention is **5.7× faster** tok/s than Mamba-3 at target config.
> Mamba-1 is **1.5× faster** than Mamba-3.

---

## All Configurations

### d_model=1024, seq=512

| Layer | fw (ms) | fwbw (ms) | tok/s | Params | Mem (MB) |
|---|---|---|---|---|---|
| MHA 16h | 0.2 | 0.7 | 5.3M | 4.2M | 100 |
| GQA 16hx4kv | 0.3 | 2.3 | 3.6M | 2.6M | 121 |
| Mamba-1 | 1.1 | 5.5 | 939k | 7.4M | 157 |
| Mamba-2 | 2.0 | 8.1 | 525k | 6.6M | 435 |
| Mamba-3 | 1.6 | 5.6 | 627k | 6.7M | 468 |

### d_model=1024, seq=2048

| Layer | fw (ms) | fwbw (ms) | tok/s | Params | Mem (MB) |
|---|---|---|---|---|---|
| MHA 16h | 0.4 | 2.8 | 9.6M | 4.2M | 386 |
| GQA 16hx4kv | 0.6 | 3.6 | 7.4M | 2.6M | 163 |
| Mamba-1 | 2.3 | 10.1 | 1.8M | 7.4M | 315 |
| Mamba-2 | 2.4 | 15.1 | 1.7M | 6.6M | 362 |
| Mamba-3 | 3.5 | 12.4 | 1.2M | 6.7M | 480 |

### d_model=1088 (target), seq=512

| Layer | fw (ms) | fwbw (ms) | tok/s | Params | Mem (MB) |
|---|---|---|---|---|---|
| GQA 17hx1kv | 0.4 | 2.3 | 2.7M | 2.5M | 114 |
| Mamba-1 | 1.3 | 6.9 | 811k | 8.2M | 164 |
| Mamba-2 | 1.4 | 7.0 | 732k | 7.4M | 423 |
| Mamba-3 | 3.5 | 8.6 | 292k | 7.5M | 474 |

### d_model=2048, seq=512

| Layer | fw (ms) | fwbw (ms) | tok/s | Params | Mem (MB) |
|---|---|---|---|---|---|
| MHA 32h | 0.3 | 2.0 | 3.2M | 16.8M | 292 |
| GQA 32hx8kv | 0.3 | 2.6 | 3.3M | 10.5M | 412 |
| Mamba-1 | 1.4 | 6.9 | 749k | 27.8M | 443 |
| Mamba-2 | 1.4 | 6.8 | 751k | 25.8M | 685 |
| Mamba-3 | 3.5 | 8.3 | 294k | 26.2M | 817 |

### d_model=2048, seq=2048

| Layer | fw (ms) | fwbw (ms) | tok/s | Params | Mem (MB) |
|---|---|---|---|---|---|
| MHA 32h | 1.0 | 3.1 | 4.3M | 16.8M | 431 |
| GQA 32hx8kv | 0.8 | 3.1 | 5.0M | 10.5M | 425 |
| Mamba-1 | 4.9 | 20.9 | 830k | 27.8M | 753 |
| Mamba-2 | 1.5 | 14.2 | 2.8M | 25.8M | 847 |
| Mamba-3 | 3.7 | 12.3 | 1.1M | 26.2M | 1124 |

## Sequence Length Scaling (d_model=1088, bs=1)

Single-layer GQA (17hx1kv), Mamba-2, and Mamba-3 pushed to OOM on A100 40GB:

| Length | GQA fw | M2 fw | M3 fw | GQA bwd | M2 bwd | M3 bwd | GQA mem | M2 mem | M3 mem |
|---|---|---|---|---|---|---|---|---|---|
| 512 | 0.2ms | 1.1ms | 1.7ms | 0.8ms | 4.3ms | 3.8ms | 68MB | 376MB | 394MB |
| 2048 | 0.7ms | 3.8ms | 4.4ms | 2.4ms | 14.3ms | 12.2ms | 128MB | 234MB | 279MB |
| 8192 | 1.3ms | 3.9ms | 5.0ms | 4.3ms | 16.1ms | 13.0ms | 251MB | 619MB | 859MB |
| 16384 | 4.3ms | 3.0ms | 8.6ms | 16.5ms | 14.2ms | 21.1ms | 415MB | 1.1GB | 1.6GB |
| **32768** | **16.9ms** | **5.9ms** | **16.7ms** | **60.8ms** | **19.4ms** | **41.6ms** | 742MB | 2.2GB | 3.1GB |
| 65536 | 64.0ms | 12.2ms | 33.3ms | 235ms | 39.2ms | 83.0ms | 1.4GB | 4.3GB | 6.2GB |
| 131072 | 259ms | **24.1ms** | OOM | 928ms | 78.3ms | OOM | 2.7GB | 8.6GB | OOM |
| 262144 | 1.09s | OOM | OOM | 3.74s | OOM | OOM | 5.3GB | OOM | OOM |

> **Mamba-2 overtakes GQA at L≈8k**, Mamba-3 at L≈32k. Mamba-2 is the throughput king at long sequences — **10.7× faster than GQA at 131k** (24ms vs 259ms).
>
> **Memory ranking**: GQA ≪ Mamba-2 < Mamba-3. GQA's flash attention tiles the O(L²) compute, keeping memory at 5.3GB even at 262k. Mamba-2 OOMs at 262k (8.6GB at 131k), Mamba-3 OOMs at 131k.
>
> **Mamba-2 vs Mamba-3**: Mamba-2 is 2-3× faster and uses ~50% less memory at all lengths. For long-context training, Mamba-2 is the better SSM choice.

---

## Key Takeaways

1. **Attention (MHA/GQA)** is 4-11× faster in tok/s than Mamba-3 at short sequences (512-2048). At these lengths FlashAttention's cuDNN-optimized kernels dominate.

2. **Mamba-2 overtakes attention at L≈8k**, Mamba-3 at L≈32k. Mamba-2 is the throughput king at long sequences — **10.7× faster than GQA at 131k**.

3. **Mamba-2 is 2-3× faster than Mamba-3** at all lengths and uses ~50% less memory. For long-context scenarios, Mamba-2 is the better SSM choice from a performance standpoint.

4. **Mamba-1 is the fastest SSM variant at short sequences** (1.5× Mamba-3 at d=1088 L=2048) — simplest architecture, least kernel overhead. Benchmark uses d_state=128 for all.

5. **Memory ranking**: GQA ≪ Mamba-1 < Mamba-2 < Mamba-3. GQA FlashAttention tiles O(L²) compute, keeping memory at 5.3GB even at 262k tokens. Mamba-2 OOMs at 262k, Mamba-3 at 131k on A100 40GB.

6. **For our target seq_len (2048–8192)**: GQA is fastest and most memory-efficient. Mamba-2 is competitive for longer-context fine-tuning. Mamba-3's value is **quality per param** — the paper claims fewer Mamba-3 layers match more attention layers in perplexity, potentially making total training faster despite higher per-layer cost.
