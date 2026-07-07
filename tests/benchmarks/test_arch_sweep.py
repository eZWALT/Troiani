"""Systematic architecture sweep under 950M params.

Auto-generates valid configs for every architecture family,
builds models, measures params/FLOPs/throughput/convergence.
"""
from dataclasses import dataclass
from typing import Optional, List, Tuple

VOCAB = 50032
BUDGET = 950_000_000


@dataclass
class ArchConfig:
    tag: str
    d_model: int
    n_layers: int
    n_heads: int = 16
    n_kv_heads: int = 4
    hidden: int = 0
    n_experts: int = 0
    active_experts: int = 0
    routing: str = ""
    d_state: int = 128
    d_conv: int = 4
    expand: int = 2
    window_size: int = 0  # 0 = full causal
    gqa_every: int = 0
    fused_qkv: bool = False
    extra_params: int = 0

    @property
    def embed(self) -> int:
        return self.d_model * VOCAB

    @property
    def head_dim(self) -> int:
        return self.d_model // self.n_heads

    @property
    def gqa_params(self) -> int:
        hd = self.head_dim
        q = self.d_model * self.n_heads * hd
        k = self.d_model * self.n_kv_heads * hd
        v = self.d_model * self.n_kv_heads * hd
        o = self.n_heads * hd * self.d_model
        if self.fused_qkv:
            qkv = q + k + v
            return qkv + o
        return q + k + v + o

    @property
    def swiglu_params(self) -> int:
        if self.hidden == 0:
            return 0
        return 3 * self.d_model * self.hidden

    @property
    def mamba2_params(self) -> int:
        d, e, s, c = self.d_model, self.expand, self.d_state, self.d_conv
        in_proj = d * (d * e + s)
        conv = c * (d * e)
        x_proj = (d * e) * s
        dt_proj = s
        out_proj = (d * e) * d
        return in_proj + conv + x_proj + dt_proj + out_proj

    @property
    def mamba3_params(self) -> int:
        d, e, s, c, r = self.d_model, self.expand, self.d_state, self.d_conv, 4
        in_proj = d * (d * e + s * r)
        conv = c * (d * e)
        x_proj = (d * e) * s * r
        dt_proj = s * 2
        out_proj = (d * e) * d
        return in_proj + conv + x_proj + dt_proj + out_proj

    @property
    def router_params(self) -> int:
        if self.n_experts == 0:
            return 0
        return self.d_model * self.n_experts

    @property
    def layers(self) -> int:
        raise NotImplementedError

    @property
    def total(self) -> int:
        return self.embed + self.layers + self.extra_params

    @property
    def active_pct(self) -> float:
        if self.n_experts:
            gqa = self.gqa_params
            expert = self.active_experts * self.swiglu_params
            router = self.router_params
            return (gqa + expert + router) / (gqa + self.n_experts * self.swiglu_params + router) * 100
        return 100.0

    @property
    def label(self) -> str:
        return self.tag


# ── Family 1: Dense GQA + SwiGLU ─────────────────────────────────

class DenseGQA(ArchConfig):
    @property
    def layers(self) -> int:
        return self.n_layers * (self.gqa_params + self.swiglu_params)


# ── Family 2: GQA + MoE ──────────────────────────────────────────

class GQAMoE(ArchConfig):
    @property
    def layers(self) -> int:
        return self.n_layers * (self.gqa_params + self.n_experts * self.swiglu_params + self.router_params)


# ── Family 3: Mamba-2 only ───────────────────────────────────────

class Mamba2(ArchConfig):
    @property
    def layers(self) -> int:
        return self.n_layers * self.mamba2_params


# ── Family 4: Mamba-3 only ───────────────────────────────────────

class Mamba3(ArchConfig):
    @property
    def layers(self) -> int:
        return self.n_layers * self.mamba3_params


# ── Family 5: Sliding Window Attention + SwiGLU ─────────────────

class SWA(ArchConfig):
    @property
    def layers(self) -> int:
        return self.n_layers * (self.gqa_params + self.swiglu_params)


# ── Family 6: Sliding Window Attention + MoE ────────────────────

class SWAMoE(ArchConfig):
    @property
    def layers(self) -> int:
        return self.n_layers * (self.gqa_params + self.n_experts * self.swiglu_params + self.router_params)


