from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-m3"

model = SentenceTransformer(MODEL_NAME)

# Keep the input length manageable for CPU processing
model.max_seq_length = 512


def create_embeddings(texts):
    return model.encode(
        texts,
        batch_size=4,
        normalize_embeddings=True,
        show_progress_bar=True
    )