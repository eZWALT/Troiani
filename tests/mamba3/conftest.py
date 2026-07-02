import pytest
import torch


def pytest_configure(config):
    config.addinivalue_line("markers", "cuda: marks tests that require CUDA")


@pytest.fixture(scope="session")
def device() -> torch.device:
    if not torch.cuda.is_available():
        pytest.skip("CUDA not available")
    return torch.device("cuda")


def _warmup_mamba3(dtype, d_model=128):
    """Warmup Triton with the same kernel config used in tests."""
    from mamba_ssm import Mamba3
    m = Mamba3(d_model=d_model, d_state=16, expand=2, headdim=64, ngroups=1, device="cuda", dtype=dtype)
    x = torch.randn(1, 32, d_model, device="cuda", dtype=dtype)
    y = m(x)
    y.mean().backward()
    del m, x, y


_warmup_done = set()


@pytest.fixture(params=[torch.float32, torch.bfloat16])
def dtype(request) -> torch.dtype:
    dt = request.param
    if dt not in _warmup_done:
        _warmup_mamba3(dt)
        _warmup_done.add(dt)
    return dt


@pytest.fixture
def d_model() -> int:
    return 128


@pytest.fixture
def mamba3_kwargs(d_model):
    return dict(
        d_model=d_model,
        d_state=16,
        expand=2,
        headdim=64,
        ngroups=1,
        dt_min=0.001,
        dt_max=0.1,
        dt_init_floor=1e-4,
        A_floor=1e-4,
        chunk_size=64,
    )
