"""Clean final architecture comparison using library models."""
import time, sys, math
import torch, torch.nn as nn, torch.nn.functional as F
import torch.optim as optim

sys.path.insert(0, "src")
from troiani.models import TroianiConfig, TroianiForCausalLM

VOCAB = 50032
B, T = 2, 1024
STEPS = 20


def benchmark(tag, model_fn):
    print(f"\n{'='*60}")
    print(f"  {tag}")
    print(f"{'='*60}")
    torch.cuda.reset_peak_memory_stats()

    model = model_fn().cuda()
    total = sum(p.numel() for p in model.parameters())
    print(f"  Params: {total/1e6:.1f}M")

    opt = optim.AdamW(model.parameters(), lr=3e-4)
    x = torch.randint(0, VOCAB, (B, T), device="cuda")
    y = torch.randint(0, VOCAB, (B, T), device="cuda")

    for _ in range(5):
        _, _, loss = model(x, labels=y) if hasattr(model, 'model') else (model(x), 0, F.cross_entropy(model(x).view(-1, VOCAB), y.view(-1)))
        if isinstance(loss, tuple): _, _, loss = loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step(); opt.zero_grad()

    torch.cuda.synchronize()
    torch.cuda.reset_peak_memory_stats()

    t0 = time.time()
    losses = []
    for i in range(STEPS):
        if hasattr(model, 'model'):  # TroianiForCausalLM
            _, _, loss = model(x, labels=y)
        else:
            logits = model(x)
            loss = F.cross_entropy(logits.view(-1, VOCAB), y.view(-1))
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step(); opt.zero_grad()
        losses.append(loss.item())
    torch.cuda.synchronize()

    elapsed = time.time() - t0
    peak = torch.cuda.max_memory_allocated()
    tok_s = B * T * STEPS / elapsed
    losses = [l for l in losses if not math.isnan(l)]
    print(f"  Throughput: {tok_s:.0f} tok/s  |  Mem: {peak/1e9:.2f}GB")
    print(f"  Loss: {losses[0]:.1f} → {losses[-1]:.1f} (Δ={losses[0]-losses[-1]:.1f})")
    del model, opt
    return tag, total, tok_s, peak, losses[0], losses[-1]


def main():
    results = []

    # 1. TroianiForCausalLM (GQA + MoE, Expert Choice)
    cfg1 = TroianiConfig()
    results.append(benchmark("GQA+MoE-6E EC (library)", lambda: TroianiForCausalLM(cfg1)))

    # 2. TroianiForCausalLM with Top-2
    cfg2 = TroianiConfig(routing="top2")
    results.append(benchmark("GQA+MoE-6E Top-2 (library)", lambda: TroianiForCausalLM(cfg2)))

    # Summary
    print(f"\n{'='*90}")
    print(f"{'Architecture':<35s} {'Params':>8s} {'tok/s':>10s} {'Mem':>8s} {'Loss Δ':>8s}")
    print(f"{'-'*35} {'-'*8} {'-'*10} {'-'*8} {'-'*8}")
    for tag, total, tok_s, peak, ls, le in results:
        print(f"{tag:<35s} {total/1e6:>7.1f}M {tok_s:>10.0f} {peak/1e9:>7.2f}GB {ls-le:>8.1f}")


if __name__ == "__main__":
    main()
