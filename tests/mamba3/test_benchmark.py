"""Benchmark Mamba-3 vs MHA vs GQA at realistic configs."""
import time
import pytest
import torch
import torch.nn as nn
import torch.nn.functional as F
from mamba_ssm import Mamba3


def build_attention(d_model, n_heads, n_kv, device, dtype):
    """MHA (n_kv=None) or GQA (n_kv < n_heads)."""
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


def build_mamba3(d_model, device, dtype):
    return Mamba3(
        d_model=d_model, d_state=128, expand=2, headdim=64,
        ngroups=1, device=device, dtype=dtype,
    )


CONFIGS = [
    pytest.param(dict(d_model=1024, n_heads=16, n_kv=None), id="MHA-16h-d1024"),
    pytest.param(dict(d_model=1024, n_heads=16, n_kv=4),   id="GQA-16h4kv-d1024"),
    pytest.param(dict(d_model=2048, n_heads=32, n_kv=None), id="MHA-32h-d2048"),
    pytest.param(dict(d_model=2048, n_heads=32, n_kv=8),   id="GQA-32h8kv-d2048"),
]


@pytest.mark.benchmark
@pytest.mark.parametrize("cfg", CONFIGS)
@pytest.mark.parametrize("seq_len", [512, 2048])
def test_benchmark_attention_vs_mamba3(device, cfg, seq_len):
    dtype = torch.bfloat16
    batch = 2
    d_model = cfg["d_model"]
    n_heads = cfg["n_heads"]
    n_kv = cfg["n_kv"]
    kind = "MHA" if n_kv is None else "GQA"

    attn = build_attention(d_model, n_heads, n_kv, device, dtype)
    mamba = build_mamba3(d_model, device, dtype)
    x = torch.randn(batch, seq_len, d_model, device=device, dtype=dtype)
    warmup, iters = 3, 20

    def bench(model, forward_fn):
        for _ in range(warmup):
            forward_fn(model, x).mean().backward()
        torch.cuda.synchronize()

        model.zero_grad()
        torch.cuda.synchronize()
        t = time.time()
        for _ in range(iters):
            forward_fn(model, x)
        torch.cuda.synchronize()
        fw = (time.time() - t) / iters * 1000

        model.zero_grad()
        torch.cuda.synchronize()
        t = time.time()
        for _ in range(iters):
            forward_fn(model, x).mean().backward()
        torch.cuda.synchronize()
        fwbw = (time.time() - t) / iters * 1000

        p = sum(p.numel() for p in model.parameters())
        m = torch.cuda.max_memory_allocated() / 1e6
        torch.cuda.reset_peak_memory_stats()
        return fw, fwbw, p, m

    fw_a, fwbw_a, p_a, m_a = bench(attn, lambda m, x: m(x))
    fw_m, fwbw_m, p_m, m_m = bench(mamba, lambda m, x: m(x))

    label = f"{kind} {n_heads}h{'x'+str(n_kv)+'kv' if n_kv else ''} d={d_model} L={seq_len}"
    print(f"\n{label}")
    print(f"  {'':>12s} {'fw(ms)':>8s} {'fwbw(ms)':>8s} {'tok/s':>10s} {'params':>8s} {'mem(MB)':>8s}")
    print(f"  {'Attention':>12s} {fw_a:>8.1f} {fwbw_a:>8.1f} {int(batch*seq_len/(fw_a/1000)):>10,} {p_a:>8,} {m_a:>8.0f}")
    print(f"  {'Mamba-3':>12s} {fw_m:>8.1f} {fwbw_m:>8.1f} {int(batch*seq_len/(fw_m/1000)):>10,} {p_m:>8,} {m_m:>8.0f}")
    print(f"  {'Ratio(A/M)':>12s} {fw_a/fw_m:>8.2f}x {fwbw_a/fwbw_m:>8.2f}x")
