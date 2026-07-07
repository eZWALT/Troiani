"""GPU benchmark: multiple architectures under 950M.
Run on Atlas (A100) to compare throughput, memory, convergence."""
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# ─── helpers ───────────────────────────────────────────────────────

device = torch.device("cuda")


def rms_norm(x, weight, eps=1e-6):
    rms = x.pow(2).mean(-1, keepdim=True).add(eps).sqrt()
    return x / rms * weight


class RMSNorm(nn.Module):
    def __init__(self, d): super().__init__(); self.w = nn.Parameter(torch.ones(d))
    def forward(self, x): return rms_norm(x, self.w)


def precompute_freqs(dim, T, theta=10000.0):
    freqs = 1.0 / (theta ** (torch.arange(0, dim, 2, device=device).float() / dim))
    t = torch.arange(T, device=device).float()
    freqs = torch.outer(t, freqs)
    return torch.stack([torch.cos(freqs), torch.sin(freqs)], dim=-1)


def apply_rotary(x, freqs_cis):
    x_2d = x.float().reshape(*x.shape[:-1], -1, 2)
    x_cos, x_sin = x_2d[..., 0], x_2d[..., 1]
    f = freqs_cis[:x.shape[-3], :, :].unsqueeze(1)
    rc, rs = f[..., 0], f[..., 1]
    out = torch.stack([x_cos * rc - x_sin * rs, x_cos * rs + x_sin * rc], dim=-1)
    return out.flatten(-2).to(x.dtype)


