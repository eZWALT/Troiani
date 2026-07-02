# Setup Guide

## Option A: pyenv (recommended)

```bash
pip install uv
pyenv virtualenv 3.14 troiani
pyenv local troiani
uv pip install -e ".[dev]"
```

## Option B: conda

```bash
conda create -n troiani python=3.14
conda activate troiani
pip install uv
uv pip install -e ".[dev]"
```

## Usage

```bash
pyenv activate troiani   # or: conda activate troiani
python -m troiani.data.tokenizer --input data/*.txt --vocab-size 46000
```

## Notes

- Vocab sizes tested: 32k, 46k, 54k. Default is 46k.
- All model configs assume tied embeddings.
- Python 3.14 required. If 3.14 isnt available, 3.12+ works but update the commands above.
