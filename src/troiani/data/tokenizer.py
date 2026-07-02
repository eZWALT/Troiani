"""
Troiani BPE Tokenizer Trainer.

Trains a BPE tokenizer from text files using HuggingFace tokenizers.
Saves to resources/tokenizer/ for use in training.

Usage:
  python -m troiani.data.tokenizer --input data/*.txt --vocab-size 46000
"""

import argparse
import json
import os
from pathlib import Path

from tokenizers import Tokenizer, models, trainers, pre_tokenizers, normalizers, decoders


def create_tokenizer(vocab_size: int):
    tokenizer = Tokenizer(models.BPE(unk_token="<unk>"))
    tokenizer.normalizer = normalizers.NFKC()
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=True)
    tokenizer.decoder = decoders.ByteLevel()

    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        special_tokens=["<pad>", "<bos>", "<eos>", "<unk>", "<mask>"],
        min_frequency=2,
        show_progress=True,
    )
    return tokenizer, trainer


def train_tokenizer(files: list[str], vocab_size: int = 46000, output_dir: str = "resources/tokenizer"):
    tokenizer, trainer = create_tokenizer(vocab_size)
    print(f"Training BPE tokenizer (vocab_size={vocab_size}) on {len(files)} file(s)...")
    tokenizer.train(files, trainer)

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"tokenizer_{vocab_size}.json")
    tokenizer.save(path)

    with open(os.path.join(output_dir, f"tokenizer_{vocab_size}_config.json"), "w") as f:
        json.dump({
            "vocab_size": vocab_size,
            "type": "BPE",
            "normalizer": "NFKC",
            "pre_tokenizer": "ByteLevel",
            "special_tokens": ["<pad>", "<bos>", "<eos>", "<unk>", "<mask>"],
        }, f, indent=2)

    print(f"Tokenizer saved to {path}")
    print(f"Vocabulary size: {tokenizer.get_vocab_size()}")
    return tokenizer


def load_tokenizer(path: str):
    return Tokenizer.from_file(path)


class TroianiTokenizer:
    def __init__(self, vocab_size: int = 46000):
        self.vocab_size = vocab_size
        self.tokenizer, _ = create_tokenizer(vocab_size)

    @classmethod
    def from_pretrained(cls, path: str):
        instance = cls.__new__(cls)
        instance.tokenizer = load_tokenizer(path)
        instance.vocab_size = instance.tokenizer.get_vocab_size()
        return instance

    def train(self, files: list[str], output_dir: str = "resources/tokenizer"):
        self.tokenizer = train_tokenizer(files, self.vocab_size, output_dir)
        return self

    def encode(self, text: str) -> list[int]:
        return self.tokenizer.encode(text).ids

    def decode(self, ids: list[int]) -> str:
        return self.tokenizer.decode(ids)

    def encode_batch(self, texts: list[str]) -> list[list[int]]:
        return [self.encode(t) for t in texts]

    def decode_batch(self, batch: list[list[int]]) -> list[str]:
        return [self.decode(ids) for ids in batch]

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.tokenizer.save(path)

    @property
    def vocab_size(self) -> int:
        return self._vocab_size

    @vocab_size.setter
    def vocab_size(self, value: int):
        self._vocab_size = value

    def __len__(self) -> int:
        return self.tokenizer.get_vocab_size()

    def __getstate__(self):
        return {"vocab_size": self._vocab_size, "tokenizer_path": None}

    def __setstate__(self, state):
        self._vocab_size = state["vocab_size"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Troiani BPE tokenizer")
    parser.add_argument("--input", nargs="+", required=True, help="Input text files for training")
    parser.add_argument("--vocab-size", type=int, default=46000, choices=[32000, 46000, 54000], help="Vocab size")
    parser.add_argument("--output-dir", default="resources/tokenizer", help="Output directory")
    args = parser.parse_args()

    files = []
    for pattern in args.input:
        p = Path(pattern)
        if p.is_file():
            files.append(str(p))
        elif p.is_dir():
            files.extend([str(f) for f in p.rglob("*") if f.is_file()])

    if not files:
        print("No input files found.")
        exit(1)

    train_tokenizer(files, args.vocab_size, args.output_dir)