class SwiGLU(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.g = nn.Linear(d, h, bias=False)
        self.u = nn.Linear(d, h, bias=False)
        self.d = nn.Linear(h, d, bias=False)
    def forward(self, x):
        return self.d(F.silu(self.g(x)) * self.u(x))


# ─── Architectures ─────────────────────────────────────────────────

class GQALayer(nn.Module):
    def __init__(self, d, nh, nkv, ws=0):
        super().__init__()
        self.nh, self.nkv, self.hd, self.ws = nh, nkv, d // nh, ws
        self.wq = nn.Linear(d, nh * (d // nh), bias=False)
        self.wk = nn.Linear(d, nkv * (d // nh), bias=False)
        self.wv = nn.Linear(d, nkv * (d // nh), bias=False)
        self.wo = nn.Linear(nh * (d // nh), d, bias=False)
        self.freqs = None

    def forward(self, x, mask=None):
        B, T, D = x.shape
        hd = self.hd
        q = self.wq(x).view(B, T, self.nh, hd).transpose(1, 2)
        k = self.wk(x).view(B, T, self.nkv, hd).transpose(1, 2)
        v = self.wv(x).view(B, T, self.nkv, hd).transpose(1, 2)
        if self.freqs is None or self.freqs.size(0) < T:
            self.freqs = precompute_freqs(hd, max(T, 8192))
        q = apply_rotary(q, self.freqs)
        k = apply_rotary(k, self.freqs)
        g = self.nh // self.nkv
        if g > 1:
            k = k.repeat_interleave(g, dim=1)
            v = v.repeat_interleave(g, dim=1)
        out = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        out = out.transpose(1, 2).contiguous().view(B, T, D)
        return self.wo(out)


class DenseGQABlock(nn.Module):
    def __init__(self, d, nh, nkv, h, ws=0):
        super().__init__()
        self.an = RMSNorm(d)
        self.attn = GQALayer(d, nh, nkv, ws)
        self.fn = RMSNorm(d)
        self.ffn = SwiGLU(d, h)

    def forward(self, x, mask=None):
        x = x + self.attn(self.an(x), mask)
        x = x + self.ffn(self.fn(x))
        return x


class MoEBlock(nn.Module):
    def __init__(self, d, nh, nkv, ne, h, ws=0):
        super().__init__()
        self.an = RMSNorm(d); self.attn = GQALayer(d, nh, nkv, ws)
        self.fn = RMSNorm(d)
        self.ne = ne; self.h = h
        self.router = nn.Linear(d, ne, bias=False)
        nn.init.normal_(self.router.weight, std=0.02)
        self.experts = nn.ModuleList([SwiGLU(d, h) for _ in range(ne)])

    def forward(self, x, mask=None):
        x = x + self.attn(self.an(x), mask)
        r = x.clone()
        B, T, D = r.shape
        flat = r.view(-1, D)

        # Top-2 routing (simpler, more stable)
        logits = self.router(flat)
        scores = F.softmax(logits.float(), dim=-1).to(logits.dtype)
        top2_scores, top2_idx = scores.topk(2, dim=-1)

        out = torch.zeros_like(flat)
        for e in range(self.ne):
            token_mask = (top2_idx == e).any(dim=-1)
            if not token_mask.any(): continue
            sel_scores = top2_scores[token_mask]
            sel_idx = top2_idx[token_mask]
            e_mask = (sel_idx == e)
            weights = sel_scores[e_mask].unsqueeze(-1)
            expert_out = self.experts[e](flat[token_mask])
            if torch.isnan(expert_out).any():
                print(f"NaN in expert {e} at layer input")
                return None
            out[token_mask] += expert_out * weights

        result = x + out.view(B, T, D)
        if torch.isnan(result).any():
            print("NaN in MoE output")
            return None
        return result


class Mamba2Block(nn.Module):
    def __init__(self, d, expand=2, d_state=128, d_conv=4):
        super().__init__()
        from mamba_ssm import Mamba2
        self.mamba = Mamba2(d_model=d, d_state=d_state, d_conv=d_conv, expand=expand)
        self.norm = RMSNorm(d)

    def forward(self, x, **kw):
        return x + self.mamba(self.norm(x))


class Mamba3Block(nn.Module):
    def __init__(self, d, expand=2, d_state=128, d_conv=4):
        super().__init__()
        from mamba_ssm import Mamba3
        self.mamba = Mamba3(d_model=d, d_state=d_state, d_conv=d_conv, expand=expand, is_mimo=False)
        self.norm = RMSNorm(d)

    def forward(self, x, **kw):
        return x + self.mamba(self.norm(x))


class Model(nn.Module):
    def __init__(self, vocab, d, blocks):
        super().__init__()
        self.embed = nn.Embedding(vocab, d)
        self.blocks = nn.ModuleList(blocks)
        self.norm = RMSNorm(d)
        self.head = nn.Linear(d, vocab, bias=False)
        self.head.weight = self.embed.weight

    def forward(self, x):
        h = self.embed(x)
        for b in self.blocks:
            h = b(h)
            if h is None: return None
        h = self.norm(h)
        return self.head(h)


# ── Configs ────────────────────────────────────────────────────────

def build_configs():
    V = 50032
    return [
        ("Dense-GQA-80L",    1024, 80, lambda d: [DenseGQABlock(d, 16, 4, int(8/3*d)) for _ in range(80)]),
        ("Mamba2-d1024-86L", 1024, 86, lambda d: [Mamba2Block(d, d_state=64) for _ in range(86)]),
        ("Mamba2-d1024-140L",1024, 140, lambda d: [Mamba2Block(d, d_state=64) for _ in range(140)]),
        ("Mamba3-d1024-74L", 1024, 74, lambda d: [Mamba3Block(d, d_state=64) for _ in range(74)]),
        ("GQA+MoE-6E-22L",   1024, 22, lambda d: [MoEBlock(d, 16, 4, 6, 2*d) for _ in range(22)]),
        ("GQA+MoE-4E-32L",   896,  32, lambda d: [MoEBlock(d, 16, 4, 4, 2*d) for _ in range(32)]),
    ]


def main():
    V = 50032
    B, T = 2, 1024
    steps = 20

    results = []
    for tag, d, L, build_fn in build_configs():
        print(f"\n{'='*60}")
        print(f"Benchmarking: {tag} (d={d}, L={L})")
        print(f"{'='*60}")
        torch.cuda.reset_peak_memory_stats()

        model = Model(V, d, build_fn(d)).to(device)
        total = sum(p.numel() for p in model.parameters())
        print(f"  Params: {total/1e6:.1f}M")

        opt = optim.AdamW(model.parameters(), lr=3e-4)
        x = torch.randint(0, V, (B, T), device=device)
        y = torch.randint(0, V, (B, T), device=device)

        try:
            # Warmup
            for _ in range(5):
                logits = model(x)
                loss = F.cross_entropy(logits.view(-1, V), y.view(-1))
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                opt.step(); opt.zero_grad()

            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()

            # Benchmark throughput
            t0 = time.time()
            losses = []
            for i in range(steps):
                logits = model(x)
                loss = F.cross_entropy(logits.view(-1, V), y.view(-1))
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                opt.step(); opt.zero_grad()
                losses.append(loss.item())
            torch.cuda.synchronize()
        except (torch.OutOfMemoryError, RuntimeError, ValueError) as e:
            print(f"  FAILED: {e}")
            del model, opt
            torch.cuda.empty_cache()
            continue
        elapsed = time.time() - t0
        peak_mem = torch.cuda.max_memory_allocated()

        tok_s = B * T * steps / elapsed
        print(f"  Throughput: {tok_s:.0f} tok/s ({elapsed:.1f}s for {steps} steps)")
        print(f"  Peak mem:   {peak_mem/1e9:.2f} GB")
        print(f"  Loss:       {losses[0]:.3f} → {losses[-1]:.3f} (Δ={losses[0]-losses[-1]:.3f})")

        results.append((tag, total, tok_s, peak_mem, losses[0], losses[-1]))

    # Summary table
    print(f"\n{'='*100}")
    print(f"{'Architecture':<25s} {'Params':>8s} {'tok/s':>10s} {'Mem':>8s} {'Loss start':>10s} {'Loss end':>10s}")
    print(f"{'-'*25} {'-'*8} {'-'*10} {'-'*8} {'-'*10} {'-'*10}")
    for tag, total, tok_s, peak_mem, ls, le in results:
        print(f"{tag:<25s} {total/1e6:>7.1f}M {tok_s:>10.0f} {peak_mem/1e9:>7.2f}GB {ls:>10.3f} {le:>10.3f}")


if __name__ == "__main__":
    main()