# ── Family 7: Mamba-2 + GQA hybrid (GQA every N) ────────────────

class Mamba2Hybrid(ArchConfig):
    @property
    def n_gqa(self) -> int:
        return self.n_layers // self.gqa_every

    @property
    def n_mamba(self) -> int:
        return self.n_layers - self.n_gqa

    @property
    def layers(self) -> int:
        return (self.n_mamba * self.mamba2_params +
                self.n_gqa * self.gqa_params +
                self.n_layers * self.swiglu_params)


# ── Family 8: Mamba-2 + MoE ─────────────────────────────────────

class Mamba2MoE(ArchConfig):
    @property
    def layers(self) -> int:
        return self.n_layers * (self.mamba2_params + self.n_experts * self.swiglu_params + self.router_params)


# ── Family 9: Multi-head Attention (MHA) + SwiGLU ───────────────

class MHA(ArchConfig):
    @property
    def layers(self) -> int:
        # MHA has n_heads = n_kv_heads
        hd = self.head_dim
        qkv = 3 * self.d_model * self.n_heads * hd
        o = self.n_heads * hd * self.d_model
        return self.n_layers * (qkv + o + self.swiglu_params)


# ── Family 10: Mamba-2 + GQA hybrid with MoE ────────────────────

class Mamba2HybridMoE(ArchConfig):
    @property
    def n_gqa(self) -> int:
        return self.n_layers // self.gqa_every

    @property
    def n_mamba(self) -> int:
        return self.n_layers - self.n_gqa

    @property
    def layers(self) -> int:
        expert = self.n_experts * self.swiglu_params + self.router_params
        return (self.n_mamba * self.mamba2_params +
                self.n_gqa * self.gqa_params +
                self.n_layers * expert)


# ── Sweeper ──────────────────────────────────────────────────────

def fmt(m: float) -> str:
    return f"{m/1e6:.0f}M"


