# Setup Guide

## Prerequisites

- Linux, NVIDIA GPU (A100/H100 tested), CUDA 12.x driver
- Python 3.10+ (3.14 recommended)

## Clone

```bash
git clone https://github.com/eZWALT/Troiani.git
cd Troiani
```

## Install PyTorch

Pick the CUDA version matching your driver. CUDA 12.7 driver is backward compatible with cu126 wheels:

```bash
# CUDA 12.6 (stable, recommended for A100s)
pip install torch --index-url https://download.pytorch.org/whl/cu126

# OR CUDA 13.0 (experimental, needs driver >=580.65)
pip install torch --index-url https://download.pytorch.org/whl/cu130
```

Verify:

```bash
python -c "import torch; print(f'torch {torch.__version__}, cuda {torch.version.cuda}, sm {torch.cuda.get_device_capability()}')"
```

## Environment setup

### Conda (from environment.yml)

```bash
conda env create -f environment.yml
conda activate troiani
pip install uv
uv pip install -e ".[dev]"
```

### pyenv

`.python-version` file is provided in the repo for automatic version switching:

```bash
pip install uv
pyenv virtualenv 3.14 troiani
pyenv local troiani
uv pip install -e ".[dev]"
```

## Install Mamba-3 (from source, after troiani deps)

```bash
MAMBA_FORCE_BUILD=TRUE pip install --no-cache-dir --force-reinstall \
  git+https://github.com/state-spaces/mamba.git --no-build-isolation
```

This compiles the selective scan CUDA kernel. Needs ninja, CUDA toolkit, and torch already installed. Takes a few minutes.

## Verify

```bash
python -c "
import torch
from mamba_ssm import Mamba3
m = Mamba3(d_model=1088, d_state=128, headdim=64,
           is_mimo=True, mimo_rank=4, chunk_size=16, dtype=torch.bfloat16)
print(f'Mamba-3 OK: {sum(p.numel() for p in m.parameters())/1e6:.1f}M params')
"
python -c "from troiani.data.tokenizer import create_tokenizer; print('troiani.data OK')"
```

## Usage

```bash
pyenv activate troiani   # or: conda activate troiani
python -m troiani.data.tokenizer --input data/*.txt --vocab-size 46000
```

## Version notes

- Mamba-3 requires `tilelang==0.1.8`, `triton>=3.5.0`, `quack-kernels>=0.3.4` (all in pyproject.toml)
- `causal-conv1d>=1.2.0` is listed as optional in mamba repo but included here for convenience
- All model configs assume tied embeddings
- Vocab sizes tested: 32k, 46k, 54k. Default is 46k
