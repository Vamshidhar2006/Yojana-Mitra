import math
import torch
import torch.nn as nn


class CausalSelfAttention(nn.Module):

    def __init__(
        self,
        d_model,
        n_heads,
        context_length,
        dropout
    ):
        super().__init__()

        assert d_model % n_heads == 0

        self.n_heads = n_heads
        self.head_dim = d_model // n_heads

        self.q_proj = nn.Linear(
            d_model,
            d_model
        )

        self.k_proj = nn.Linear(
            d_model,
            d_model
        )

        self.v_proj = nn.Linear(
            d_model,
            d_model
        )

        self.out_proj = nn.Linear(
            d_model,
            d_model
        )

        self.attn_dropout = nn.Dropout(dropout)
        self.resid_dropout = nn.Dropout(dropout)

        mask = torch.tril(
            torch.ones(
                context_length,
                context_length
            )
        ).view(
            1,
            1,
            context_length,
            context_length
        )

        self.register_buffer(
            "mask",
            mask
        )

    def forward(self, x):

        B, T, C = x.shape

        q = self.q_proj(x)
        k = self.k_proj(x)
        v = self.v_proj(x)

        q = q.view(
            B,
            T,
            self.n_heads,
            self.head_dim
        ).transpose(1, 2)

        k = k.view(
            B,
            T,
            self.n_heads,
            self.head_dim
        ).transpose(1, 2)

        v = v.view(
            B,
            T,
            self.n_heads,
            self.head_dim
        ).transpose(1, 2)

        attention = (
            q @ k.transpose(-2, -1)
        ) / math.sqrt(self.head_dim)

        attention = attention.masked_fill(
            self.mask[:, :, :T, :T] == 0,
            float("-inf")
        )

        attention = torch.softmax(
            attention,
            dim=-1
        )

        attention = self.attn_dropout(
            attention
        )

        y = attention @ v

        y = y.transpose(
            1,
            2
        ).contiguous().view(
            B,
            T,
            C
        )

        y = self.out_proj(y)

        y = self.resid_dropout(y)

        return y


class FeedForward(nn.Module):

    def __init__(
        self,
        d_model,
        ffn_dim,
        dropout
    ):
        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(
                d_model,
                ffn_dim
            ),

            nn.GELU(),

            nn.Linear(
                ffn_dim,
                d_model
            ),

            nn.Dropout(
                dropout
            )
        )

    def forward(self, x):
        return self.network(x)


class TransformerBlock(nn.Module):

    def __init__(
        self,
        d_model,
        n_heads,
        ffn_dim,
        context_length,
        dropout
    ):
        super().__init__()

        self.ln1 = nn.LayerNorm(d_model)

        self.attention = CausalSelfAttention(
            d_model,
            n_heads,
            context_length,
            dropout
        )

        self.ln2 = nn.LayerNorm(d_model)

        self.ffn = FeedForward(
            d_model,
            ffn_dim,
            dropout
        )

    def forward(self, x):

        x = x + self.attention(
            self.ln1(x)
        )

        x = x + self.ffn(
            self.ln2(x)
        )

        return x


class YojanaLM(nn.Module):

    def __init__(
        self,
        vocab_size=16000,
        d_model=256,
        n_heads=8,
        n_layers=8,
        ffn_dim=1024,
        context_length=512,
        dropout=0.1
    ):
        super().__init__()

        self.token_embedding = nn.Embedding(
            vocab_size,
            d_model
        )

        self.position_embedding = nn.Embedding(
            context_length,
            d_model
        )

        self.blocks = nn.ModuleList([

            TransformerBlock(
                d_model,
                n_heads,
                ffn_dim,
                context_length,
                dropout
            )

            for _ in range(n_layers)
        ])

        self.ln_f = nn.LayerNorm(d_model)

        self.lm_head = nn.Linear(
            d_model,
            vocab_size,
            bias=False
        )

        # Weight tying
        self.lm_head.weight = self.token_embedding.weight

        self.context_length = context_length

    def forward(self, idx):

        B, T = idx.shape

        if T > self.context_length:
            raise ValueError(
                f"Input length {T} exceeds "
                f"context length {self.context_length}"
            )

        positions = torch.arange(
            T,
            device=idx.device
        )

        x = (
            self.token_embedding(idx)
            +
            self.position_embedding(positions)
        )

        for block in self.blocks:
            x = block(x)

        x = self.ln_f(x)

        logits = self.lm_head(x)

        return logits