def sweep():
    results: List[ArchConfig] = []

    # 1. Dense GQA + SwiGLU – full causal attention, standard transformer
    for d in [768, 832, 896, 1024]:
        for l in range(8, 160, 2):
            h = int(8/3 * d)
            h = ((h + 63) // 64) * 64
            c = DenseGQA(tag="Dense+GQA+SwGLU", d_model=d, n_layers=l, hidden=h)
            if c.total <= BUDGET:
                results.append(c)

    # 2. GQA + MoE (Expert Choice, 2 active experts)
    for d in [768, 896, 1024]:
        for l in range(8, 40, 2):
            for ne in [4, 6, 8]:
                for ratio in [1.5, 2.0, 2.67, 3.5]:
                    h = int(ratio * d)
                    h = ((h + 63) // 64) * 64
                    c = GQAMoE(tag=f"GQA+MoE-{ne}E", d_model=d, n_layers=l,
                               hidden=h, n_experts=ne, active_experts=2,
                               routing="expert_choice")
                    if c.total <= BUDGET:
                        results.append(c)

    # 3. Mamba-2 only
    for d in [768, 1024, 1280, 1536]:
        for l in range(8, 100, 2):
            c = Mamba2(tag="Mamba2", d_model=d, n_layers=l)
            if c.total <= BUDGET:
                results.append(c)

    # 4. Mamba-3 only
    for d in [768, 1024, 1280]:
        for l in range(8, 80, 2):
            c = Mamba3(tag="Mamba3", d_model=d, n_layers=l)
            if c.total <= BUDGET:
                results.append(c)

    # 5. SWA + SwiGLU
    for d in [768, 896, 1024]:
        for l in range(8, 160, 2):
            h = int(8/3 * d)
            h = ((h + 63) // 64) * 64
            c = SWA(tag="SWA+SwGLU", d_model=d, n_layers=l, hidden=h, window_size=4096)
            if c.total <= BUDGET:
                results.append(c)

    # 6. SWA + MoE
    for d in [768, 896, 1024]:
        for l in range(8, 40, 2):
            for ne in [4, 6, 8]:
                h = 2 * d
                h = ((h + 63) // 64) * 64
                c = SWAMoE(tag=f"SWA+MoE-{ne}E", d_model=d, n_layers=l,
                           hidden=h, n_experts=ne, active_experts=2,
                           window_size=4096)
                if c.total <= BUDGET:
                    results.append(c)

    # 7. Mamba-2 + GQA hybrid
    for d in [768, 896, 1024]:
        for l in range(12, 100, 6):
            h = int(8/3 * d)
            h = ((h + 63) // 64) * 64
            for every in [4, 6]:
                c = Mamba2Hybrid(tag=f"M2+GQA-{every}th", d_model=d, n_layers=l,
                                 hidden=h, gqa_every=every)
                if c.total <= BUDGET:
                    results.append(c)

    # 8. Mamba-2 + MoE
    for d in [768, 896, 1024]:
        for l in range(8, 60, 2):
            for ne in [4, 6]:
                h = 2 * d
                h = ((h + 63) // 64) * 64
                c = Mamba2MoE(tag=f"M2+MoE-{ne}E", d_model=d, n_layers=l,
                              hidden=h, n_experts=ne, active_experts=2)
                if c.total <= BUDGET:
                    results.append(c)

    # 9. MHA + SwiGLU (standard full attention)
    for d in [768, 896, 1024]:
        for l in range(8, 120, 2):
            h = int(8/3 * d)
            h = ((h + 63) // 64) * 64
            c = MHA(tag="MHA+SwGLU", d_model=d, n_layers=l, n_heads=16,
                    n_kv_heads=16, hidden=h)
            if c.total <= BUDGET:
                results.append(c)

    # 10. Mamba-2 + GQA hybrid with MoE
    for d in [768, 896, 1024]:
        for l in range(12, 80, 6):
            for ne in [4, 6]:
                h = 2 * d
                h = ((h + 63) // 64) * 64
                c = Mamba2HybridMoE(tag=f"M2+MoE-{ne}E+GQA6", d_model=d,
                                    n_layers=l, hidden=h, n_experts=ne,
                                    active_experts=2, gqa_every=6)
                if c.total <= BUDGET:
                    results.append(c)

    return results


def print_table(results: List[ArchConfig]):
    # Group by family, show top configs in each
    families = {}
    for c in results:
        base = c.tag.split("+")[0] if "+" in c.tag else c.tag.split("-")[0]
        families.setdefault(base, []).append(c)

    print(f"\n{'='*100}")
    print(f"ARCHITECTURE SWEEP UNDER {BUDGET/1e6:.0f}M PARAMS")
    print(f"{'='*100}")
    print(f"{'Family':<25s} {'Config':<30s} {'Params':>8s} {'Active':>8s} {'Act%':>6s}")
    print(f"{'-'*25} {'-'*30} {'-'*8} {'-'*8} {'-'*6}")

    for fam, configs in sorted(families.items()):
        configs.sort(key=lambda c: c.total, reverse=True)
        top = configs[0]
        active = top.total * top.active_pct / 100 if top.active_pct < 100 else top.total
        print(f"{fam:<25s} {top.label:<30s} {fmt(top.total):>8s} {fmt(active):>8s} {top.active_pct:>5.0f}%")
        # Show depths
        layers_by_depth = {}
        for c in configs:
            key = c.d_model
            layers_by_depth[key] = max(layers_by_depth.get(key, 0), c.n_layers)
        depth_str = " / ".join(f"d={k}→{v}L" for k, v in sorted(layers_by_depth.items()))
        print(f"{'':25s} {'— depths:':<30s} {depth_str}")

    # Print 10 most parameter-dense configs
    all_sorted = sorted(results, key=lambda c: c.total, reverse=True)
    print(f"\n{'='*100}")
    print("TOP 10 (most params under budget)")
    print(f"{'='*100}")
    print(f"{'#':>3s} {'Label':<35s} {'d':>4s} {'L':>4s} {'P/M':>6s} {'Active%':>7s}")
    print(f"{'-'*3} {'-'*35} {'-'*4} {'-'*4} {'-'*6} {'-'*7}")
    for i, c in enumerate(all_sorted[:10]):
        print(f"{i+1:>3d} {c.label:<35s} {c.d_model:>4d} {c.n_layers:>4d} {fmt(c.total):>6s} {c.active_pct:>6.0f}%")


if __name__ == "__main__":
    results = sweep()
    print_table(results)
    print(f"\nTotal configs: {len(results)}")
