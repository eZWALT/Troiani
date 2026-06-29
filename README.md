<div align="center">

  <a href="https://github.com/eZWALT/Troiani">
    <img src="resources/troiani_logo_transparent.png" alt="Troiani" width="350"/>
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
- **Modern Architecture** — Troiani combines **LIV**, **Mamba-3**, and **Grouped Query Attention (GQA)** for efficient, multimodal-capable, reasoning-first models.
- **Radically Open** — Datasets, configs, hyperparameters, and even failure logs are public. The openest LLM model family ever.
- **Resilient Training** — Designed for checkpoint-driven, interruptible training that survives preempted jobs and cron-scheduled restarts.
- **Educational** — A reference for anyone who wants to understand how an LLM is built, end-to-end, without wading through a framework.

## News

<details>
<summary><b>Click to expand</b></summary>

- **2026-06-24** — Published the Troiani v1 roadmap (see [`docs/Troiani-v1-roadmap.md`](docs/Troiani-v1-roadmap.md)).
- **2026-06-22** — Laid out the minimal repository structure (src, config, docs, research, tests).
- **2026-06-22** — Initial commit. The journey begins.

</details>

## Architecture

Troiani v0 targets a modern, efficient, multimodal-ready backbone:

| Component            | Choice                          | Notes                                                         |
|----------------------|---------------------------------|---------------------------------------------------------------|
| Sequence Mixer       | **Mamba-3**                     | Selective state-space model for linear-time long-context.    |
| Attention            | **Grouped Query Attention**     | KV-cache efficient; scales inference without quality loss.   |
| Vision / Multimodal  | **LIV**                         | Native multimodal fusion from the tokenizer up.              |
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
- [ ] Research optimal hyperparameters and values for the architecture (LIV + Mamba3 + GQA)
- [ ] Build and try the architecture (Mamba-3) (inference and train)
- [ ] Create the initial training HF script (test with continuous training of a tiny model)
- [ ] Refine strategy for constantly interrupted jobs (cronjob / checkpoints) so it will always be training
- [ ] Get config values for OOM (HF, Academia pretraining...¿?)

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
