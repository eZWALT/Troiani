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

Single-layer GQA (17hx1kv) vs Mamba-3 pushed to OOM on A100 40GB:

| Length | GQA fw | M3 fw | GQA bwd | M3 bwd | GQA mem | M3 mem | fw gap | bwd gap |
|---|---|---|---|---|---|---|---|---|
| 512 | 0.2ms | 1.7ms | 0.9ms | 3.8ms | 53MB | 365MB | 0.12x | 0.23x |
| 2048 | 0.5ms | 3.2ms | 1.5ms | 7.5ms | 99MB | 249MB | 0.14x | 0.20x |
| 8192 | 1.3ms | 4.8ms | 4.3ms | 12.0ms | 222MB | 830MB | 0.27x | 0.36x |
| 16384 | 4.2ms | 8.7ms | 16.1ms | 21.2ms | 385MB | 1.6GB | 0.49x | 0.76x |
| **32768** | **16.7ms** | **16.6ms** | **59.5ms** | **41.1ms** | 712MB | 3.1GB | **1.00x** | **1.45x** |
| 65536 | 63.0ms | 32.9ms | 230.1ms | 83.0ms | 1.4GB | 6.2GB | 1.91x | 2.77x |
| 131072 | 253.1ms | OOM | 910.9ms | OOM | 2.7GB | OOM | - | - |

> **Crossover at L≈32k**: Mamba-3's O(L) scaling overtakes FlashAttention's cuDNN-optimized O(L²). At 65k Mamba-3 is **1.9× faster** fwd, **2.8× faster** bwd.
>
> **Memory tradeoff**: Mamba-3 uses 4-5× more memory per layer at long sequences because the SSM state materializes O(L × d_state × d_inner) for backprop. FlashAttention tiles the attention computation, keeping memory low.
>
> **Mamba-3 OOM at 131k** on 40GB (single layer with d_state=128, expand=2). GQA is still alive at 131k using only 2.7GB thanks to flash attention tiling.

---

## Key Takeaways

1. **Attention (MHA/GQA)** is 4-11× faster in tok/s than Mamba-3 at short sequences (512-2048). At these lengths FlashAttention's cuDNN-optimized kernels dominate.

2. **Mamba-3 overtakes attention at L≈32768** due to O(L) vs O(L²) scaling. At 65536, Mamba-3 is **1.9× faster forward** and **2.8× faster backward**.

3. **Mamba-1 is the fastest SSM variant** (1.5× Mamba-3 at target config) — simplest architecture, least kernel overhead. However, Mamba-1 uses `d_state=16` by default vs `d_state=128` in Mamba-2/3 (we benchmarked all at d_state=128 for fair comparison).

4. **Mamba-2 and Mamba-3 are comparable** at long sequences (2048). Mamba-3 has slightly slower forward but comparable backward due to the fused kernel optimizations.

5. **Mamba-2 forward is surprisingly fast at d=2048 L=2048** (1.5ms vs 4.9ms for Mamba-1). This suggests Mamba-2's chunked scan kernel is particularly efficient at larger dimensions.

6. **Mamba-3 memory is highest** — the SSM state materializes O(L × d_state × d_inner) activations, while FlashAttention tiles the computation. Mamba-3 OOMs at 131k tokens on A100 40GB (single layer), GQA still works at 2.7GB.

7. **Tradeoff**: At our target seq_len (2048-8192), GQA is faster and more memory efficient. Mamba-3's value is **quality per param** — fewer Mamba-3 layers can match more attention layers in perplexity, making total training faster despite higher per-layer cost.
