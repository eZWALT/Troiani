"""Benchmark Mamba-1/2/3 vs MHA vs GQA at realistic configs."""
import time
import pytest
import torch
import torch.nn as nn
import torch.nn.functional as F
from mamba_ssm import Mamba, Mamba2, Mamba3


def build_attention(d_model, n_heads, n_kv, device, dtype):
    head_dim = d_model // n_heads
    kv_heads = n_kv if n_kv is not None else n_heads

    class AttnLayer(nn.Module):
        def __init__(self):
            super().__init__()
            self.wq = nn.Linear(d_model, n_heads * head_dim, bias=False)
            self.wk = nn.Linear(d_model, kv_heads * head_dim, bias=False)
            self.wv = nn.Linear(d_model, kv_heads * head_dim, bias=False)
            self.wo = nn.Linear(n_heads * head_dim, d_model, bias=False)
            self.n_heads = n_heads
            self.kv_heads = kv_heads
            self.head_dim = head_dim

        def forward(self, x):
            B, T, C = x.shape
            q = self.wq(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
            k = self.wk(x).view(B, T, self.kv_heads, self.head_dim).transpose(1, 2)
            v = self.wv(x).view(B, T, self.kv_heads, self.head_dim).transpose(1, 2)
            if self.kv_heads != self.n_heads:
                k = k.repeat_interleave(self.n_heads // self.kv_heads, dim=1)
                v = v.repeat_interleave(self.n_heads // self.kv_heads, dim=1)
            y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
            y = y.transpose(1, 2).contiguous().view(B, T, -1)
            return self.wo(y)

    return AttnLayer().to(device, dtype)


def build_mamba(d_model, version, device, dtype):
    kwargs = dict(d_model=d_model, d_state=128, expand=2, d_conv=4,
                  device=device, dtype=dtype)
    if version == 1:
        return Mamba(**kwargs)
    elif version == 2:
        return Mamba2(**kwargs, headdim=64, ngroups=1, chunk_size=256)
    elif version == 3:
        return Mamba3(**kwargs, headdim=64, ngroups=1, chunk_size=64)


CONFIGS = [
    pytest.param(dict(d_model=1024, n_heads=16, n_kv=None, kind="MHA-16h"),       id="MHA-16h-d1024"),
    pytest.param(dict(d_model=1024, n_heads=16, n_kv=4,   kind="GQA-16hx4kv"),    id="GQA-16h4kv-d1024"),
    pytest.param(dict(d_model=1088, n_heads=17, n_kv=1,   kind="GQA-17hx1kv"),    id="GQA-17h1kv-d1088"),
    pytest.param(dict(d_model=2048, n_heads=32, n_kv=None, kind="MHA-32h"),       id="MHA-32h-d2048"),
    pytest.param(dict(d_model=2048, n_heads=32, n_kv=8,   kind="GQA-32hx8kv"),    id="GQA-32h8kv-d2048"),
]


@pytest.mark.benchmark
@pytest.mark.parametrize("cfg", CONFIGS)
@pytest.mark.parametrize("seq_len", [512, 2048])
def test_benchmark_all(device, cfg, seq_len):
    dtype = torch.bfloat16
    batch = 2
    d_model = cfg["d_model"]
    n_heads = cfg["n_heads"]
    n_kv = cfg["n_kv"]
    kind = cfg["kind"]

    attn = build_attention(d_model, n_heads, n_kv, device, dtype)
    m1 = build_mamba(d_model, 1, device, dtype)
    m2 = build_mamba(d_model, 2, device, dtype)
    m3 = build_mamba(d_model, 3, device, dtype)

    x = torch.randn(batch, seq_len, d_model, device=device, dtype=dtype)
    warmup, iters = 3, 20

    def bench(model):
        for _ in range(warmup):
            model(x).mean().backward()
        torch.cuda.synchronize()

        model.zero_grad()
        torch.cuda.synchronize()
        t = time.time()
        for _ in range(iters):
            model(x)
        torch.cuda.synchronize()
        fw = (time.time() - t) / iters * 1000

        model.zero_grad()
        torch.cuda.synchronize()
        t = time.time()
        for _ in range(iters):
            model(x).mean().backward()
        torch.cuda.synchronize()
        fwbw = (time.time() - t) / iters * 1000

        p = sum(p.numel() for p in model.parameters())
        m = torch.cuda.max_memory_allocated() / 1e6
        torch.cuda.reset_peak_memory_stats()
        tok_s = int(batch * seq_len / (fw / 1000))
        return fw, fwbw, tok_s, p, m

    results = {}
    for label, model in [("Attention", attn), ("Mamba-1", m1), ("Mamba-2", m2), ("Mamba-3", m3)]:
        results[label] = bench(model)

    label = f"{kind} d={d_model} L={seq_len}"
    print(f"\n{label}")
    print(f"  {'':>12s} {'fw(ms)':>8s} {'fwbw(ms)':>8s} {'tok/s':>10s} {'params':>9s} {'mem(MB)':>8s}")
    for k in ["Attention", "Mamba-1", "Mamba-2", "Mamba-3"]:
        r = results[k]
        print(f"  {k:>12s} {r[0]:>8.1f} {r[1]:>8.1f} {r[2]:>10,} {r[3]:>9,} {r[4]:>8.0f}")
    # Ratios relative to Mamba-3
    m3 = results["Mamba-3"]
    print(f"  {'Ratio v3':>12s} {'fw':>8s} {'fwbw':>8s} {'tok/s':>10s}")
    for k in ["Attention", "Mamba-1", "Mamba-2"]:
        r = results[k]
        print(f"  {f'{k}/M3':>12s} {r[0]/m3[0]:>8.2f}x {r[1]/m3[1]:>8.2f}x {r[2]/m3[2]:>8.2f}x")
