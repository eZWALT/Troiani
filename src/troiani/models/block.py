import torch
import torch.nn as nn

from .attention import GroupedQueryAttention
from .moe import MoELayer
from .norm import RMSNorm


class TransformerBlock(nn.Module):
    def __init__(
        self,
        d_model: int,
        n_heads: int,
        n_kv_heads: int,
        n_experts: int,
        hidden: int,
        max_seq_len: int,
        theta: float,
        routing: str = "expert_choice",
        capacity_factor: float = 1.25,
    ):
        super().__init__()
        self.attn_norm = RMSNorm(d_model)
        self.attn = GroupedQueryAttention(d_model, n_heads, n_kv_heads, max_seq_len, theta)
        self.ffn_norm = RMSNorm(d_model)
        self.moe = MoELayer(d_model, hidden, n_experts, routing=routing)
        if routing == "expert_choice":
            self.moe.router.capacity_factor = capacity_factor

    def forward(self, x: torch.Tensor, mask: torch.Tensor = None):
        h = self.attn(self.attn_norm(x), mask)
        x = x + h
        h, aux = self.moe(self.ffn_norm(x))
        x = x + h
        return x, aux
