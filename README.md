<div align="center">

  <a href="https://github.com/eZWALT/Troiani">
    <img src="resources/troiani_logo_white.png" alt="Troiani" width="350"/>
  </a>

  <h1>Troiani</h1>

  <p><strong>The openest LLM model family — built from scratch, in the open, end-to-end.</strong></p>

  <p>
    <a href="https://github.com/eZWALT/Troiani/blob/main/LICENSE">
      <img alt="License" src="https://img.shields.io/badge/license-Apache--2.0-blue.svg">
    </a>
    <a href="https://github.com/eZWALT/Troiani">
      <img alt="Status" src="https://img.shields.io/badge/status-pre--alpha-orange.svg">
    </a>
    <a href="https://github.com/eZWALT/Troiani/stargazers">
      <img alt="GitHub stars" src="https://img.shields.io/github/stars/eZWALT/Troiani?style=social">
    </a>
    <a href="https://github.com/eZWALT/Troiani/commits/main">
      <img alt="Last commit" src="https://img.shields.io/github/last-commit/eZWALT/Troiani?color=brightgreen">
    </a>
    <a href="https://github.com/eZWALT/Troiani/issues">
      <img alt="Issues" src="https://img.shields.io/github/issues/eZWALT/Troiani">
    </a>
  </p>

</div>

---

> **The Troiani Model Family (v0)** — a cookbook, recipe book, and full source tree for training language models from scratch. Tokenizer, architecture, data pipeline, trainer, and eval harness — all open, all hackable.

## Why Troiani?

- **From Scratch** — Every component, from the tokenizer to the distributed trainer, is built in the open. No hidden sauce.
- **Modern Architecture** — Troiani combines **Mamba-2** (selective state-space model), **SwiGLU** MLPs, and **Grouped Query Attention (GQA)** for efficient, multimodal-capable, reasoning-first models. Designed for deep, Mamba-dominant hybrids at sub-1B scale.
- **Radically Open** — Datasets, configs, hyperparameters, and even failure logs are public. The openest LLM model family ever.
- **Resilient Training** — Designed for checkpoint-driven, interruptible training that survives preempted jobs and cron-scheduled restarts.
- **Educational** — A reference for anyone who wants to understand how an LLM is built, end-to-end, without wading through a framework.

## News

<details>
<summary><b>Click to expand</b></summary>

