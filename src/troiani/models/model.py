import torch
import torch.nn as nn
import torch.nn.functional as F
from dataclasses import dataclass

from .block import TransformerBlock
from .norm import RMSNorm


@dataclass
class TroianiConfig:
    d_model: int = 1024
    n_heads: int = 16
    n_kv_heads: int = 4
    n_layers: int = 22
    n_experts: int = 6
    hidden: int = 2048
    vocab_size: int = 50032
    max_seq_len: int = 8192
    theta: float = 10000.0
    routing: str = "expert_choice"
    capacity_factor: float = 1.25


class TroianiModel(nn.Module):
    def __init__(self, config: TroianiConfig):
        super().__init__()
        self.config = config
        self.embed = nn.Embedding(config.vocab_size, config.d_model)
        self.layers = nn.ModuleList([
            TransformerBlock(
                config.d_model,
                config.n_heads,
                config.n_kv_heads,
                config.n_experts,
                config.hidden,
                config.max_seq_len,
                config.theta,
                config.routing,
                config.capacity_factor,
            )
            for _ in range(config.n_layers)
        ])
        self.norm = RMSNorm(config.d_model)

    def forward(self, x: torch.Tensor, mask: torch.Tensor = None):
        h = self.embed(x)
        aux_loss = 0.0
        for layer in self.layers:
            h, aux = layer(h, mask)
            aux_loss = aux_loss + aux
        h = self.norm(h)
        return h, aux_loss


class TroianiForCausalLM(nn.Module):
    def __init__(self, config: TroianiConfig):
        super().__init__()
        self.model = TroianiModel(config)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)
        self.lm_head.weight = self.model.embed.weight

    def forward(self, x: torch.Tensor, labels: torch.Tensor = None, mask: torch.Tensor = None):
        h, aux_loss = self.model(x, mask)
        logits = self.lm_head(h)

        loss = None
        if labels is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), labels.view(-1))
        return logits, aux_loss, loss
