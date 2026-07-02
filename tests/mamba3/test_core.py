import pytest
import torch
from mamba_ssm import Mamba3


class TestSingleMamba3:

    def test_forward_shape(self, device, dtype, mamba3_kwargs):
        model = Mamba3(**mamba3_kwargs, device=device, dtype=dtype)
        x = torch.randn(2, 64, mamba3_kwargs["d_model"], device=device, dtype=dtype)
        y = model(x)
        assert y.shape == x.shape, f"{y.shape} != {x.shape}"

    def test_backward(self, device, dtype, mamba3_kwargs):
        model = Mamba3(**mamba3_kwargs, device=device, dtype=dtype)
        x = torch.randn(2, 64, mamba3_kwargs["d_model"], device=device, dtype=dtype)
        y = model(x)
        loss = y.mean()
        loss.backward()
        grads = [p.grad for p in model.parameters() if p.grad is not None]
        assert len(grads) > 0, "no gradients"
        assert all(g.isfinite().all() for g in grads), "non-finite gradients"

    def test_batch_independent(self, device, dtype, mamba3_kwargs):
        model = Mamba3(**mamba3_kwargs, device=device, dtype=dtype)
        model.eval()
        x = torch.randn(4, 32, mamba3_kwargs["d_model"], device=device, dtype=dtype)
        y = model(x)
        atol = 1e-2 if dtype == torch.bfloat16 else 1e-5
        for i in range(4):
            single = model(x[i : i + 1])
            assert torch.allclose(y[i : i + 1], single, atol=atol), (
                f"batch position {i} differs"
            )

    def test_numeric_stability(self, device, dtype, mamba3_kwargs):
        model = Mamba3(**mamba3_kwargs, device=device, dtype=dtype)
        model.eval()
        x = torch.randn(1, 1024, mamba3_kwargs["d_model"], device=device, dtype=dtype)
        y = model(x)
        assert y.isfinite().all(), "non-finite output on long sequence"
