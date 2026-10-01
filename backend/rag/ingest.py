import pandas as pd
import chromadb
from pathlib import Path

from embeddings import create_embeddings


BASE_DIR = Path(__file__).resolve().parents[2]

CSV_PATH = BASE_DIR / "data" / "csv" / "yojana_mitra_master.csv"
CHROMA_PATH = BASE_DIR / "data" / "chroma"

df = pd.read_csv(CSV_PATH)

print("Total schemes:", len(df))

# Remove rows without a document
df = df[df["document"].notna()].copy()

documents = df["document"].tolist()

print("Creating embeddings...")

embeddings = create_embeddings(documents)

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="yojana_schemes"
)

# Chroma IDs must be strings
ids = df["scheme_id"].astype(str).tolist()

# Keep metadata simple and Chroma-compatible
metadatas = []

for _, row in df.iterrows():

    metadata = {
        "scheme_name": str(row["scheme_name"]),
        "state": str(row["state"]) if pd.notna(row["state"]) else "",
        "category": str(row["category"]) if pd.notna(row["category"]) else "",
        "occupation": str(row["occupation"]) if pd.notna(row["occupation"]) else "",
        "gender": str(row["gender"]) if pd.notna(row["gender"]) else "",
        "social_category": str(row["social_category"]) if pd.notna(row["social_category"]) else "",
        "official_source_url": str(row["official_source_url"]) if pd.notna(row["official_source_url"]) else ""
    }

    metadatas.append(metadata)


collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)

print("Successfully stored schemes in ChromaDB.")
print("Total stored:", collection.count())