# Setup Guide

## Prerequisites

- Linux, NVIDIA GPU, CUDA 11.6+
- Python 3.10+ (3.14 recommended via pyenv/conda)

## Clone

```bash
git clone https://github.com/eZWALT/Troiani.git
cd Troiani
```

## Environment setup

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

## Install Mamba-3 (from source)

Must be done after the environment is active and torch is installed:

```bash
# Verify torch is installed first
python -c "import torch; print(f'torch {torch.__version__}, cuda {torch.version.cuda}')"

# Compile and install the Mamba CUDA kernels
MAMBA_FORCE_BUILD=TRUE pip install --no-cache-dir --force-reinstall \
  git+https://github.com/state-spaces/mamba.git --no-build-isolation
```

This compiles the selective scan CUDA kernel. Takes a few minutes the first time.

## Verify everything works

```bash
# Test Mamba-3 imports
python -c "
import torch
from mamba_ssm import Mamba3
m = Mamba3(d_model=1088, d_state=128, headdim=64, is_mimo=True, mimo_rank=4, chunk_size=16, dtype=torch.bfloat16)
print(f'Mamba-3 OK: {sum(p.numel() for p in m.parameters())/1e6:.1f}M params')
"

# Test tokenizer module
python -c "from troiani.data.tokenizer import create_tokenizer; print('troiani.data OK')"
```

## Usage

```bash
pyenv activate troiani   # or: conda activate troiani
python -m troiani.data.tokenizer --input data/*.txt --vocab-size 46000
```

## Notes

- `mamba-ssm` is installed from source (compiles CUDA kernels). Requires torch+cuda available first.
- `causal-conv1d>=1.4.0` is a required backend for Mamba and is included in pyproject.toml.
- Vocab sizes tested: 32k, 46k, 54k. Default is 46k.
- All model configs assume tied embeddings.
