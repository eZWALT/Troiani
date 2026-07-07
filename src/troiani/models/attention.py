import torch
import torch.nn as nn
import torch.nn.functional as F

from .rotary import apply_rotary_emb, precompute_freqs_cis


class GroupedQueryAttention(nn.Module):
    def __init__(self, d_model: int, n_heads: int, n_kv_heads: int, max_seq_len: int = 8192, theta: float = 10000.0):
        super().__init__()
        self.n_heads = n_heads
        self.n_kv_heads = n_kv_heads
        self.n_groups = n_heads // n_kv_heads
        self.head_dim = d_model // n_heads
        self.max_seq_len = max_seq_len

        self.wq = nn.Linear(d_model, n_heads * self.head_dim, bias=False)
        self.wk = nn.Linear(d_model, n_kv_heads * self.head_dim, bias=False)
        self.wv = nn.Linear(d_model, n_kv_heads * self.head_dim, bias=False)
        self.wo = nn.Linear(n_heads * self.head_dim, d_model, bias=False)

        self.freqs_cis = None

    def _reshape(self, x: torch.Tensor, n_heads: int) -> torch.Tensor:
        B, T, D = x.shape
        return x.view(B, T, n_heads, self.head_dim).transpose(1, 2)

    def forward(self, x: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        B, T, D = x.shape

        q = self._reshape(self.wq(x), self.n_heads)
        k = self._reshape(self.wk(x), self.n_kv_heads)
        v = self._reshape(self.wv(x), self.n_kv_heads)

        if self.freqs_cis is None or self.freqs_cis.size(0) < T:
            self.freqs_cis = precompute_freqs_cis(
                self.head_dim, max(T, self.max_seq_len), device=x.device, dtype=x.dtype
            )

        q = apply_rotary_emb(q, self.freqs_cis)
        k = apply_rotary_emb(k, self.freqs_cis)

        if self.n_groups > 1:
            k = k.repeat_interleave(self.n_groups, dim=1)
            v = v.repeat_interleave(self.n_groups, dim=1)

        out = F.scaled_dot_product_attention(q, k, v, attn_mask=mask, is_causal=mask is None)
        out = out.transpose(1, 2).contiguous().view(B, T, D)
        return self.wo(out)
