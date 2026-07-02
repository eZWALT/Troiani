import pytest
import torch


@pytest.fixture
def device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    pytest.skip("CUDA not available")


@pytest.fixture(params=[torch.float32, torch.bfloat16])
def dtype(request) -> torch.dtype:
    return request.param


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
