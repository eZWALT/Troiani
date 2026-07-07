"""Compare Top-2 vs Expert Choice routing convergence."""
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from troiani.models.moe import MoELayer

torch.manual_seed(42)


class MoETransformer(nn.Module):
    def __init__(self, d_model: int, n_experts: int, hidden: int, routing: str, vocab: int = 1024):
        super().__init__()
        self.embed = nn.Embedding(vocab, d_model)
        self.moe = MoELayer(d_model, hidden, n_experts, routing=routing)
        self.norm = nn.RMSNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab, bias=False)
        self.embed.weight = self.lm_head.weight

    def forward(self, x):
        h = self.embed(x)
        h, aux = self.moe(h)
        h = self.norm(h)
        logits = self.lm_head(h)
        return logits, aux


def expert_utilization(model, vocab=1024):
    device = next(model.parameters()).device
    model.eval()
    x = torch.randint(0, vocab, (4, 128), device=device)
    with torch.no_grad():
        h = model.embed(x)
        if model.moe.routing == "top2":
            _, idx, _ = model.moe.router(h)
            counts = F.one_hot(idx, model.moe.n_experts).float().sum(dim=(0, 1, 2))
        else:
            _, idx, _ = model.moe.router(h)
            counts = torch.zeros(model.moe.n_experts, device=device)
            for e in range(model.moe.n_experts):
                counts[e] = idx[:, e].unique().numel()
    return counts / counts.sum()


def train_step(model, opt, x, y, aux_coeff=0.01):
    model.train()
    logits, aux_loss = model(x)
    ce = F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
    loss = ce + aux_coeff * aux_loss
    opt.zero_grad()
    loss.backward()
    opt.step()
    return ce.item(), aux_loss.item()


d_model = 256
n_experts = 4
hidden = 768
steps = 500
vocab = 1024
lr = 3e-4
aux_coeff = 0.01
device = "cuda"

results = {}
for routing in ["top2", "expert_choice"]:
    print(f"\n{'='*60}")
    print(f"Training MoE with {routing} routing")
    print(f"{'='*60}")

    model = MoETransformer(d_model, n_experts, hidden, routing).to(device)
    opt = optim.AdamW(model.parameters(), lr=lr)

    ce_vals, aux_vals = [], []
    t0 = time.time()

    for step in range(steps):
        x = torch.randint(0, vocab, (4, 128), device=device)
        y = torch.randint(0, vocab, (4, 128), device=device)
        ce, aux = train_step(model, opt, x, y, aux_coeff)

        if step % 50 == 0 or step == steps - 1:
            elapsed = time.time() - t0
            util = expert_utilization(model, vocab)
            print(f"  step {step:>4d} | ce={ce:.3f} | aux={aux:.5f} | util={[f'{u:.2f}' for u in util.tolist()]} | {elapsed:.1f}s")
            ce_vals.append(ce)
            aux_vals.append(aux)

    total = time.time() - t0
    util = expert_utilization(model, vocab)
    print(f"\n  Final: ce={ce_vals[-1]:.3f} | util={[f'{u:.2f}' for u in util.tolist()]} | {total:.1f}s total")
    results[routing] = dict(ce=ce_vals, aux=aux_vals, time=total, util=util)

print(f"\n{'='*60}")
print("COMPARISON")
print(f"{'='*60}")
print(f"{'':>15s} {'Top-2':>10s} {'ExpertChoice':>15s}")
print(f"{'Final CE':>15s} {results['top2']['ce'][-1]:>10.3f} {results['expert_choice']['ce'][-1]:>15.3f}")
print(f"{'Time':>15s} {results['top2']['time']:>10.1f}s {results['expert_choice']['time']:>15.1f}s")
for i in range(n_experts):
    t2u = results['top2']['util'][i].item()
    ecu = results['expert_choice']['util'][i].item()
    print(f"{'Expert '+str(i)+' util':>15s} {t2u:>10.3f} {ecu:>15.3f}")
