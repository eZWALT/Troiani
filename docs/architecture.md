# Troiani v1 Architecture

Troiani v1 is a **Mamba-3-dominant hybrid** with sparse GQA, SwiGLU MLPs, RoPE + YaRN, and tied embeddings. Built to stay under 1B params with room for multimodal adapters.

## Design Rationale

Extensive parameter budgeting across d_model (512-1536), MLP ratios (2.0-4.0), layer counts, and mixing schemes (Mamba/LIV/GQA) led to the following conclusions:

1. **Mamba-3 is the backbone.** Its selective SSM provides input-dependent global mixing in O(L) time - already a superset of what a static long-conv (LIV) offers. Mamba's built-in conv1d (k=4) and d_state=128 cover local and global receptive fields.

2. **LIV long-conv is deferred.** LIV duplicates Mamba's global mixing but without selectivity. It only helps early-layer feature extraction on data with fixed/periodic patterns. Net param cost isn't justified for language at sub-1B scale. Revisit if multimodal data shows strong shift-invariant structure.

3. **GQA every 5-6 layers is the sweet spot** (~17-20% attention). Matches the Jamba design philosophy - enough for sharp content retrieval, Mamba dominates the rest.

4. **SwiGLU with ratio 8/3** (LLaMA-style). The gating-optimized default - preserves the capacity of a 4x FFN at lower param cost.

5. **d_model=1024** - wide enough for multimodal fusion (vision/audio features need the capacity), still deep at 36 layers.

## Target Config: Troiani-base (~806M)

```
d_model:           1024
n_layers:          36  (30 Mamba-3 + 6 GQA)
layer pattern:     [M M M M M A] x 6   (GQA every 6th, 17% attention)
MLP:               SwiGLU, ratio 8/3  (hidden = 2731)
SSM:               Mamba-3 (d_state=128, d_conv=4, expand=2)
Attention:         GQA (8 query heads, 1 KV head)
Positional enc:    RoPE + YaRN (for context extension)
Norm:              RMSNorm
Embeddings:        Tied (input = output LM head)
Vocab:             32,000

Base params:       ~806M
+ multimodal       ~60M  (vision Q-Former + audio adapter + router)
adapters:          ----
Total:             ~866M  (134M headroom under 1B)
```

### Depth Variants

| Layers | Pattern         | Base Params | + Adapters | Notes                     |
|--------|-----------------|-------------|------------|---------------------------|
| 30     | MMMMMA x 5      | 677M        | 737M       | Light, fast, roomy        |
| 36     | MMMMMA x 6      | 806M        | 866M       | Sweet spot (recommended)  |
| 42     | MMMMMA x 7      | 934M        | 994M       | Max depth under 1B        |

## Per-Layer Param Breakdown (d=1024, SwiGLU ratio 8/3)

| Layer type | Params/layer | Role |
|------------|-------------|------|
| Mamba-3    | ~23.6M       | Selective global state-space mixer (dominant) |
| GQA        | ~10.7M       | Sharp content retrieval, KV-cache efficient |
| SwiGLU MLP | ~8.4M        | Feedforward non-linearity |
| RMSNorm    | ~2K          | Per-token normalization |

## Component Table

| Component            | Choice                        | Notes                                                     |
|----------------------|-------------------------------|-----------------------------------------------------------|
| Sequence Mixer       | **Mamba-3**                   | Selective SSM, d_state=128, linear-time long-context.    |
| Attention            | **GQA** (every 6th layer)    | KV-cache efficient; sharp retrieval without quality loss.|
| Feedforward          | **SwiGLU** (ratio 8/3)       | LLaMA-style gated MLP, capacity-efficient.               |
| Positional Encoding  | **RoPE + YaRN**              | Rotary embeddings with YaRN for context extension.        |
| Normalization        | **RMSNorm**                  | No mean subtraction, stable in deep stacks.              |
| Embeddings           | **Tied**                      | Shared input/output LM head embeddings.                  |
| Vision / Multimodal  | **Adapters** (future)        | Q-Former + audio projection + modality router (~60M).    |
| Tokenizer            | Custom (in development)       | Multimodal + reasoning-aware tokenization by design.     |
| Training             | HuggingFace + distributed    | Continuous, checkpoint-resumable, cron-friendly.          |
