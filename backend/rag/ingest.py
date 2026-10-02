import pandas as pd
import chromadb
from pathlib import Path

from embeddings import create_embeddings


BASE_DIR = Path(__file__).resolve().parents[2]

CSV_PATH = BASE_DIR / "data" / "csv" / "yojana_mitra_master.csv"
CHROMA_PATH = BASE_DIR / "data" / "chroma"


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv(CSV_PATH)

print("Total schemes:", len(df))


# --------------------------------------------------
# Remove rows without documents
# --------------------------------------------------

df = df[df["document"].notna()].copy()

documents = df["document"].tolist()

print("Documents available:", len(documents))


# --------------------------------------------------
# Create embeddings
# --------------------------------------------------

print("Creating embeddings with MiniLM...")

embeddings = create_embeddings(documents)

print("Embeddings created.")


# --------------------------------------------------
# Connect to ChromaDB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)


# --------------------------------------------------
# Remove old collection
# --------------------------------------------------

try:

    client.delete_collection(
        name="yojana_schemes"
    )

    print("Old Chroma collection deleted.")

except Exception:

    print("No old Chroma collection found.")


# --------------------------------------------------
# Create new collection
# --------------------------------------------------

collection = client.create_collection(
    name="yojana_schemes"
)


# --------------------------------------------------
# Create scheme IDs
# --------------------------------------------------

ids = (
    df["scheme_id"]
    .astype(str)
    .tolist()
)


# --------------------------------------------------
# Create metadata
# --------------------------------------------------

metadatas = []

for _, row in df.iterrows():

    metadata = {

        "scheme_id": str(row["scheme_id"]),

        "scheme_name": str(
            row["scheme_name"]
        ),

        "state": (
            str(row["state"])
            if pd.notna(row["state"])
            else ""
        ),

        "category": (
            str(row["category"])
            if pd.notna(row["category"])
            else ""
        ),

        "occupation": (
            str(row["occupation"])
            if pd.notna(row["occupation"])
            else ""
        ),

        "gender": (
            str(row["gender"])
            if pd.notna(row["gender"])
            else ""
        ),

        "social_category": (
            str(row["social_category"])
            if pd.notna(row["social_category"])
            else ""
        ),

        "official_source_url": (
            str(row["official_source_url"])
            if pd.notna(
                row["official_source_url"]
            )
            else ""
        )
    }

    metadatas.append(metadata)


# --------------------------------------------------
# Store everything in ChromaDB
# --------------------------------------------------

collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)


# --------------------------------------------------
# Verify
# --------------------------------------------------

print(
    "Successfully stored schemes in ChromaDB."
)

print(
    "Total stored:",
    collection.count()
)