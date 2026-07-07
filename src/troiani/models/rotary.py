import torch
import torch.nn as nn


def precompute_freqs_cis(
    dim: int, max_seq_len: int, theta: float = 10000.0, device: torch.device = None, dtype: torch.dtype = None
) -> torch.Tensor:
    freqs = 1.0 / (theta ** (torch.arange(0, dim, 2, device=device).float() / dim))
    t = torch.arange(max_seq_len, device=device).float()
    freqs = torch.outer(t, freqs)
    return torch.stack([torch.cos(freqs), torch.sin(freqs)], dim=-1).to(dtype=dtype)


def apply_rotary_emb(x: torch.Tensor, freqs_cis: torch.Tensor) -> torch.Tensor:
    x_2d = x.float().reshape(*x.shape[:-1], -1, 2)
    x_cos = x_2d[..., 0]
    x_sin = x_2d[..., 1]
    freqs = freqs_cis[: x.shape[-3], :, :].unsqueeze(1)
    rot_cos = freqs[..., 0]
    rot_sin = freqs[..., 1]
    out = torch.stack(
        [x_cos * rot_cos - x_sin * rot_sin, x_cos * rot_sin + x_sin * rot_cos], dim=-1
    )
    return out.flatten(-2).to(x.dtype)
