# Troiani v1 Architecture

Troiani v1 is a **Mamba-3-dominant hybrid** with sparse GQA, SwiGLU MLPs, RoPE + YaRN, and tied embeddings. Built to stay under 1B params with room for multimodal adapters.

## Design Rationale

Extensive parameter budgeting across d_model (512-1536), MLP ratios (2.0-4.0), layer counts, and mixing schemes (Mamba/LIV/GQA) led to the following conclusions:

1. **Mamba-3 is the backbone.** Its selective SSM provides input-dependent global mixing in O(L) time - already a superset of what a static long-conv (LIV) offers. Mamba's built-in conv1d (k=4) and d_state=128 cover local and global receptive fields.

2. **LIV long-conv is deferred.** LIV duplicates Mamba's global mixing but without selectivity. It only helps early-layer feature extraction on data with fixed/periodic patterns. Net param cost isn't justified for language at sub-1B scale. Revisit if multimodal data shows strong shift-invariant structure.

3. **GQA every 5-6 layers is the sweet spot** (~17-20% attention). Matches the Jamba design philosophy - enough for sharp content retrieval, Mamba dominates the rest.

4. **SwiGLU with ratio 8/3** (LLaMA-style). The gating-optimized default - preserves the capacity of a 4x FFN at lower param cost.

5. **d_model=1088** - wider than 1024 for better per-layer representational capacity, still 36 layers deep under 1B. GQA every 6 gives 30 Mamba-3 + 6 GQA.

## Target Config: Troiani-base (~921M)

```
d_model:           1088
n_layers:          36  (30 Mamba-3 + 6 GQA)
layer pattern:     [M M M M M A] x 6   (GQA every 6th, 17% attention)
MLP:               SwiGLU, ratio 8/3  (hidden = 2901)
SSM:               Mamba-3 (d_state=128, d_conv=4, expand=2)
Attention:         GQA (8 query heads, 1 KV head)
Positional enc:    RoPE + YaRN (for context extension)
Norm:              RMSNorm
Embeddings:        Tied (input = output LM head)
Vocab:             46,000

Base params:       ~921M
+ multimodal       ~60M  (vision Q-Former + audio adapter + router)
adapters:          ----
Total:             ~981M  (19M headroom under 1B)
```

### Vocab Variants (36 layers)

| Vocab  | Embedding | Base Params | + Adapters | Room   |
|--------|-----------|-------------|------------|--------|
| 32,000 | 34.8M     | 906M        | 966M       | 34M    |
| 46,000 | 50.1M     | 921M        | 981M       | 19M    |
| 54,000 | 58.8M     | 930M        | 990M       | 10M    |

## Per-Layer Param Breakdown (d=1088, SwiGLU ratio 8/3)

| Layer type | Params/layer | Role |
|------------|-------------|------|
| Mamba-3    | ~26.6M       | Selective global state-space mixer (dominant) |
| GQA        | ~12.1M       | Sharp content retrieval, KV-cache efficient |
| SwiGLU MLP | ~9.5M        | Feedforward non-linearity |
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
