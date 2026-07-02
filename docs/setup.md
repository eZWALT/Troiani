# Setup Guide

## Prerequisites

- Python 3.10+ (3.12 recommended)
- [pyenv](https://github.com/pyenv/pyenv) + [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
- [uv](https://github.com/astral-sh/uv) (fast Python package installer)

## One-time setup

```bash
# Install uv if you don't have it
pip install uv

# Create virtual environment with pyenv
pyenv virtualenv 3.12 troiani
pyenv local troiani

# Install dependencies with uv (much faster than pip)
uv pip install -e ".[dev]"
```

## Daily workflow

```bash
# Activate the environment
pyenv activate troiani

# Or if using just venv:
# python3 -m venv .venv && source .venv/bin/activate

# Run the tokenizer
python -m troiani.data.tokenizer --input data/raw/*.txt --vocab-size 46000

# Run tests
pytest tests/

# Format code
black src/ tests/
ruff check src/ tests/
```

## Project structure

```
Troiani/
  src/troiani/
    data/         # tokenizer, dataset, dataloader
    models/       # Mamba-3 + GQA blocks
    train/        # training loop and distributed trainer
    evaluation/   # eval harness
  resources/
    tokenizer/    # trained tokenizer files
  config/         # model and training configs
  docs/           # architecture docs
  research/       # experiments and parameter sweeps
```

## Notes

- The tokenizer trains a BPE tokenizer using HuggingFace `tokenizers`.
- Vocab sizes tested: 32000, 46000, 54000. Default is 46000.
- All model configs assume tied embeddings (shared input/output).
