"""Debug MoE NaN — identify source of NaN in GQA+MoE model."""
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

device = torch.device("cuda")
V, B, T = 50032, 1, 256


class RMSNorm(nn.Module):
    def __init__(self, d): super().__init__(); self.w = nn.Parameter(torch.ones(d))
    def forward(self, x): rms = x.pow(2).mean(-1,keepdim=True).add(1e-6).sqrt(); return x / rms * self.w


class SwiGLU(nn.Module):
    def __init__(self, d, h): super().__init__(); self.g=nn.Linear(d,h,bias=False); self.u=nn.Linear(d,h,bias=False); self.d=nn.Linear(h,d,bias=False)
    def forward(self, x): return self.d(F.silu(self.g(x))*self.u(x))


class GQALayer(nn.Module):
    def __init__(self, d, nh, nkv):
        super().__init__(); self.nh,self.nkv,self.hd=nh,nkv,d//nh
        self.wq=nn.Linear(d,nh*(d//nh),bias=False); self.wk=nn.Linear(d,nkv*(d//nh),bias=False)
        self.wv=nn.Linear(d,nkv*(d//nh),bias=False); self.wo=nn.Linear(nh*(d//nh),d,bias=False)
        self.freqs=None
    def forward(self, x, mask=None):
        B,T,D=x.shape; hd=self.hd
        q=self.wq(x).view(B,T,self.nh,hd).transpose(1,2); k=self.wk(x).view(B,T,self.nkv,hd).transpose(1,2); v=self.wv(x).view(B,T,self.nkv,hd).transpose(1,2)
        g=self.nh//self.nkv
        if g>1: k=k.repeat_interleave(g,dim=1); v=v.repeat_interleave(g,dim=1)
        out=F.scaled_dot_product_attention(q,k,v,is_causal=True)
        out=out.transpose(1,2).contiguous().view(B,T,D)
        return self.wo(out)


class MoEBlock(nn.Module):
    def __init__(self, d, nh, nkv, ne, h):
        super().__init__()
        self.an=RMSNorm(d); self.attn=GQALayer(d,nh,nkv)
        self.fn=RMSNorm(d); self.ne=ne; self.h=h
        self.router=nn.Linear(d,ne,bias=False)
        self.experts=nn.ModuleList([SwiGLU(d,h) for _ in range(ne)])

    def forward(self, x):
        x = x + self.attn(self.an(x))
        r = x; flat = r.view(-1, r.size(-1))
        logits = self.router(flat)
        scores = F.softmax(logits.float(), dim=-1).to(logits.dtype)
        k = int(r.size(0) * r.size(1) * 1.25 / self.ne)
        topk_scores, topk_idx = scores.t().topk(k, dim=1)
        out = torch.zeros_like(flat)
        for e in range(self.ne):
            sel = topk_idx[e]; w = topk_scores[e].unsqueeze(-1)
            expert_out = self.experts[e](flat[sel])
            if torch.isnan(expert_out).any():
                print(f"  NaN in expert {e} output! sel range=[{sel.min().item()},{sel.max().item()}] out of {flat.size(0)}")
                return None
            out.index_add_(0, sel, expert_out * w)
        return x + out.view(r.shape)


class Model(nn.Module):
    def __init__(self, vocab, d, blocks):
        super().__init__()
        self.embed=nn.Embedding(vocab,d); self.blocks=nn.ModuleList(blocks)
        self.norm=RMSNorm(d); self.head=nn.Linear(d,vocab,bias=False)
        self.head.weight=self.embed.weight

    def forward(self, x):
        h=self.embed(x)
        for b in self.blocks:
            h=b(h)
            if h is None: return None
        h=self.norm(h)
        return self.head(h)


for d in [256, 512, 768, 1024]:
    for ne in [4, 6]:
        for cap in [1.0, 1.25, 1.5]:
            L = 4
            print(f"\nTesting d={d}, ne={ne}, cap={cap}, L={L}...")
            model = Model(V, d, [MoEBlock(d, 8, 2, ne, 2*d) for _ in range(L)]).to(device)
            opt = optim.AdamW(model.parameters(), lr=1e-4)
            x = torch.randint(0, min(V, 4096), (B, T), device=device)
            y = torch.randint(0, min(V, 4096), (B, T), device=device)
            nan = False
            for step in range(10):
                logits = model(x)
                if logits is None:
                    print(f"  NaN at step {step}!")
                    nan = True; break
                loss = F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
                if torch.isnan(loss):
                    print(f"  NaN loss at step {step}!")
                    nan = True; break
                opt.zero_grad(); loss.backward(); opt.step()
            if not nan:
                print(f"  OK — final loss={loss.item():.3f}")
            del model, opt; torch.cuda.empty_cache()
