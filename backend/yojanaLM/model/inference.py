from pathlib import Path

import torch
import sentencepiece as spm

from .yojana_lm import YojanaLM


# --------------------------------------------------
# PATHS
# --------------------------------------------------

YOJANALM_DIR = Path(__file__).resolve().parent.parent

CHECKPOINT_PATH = (
    YOJANALM_DIR
    / "checkpoints"
    / "yojanalm_stage1_best.pt"
)

TOKENIZER_PATH = (
    YOJANALM_DIR
    / "tokenizer"
    / "yojana_tokenizer.model"
)


# --------------------------------------------------
# DEVICE
# --------------------------------------------------

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


# --------------------------------------------------
# LOAD TOKENIZER
# --------------------------------------------------

tokenizer = spm.SentencePieceProcessor()

if not tokenizer.load(str(TOKENIZER_PATH)):
    raise RuntimeError(
        f"Could not load tokenizer: {TOKENIZER_PATH}"
    )


VOCAB_SIZE = tokenizer.get_piece_size()


# --------------------------------------------------
# CREATE MODEL
# --------------------------------------------------

model = YojanaLM(
    vocab_size=VOCAB_SIZE,
    d_model=256,
    n_heads=8,
    n_layers=8,
    ffn_dim=1024,
    context_length=512,
    dropout=0.1
).to(DEVICE)


# --------------------------------------------------
# LOAD CHECKPOINT
# --------------------------------------------------

checkpoint = torch.load(
    CHECKPOINT_PATH,
    map_location=DEVICE,
    weights_only=False
)

model.load_state_dict(
    checkpoint["model"],
    strict=True
)

model.eval()


print("YojanaLM loaded successfully")
print("Device:", DEVICE)
print("Vocabulary:", VOCAB_SIZE)
print("Checkpoint:", CHECKPOINT_PATH)