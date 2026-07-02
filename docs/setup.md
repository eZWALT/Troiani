# Setup Guide

## Prerequisites

- Linux, NVIDIA GPU, CUDA 11.6+
- Python 3.10+ (3.14 recommended via pyenv/conda)

## One-time setup

### Option A: pyenv (recommended)

```bash
pip install uv
pyenv virtualenv 3.14 troiani
pyenv local troiani
uv pip install -e ".[dev]"
```

### Option B: conda

```bash
conda create -n troiani python=3.14
conda activate troiani
pip install uv
uv pip install -e ".[dev]"
```

### Install Mamba-3 (from source, after environment is active)

```bash
MAMBA_FORCE_BUILD=TRUE pip install --no-cache-dir --force-reinstall \
  git+https://github.com/state-spaces/mamba.git --no-build-isolation
```

## Usage

```bash
pyenv activate troiani   # or: conda activate troiani
python -m troiani.data.tokenizer --input data/*.txt --vocab-size 46000
```

## Notes

- `mamba-ssm` is installed from source (compiles CUDA kernels). Requires `torch` and `cuda` to be available first.
- `causal-conv1d>=1.4.0` is a required backend for Mamba and is included in pyproject.toml.
- Vocab sizes tested: 32k, 46k, 54k. Default is 46k.
- All model configs assume tied embeddings.