- **2026-06-29** — Completed architecture research: landed on **Mamba-2 + sparse GQA** hybrid with SwiGLU MLPs. LIV long-conv evaluated and deferred (Mamba's SSM already provides selective global mixing). See [Architecture](#architecture) section.
- **2026-06-24** — Published the Troiani v1 roadmap (see [`docs/Troiani-v1-roadmap.md`](docs/Troiani-v1-roadmap.md)).
- **2026-06-22** — Laid out the minimal repository structure (src, config, docs, research, tests).
- **2026-06-22** — Initial commit. The journey begins.

</details>

## Architecture

Troiani v0 is a **Mamba-2-dominant hybrid** with sparse GQA, SwiGLU MLPs, RoPE + YaRN, and tied embeddings. Built to stay under 1B params with room for multimodal adapters. Mamba-3 is planned for a future iteration once released.

### Design rationale

Extensive parameter budgeting across d_model (512–1536), MLP ratios (2.0–4.0), layer counts, and mixing schemes (Mamba/LIV/GQA) led to the following conclusions:

1. **Mamba-2 is the backbone.** Its selective SSM provides input-dependent global mixing in O(L) time — already a superset of what a static long-conv (LIV) offers. Mamba-2's built-in `conv1d` (k=4) and `d_state=128` cover local and global receptive fields.

2. **LIV long-conv is deferred.** LIV duplicates Mamba's global mixing but without selectivity. It only helps early-layer feature extraction on data with fixed/periodic patterns. Net param cost isn't justified for language at sub-1B scale. Revisit if multimodal data shows strong shift-invariant structure.

3. **GQA every 5–6 layers is the sweet spot** (~17–20% attention). Matches the Jamba design philosophy — enough for sharp content retrieval, Mamba dominates the rest.

4. **SwiGLU with ratio 8/3** (LLaMA-style). The gating-optimized default — preserves the capacity of a 4× FFN at lower param cost.

5. **d_model=1024** — wide enough for multimodal fusion (vision/audio features need the capacity), still deep at 36 layers.

### Target config: Troiani-base (~806M)

```
d_model:           1024
n_layers:          36  (30 Mamba-2 + 6 GQA)
layer pattern:     [M M M M M A] × 6   (GQA every 6th, 17% attention)
MLP:               SwiGLU, ratio 8/3  (hidden = 2731)
SSM:               Mamba-2 (d_state=128, d_conv=4, expand=2)
Attention:         GQA (8 query heads, 1 KV head)
Positional enc:    RoPE + YaRN (for context extension)
Norm:              RMSNorm
Embeddings:        Tied (input = output LM head)
Vocab:             32,000

Base params:       ~806M
+ multimodal       ~60M  (vision Q-Former + audio adapter + router)
adapters:          ────
Total:             ~866M  (134M headroom under 1B)

Depth variants:
  30 layers → 677M base (737M w/ adapters)
  42 layers → 934M base (994M w/ adapters, max under 1B)
```

### Per-layer param breakdown (d=1024, SwiGLU ratio 8/3)

| Layer type | Params/layer | Role |
|------------|-------------|------|
| Mamba-2    | ~23.6M       | Selective global state-space mixer (dominant) |
| GQA        | ~10.7M       | Sharp content retrieval, KV-cache efficient |
| SwiGLU MLP | ~8.4M        | Feedforward non-linearity |
| RMSNorm    | ~2K          | Per-token normalization |

### Component table

| Component            | Choice                          | Notes                                                         |
|----------------------|---------------------------------|---------------------------------------------------------------|
| Sequence Mixer       | **Mamba-2** (Mamba-3 planned)   | Selective SSM, `d_state=128`, linear-time long-context. Will upgrade to Mamba-3 when available. |
| Attention            | **GQA** (every 6th layer)      | KV-cache efficient; sharp retrieval without quality loss.    |
| Feedforward          | **SwiGLU** (ratio 8/3)         | LLaMA-style gated MLP, capacity-efficient.                   |
| Positional Encoding  | **RoPE + YaRN**                | Rotary embeddings with YaRN for context extension.            |
| Normalization        | **RMSNorm**                    | No mean subtraction, stable in deep stacks.                  |
| Embeddings           | **Tied**                        | Shared input/output LM head embeddings.                      |
| Vision / Multimodal  | **Adapters** (future)          | Q-Former + audio projection + modality router (~60M budget). |
| Tokenizer            | Custom (in development)         | Multimodal + reasoning-aware tokenization by design.         |
| Training             | HuggingFace + distributed      | Continuous, checkpoint-resumable, cron-friendly.              |

## Repository Structure

```
Troiani/
├── config/         # Training and model configuration
├── docs/           # Roadmaps and design documents
│   └── Troiani-v1-roadmap.md
├── research/       # Research notes and experiments
├── src/
│   ├── data/           # Data loading and preprocessing
│   ├── evaluation/     # Benchmarks and evaluation harness
│   ├── models/         # Model architecture definitions
│   ├── pipelines/      # End-to-end data and training pipelines
│   ├── train/          # Training scripts and loops
│   └── troiani/        # Core Troiani package
├── tests/          # Unit and integration tests
├── pyproject.toml
└── LICENSE
```

## Install

The Troiani model family is under active development and is installed from source:

```bash
git clone https://github.com/eZWALT/Troiani.git
cd Troiani
pip install -e .
```

## Usage

The first MVP model is being trained. Once checkpoints are available, inference and fine-tuning guides will land here. In the meantime, track progress in the [v1 roadmap](docs/Troiani-v1-roadmap.md).

## Roadmap

The Troiani v1 roadmap — see [`docs/Troiani-v1-roadmap.md`](docs/Troiani-v1-roadmap.md) for the live version:

- [ ] Create a tokenizer that allows multimodality and reasoning from the get-go
- [ ] Data preprocessing pipeline validation
- [ ] Data selection
- [x] Research optimal hyperparameters and values for the architecture (Mamba-2 + GQA, SwiGLU 8/3, d=1024, GQA every 6th)
- [ ] Build and try the architecture (Mamba-2 + GQA) (inference and train)
- [ ] Create the initial training HF script (test with continuous training of a tiny model)
- [ ] Refine strategy for constantly interrupted jobs (cronjob / checkpoints) so it will always be training
- [ ] Get config values for OOM (HF, Academia pretraining...¿?)
- [ ] Upgrade to Mamba-3 when available

## Contributing

All positive and productive contributions are welcome. As the project matures, a `CONTRIBUTING.md` with guidelines will be added. In the meantime, feel free to open [issues](https://github.com/eZWALT/Troiani/issues) or [pull requests](https://github.com/eZWALT/Troiani/pulls).

## Acknowledgements

Troiani builds on the open-source work of many. Key inspirations:

- [Mamba](https://github.com/state-spaces/mamba) — selective state-space models.
- [Transformers](https://github.com/huggingface/transformers) — HuggingFace ecosystem.
- [nanoGPT](https://github.com/karpathy/nanoGPT) — the simplest from-scratch GPT trainer.
- [TinyLlama](https://github.com/jzhang38/TinyLlama) — open pretraining playbook.
- [OLMo](https://github.com/allenai/OLMo) — fully open language model stack.

## Citation

If you find Troiani useful, please cite:

```bibtex
@misc{troiani2026,
  title        = {Troiani: The Openest LLM Model Family Built From Scratch},
  author       = {eZWALT},
  year         = {2026},
  url          = {https://github.com/eZWALT/Troiani},
}
```

## License

This project is licensed under the Apache v2.0 License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**[⭐ Star this repo](https://github.com/eZWALT/Troiani)** to follow the Troiani model family's journey from scratch.

</div>
