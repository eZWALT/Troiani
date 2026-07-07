import torch
import torch.nn as nn
import torch.nn.functional as F


class SwiGLU(nn.Module):
    def __init__(self, d_model: int, hidden: int):
        super().__init__()
        self.gate = nn.Linear(d_model, hidden, bias=False)
        self.up = nn.Linear(d_model, hidden, bias=False)
        self.down = nn.Linear(hidden, d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.down(F.silu(self.gate(x)) * self.up(x))


class Top2Router(nn.Module):
    def __init__(self, d_model: int, n_experts: int):
        super().__init__()
        self.router = nn.Linear(d_model, n_experts, bias=False)

    def forward(self, x: torch.Tensor):
        logits = self.router(x)
        scores = F.softmax(logits.float(), dim=-1).to(logits.dtype)
        top2_scores, top2_idx = scores.topk(2, dim=-1)
        return top2_scores, top2_idx, logits

    def load_balancing_loss(self, logits: torch.Tensor, top2_idx: torch.Tensor) -> torch.Tensor:
        n_experts = logits.size(-1)
        mask = F.one_hot(top2_idx, n_experts).float()
        f = mask.view(-1, n_experts).mean(dim=0)
        g = F.softmax(logits.float(), dim=-1).view(-1, n_experts).mean(dim=0)
        cv = (f / (f.mean() + 1e-6) - 1).pow(2).mean()
        return cv


class ExpertChoiceRouter(nn.Module):
    def __init__(self, d_model: int, n_experts: int, capacity_factor: float = 1.25):
        super().__init__()
        self.router = nn.Linear(d_model, n_experts, bias=False)
        self.capacity_factor = capacity_factor

    def forward(self, x: torch.Tensor):
        B, T, D = x.shape
        n_experts = self.router.weight.size(0)
        logits = self.router(x)
        scores = F.softmax(logits.float(), dim=-1).to(logits.dtype)
        flat_scores = scores.view(-1, n_experts)
        k = int(B * T * self.capacity_factor / n_experts)
        topk_scores, topk_idx = flat_scores.topk(k, dim=0)
        return topk_scores, topk_idx, logits

    def load_balancing_loss(self, logits: torch.Tensor) -> torch.Tensor:
        n_experts = logits.size(-1)
        g = F.softmax(logits.float(), dim=-1).view(-1, n_experts).mean(dim=0)
        target = torch.ones(n_experts, device=logits.device) / n_experts
        cv = ((g - target).pow(2) / (target + 1e-6)).mean()
        return cv


class MoELayer(nn.Module):
    def __init__(self, d_model: int, hidden: int, n_experts: int, routing: str = "top2"):
        super().__init__()
        self.n_experts = n_experts
        self.routing = routing
        self.experts = nn.ModuleList([SwiGLU(d_model, hidden) for _ in range(n_experts)])

        if routing == "top2":
            self.router = Top2Router(d_model, n_experts)
        elif routing == "expert_choice":
            self.router = ExpertChoiceRouter(d_model, n_experts)
        else:
            raise ValueError(f"Unknown routing: {routing}")

    def forward(self, x: torch.Tensor):
        B, T, D = x.shape
        flat_x = x.view(-1, D)

        if self.routing == "top2":
            scores, idx, logits = self.router(x)
            flat_scores = scores.view(-1, 2)
            flat_idx = idx.view(-1, 2)

            out = torch.zeros_like(flat_x)
            for e in range(self.n_experts):
                mask = (flat_idx == e).any(dim=-1)
                if not mask.any():
                    continue
                sel_scores = flat_scores[mask]
                sel_idx = flat_idx[mask]
                weight_mask = (sel_idx == e)
                weights = sel_scores[weight_mask].unsqueeze(-1)
                out[mask] += self.experts[e](flat_x[mask]) * weights

            aux_loss = self.router.load_balancing_loss(logits, idx)

        elif self.routing == "expert_choice":
            scores, idx, logits = self.router(x)

            out = torch.zeros_like(flat_x)
            for e in range(self.n_experts):
                expert_tokens = idx[:, e]
                expert_scores = scores[:, e]
                expert_out = self.experts[e](flat_x[expert_tokens])
                out.index_add_(0, expert_tokens, expert_out * expert_scores.unsqueeze(-1))

            aux_loss = self.router.load_balancing_loss(logits)

        return out.view(B, T, D), aux_loss
