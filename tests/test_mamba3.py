"""Sanity tests for Mamba-3 hybrid stack."""
import torch
import torch.nn as nn
import torch.nn.functional as F
from mamba_ssm import Mamba3


class GQALayer(nn.Module):
    def __init__(self, d_model: int, n_heads: int, n_kv_heads: int):
        super().__init__()
        self.n_heads = n_heads
        self.n_kv_heads = n_kv_heads
        self.head_dim = d_model // n_heads
        self.wq = nn.Linear(d_model, d_model, bias=False)
        self.wk = nn.Linear(d_model, n_kv_heads * self.head_dim, bias=False)
        self.wv = nn.Linear(d_model, n_kv_heads * self.head_dim, bias=False)
        self.wo = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, C = x.shape
        q = self.wq(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        k = self.wk(x).view(B, T, self.n_kv_heads, self.head_dim).transpose(1, 2)
        v = self.wv(x).view(B, T, self.n_kv_heads, self.head_dim).transpose(1, 2)
        k = k.repeat_interleave(self.n_heads // self.n_kv_heads, dim=1)
        v = v.repeat_interleave(self.n_heads // self.n_kv_heads, dim=1)
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.wo(y)


def test_single_mamba3():
    model = Mamba3(
        d_model=64, d_state=16, expand=2, headdim=64,
        ngroups=1, device="cuda", dtype=torch.float32,
    )
    x = torch.randn(2, 128, 64, device="cuda")
    y = model(x)
    loss = y.mean()
    loss.backward()
    assert y.shape == x.shape, f"Expected {x.shape}, got {y.shape}"
    print("  single Mamba3: PASSED")


def test_hybrid_stack():
    d_model = 128
    layers = nn.ModuleList()
    for i in range(6):
        if i == 5:
            layers.append(GQALayer(d_model, n_heads=4, n_kv_heads=2))
        else:
            layers.append(Mamba3(
                d_model=d_model, d_state=16, expand=2,
                headdim=64, ngroups=1, device="cuda", dtype=torch.float32,
            ))
    model = nn.Sequential(*layers).to("cuda")
    x = torch.randn(2, 64, d_model, device="cuda")
    y = model(x)
    loss = y.mean()
    loss.backward()
    assert y.shape == x.shape, f"Expected {x.shape}, got {y.shape}"
    total = sum(p.numel() for p in model.parameters())
    grad_norm = sum(p.grad.norm().item() for p in model.parameters() if p.grad is not None)
    print(f"  hybrid (5 Mamba3 + 1 GQA): {total:,} params, grad_norm={grad_norm:.4f}")


if __name__ == "__main__":
    test_single_mamba3()
    test_hybrid_stack()
    print("All Mamba-3 sanity tests: PASSED")
