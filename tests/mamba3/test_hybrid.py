import pytest
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


def build_hybrid_stack(d_model, n_layers=6, gqa_interval=6, device="cuda", dtype=torch.float32):
    layers = []
    for i in range(n_layers):
        if (i + 1) % gqa_interval == 0:
            layers.append(GQALayer(d_model, n_heads=8, n_kv_heads=1))
        else:
            layers.append(Mamba3(
                d_model=d_model, d_state=16, expand=2,
                headdim=64, ngroups=1, device=device, dtype=dtype,
            ))
    return nn.Sequential(*layers).to(device, dtype)


class TestHybridStack:

    @pytest.fixture(params=[4, 6, 12])
    def n_layers(self, request):
        return request.param

    def test_forward_shape(self, device, dtype, d_model, n_layers):
        model = build_hybrid_stack(d_model, n_layers, device=device, dtype=dtype)
        x = torch.randn(2, 64, d_model, device=device, dtype=dtype)
        y = model(x)
        assert y.shape == x.shape, f"{y.shape} != {x.shape}"

    def test_backward(self, device, dtype, d_model, n_layers):
        model = build_hybrid_stack(d_model, n_layers, device=device, dtype=dtype)
        x = torch.randn(2, 64, d_model, device=device, dtype=dtype)
        y = model(x)
        loss = y.mean()
        loss.backward()
        grads = [p.grad for p in model.parameters() if p.grad is not None]
        assert len(grads) > 0, "no gradients"
        assert all(g.isfinite().all() for g in grads), "non-finite gradients"

    def test_gqa_placement(self, device, dtype, d_model):
        gqa_interval = 6
        model = build_hybrid_stack(
            d_model, n_layers=12, gqa_interval=gqa_interval,
            device=device, dtype=dtype,
        )
        for i, layer in enumerate(model):
            is_gqa = isinstance(layer, GQALayer)
            expected_gqa = ((i + 1) % gqa_interval == 0)
            assert is_gqa == expected_gqa, (
                f"layer {i}: expected GQA={expected_gqa}, got GQA={is_gqa}"
            )
