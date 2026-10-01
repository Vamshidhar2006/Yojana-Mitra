import pandas as pd
import chromadb
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

CSV_PATH = BASE_DIR / "data" / "csv" / "yojana_mitra_master.csv"
CHROMA_PATH = BASE_DIR / "data" / "chroma"

# Load the master dataset
df = pd.read_csv(CSV_PATH)

print("Total schemes in CSV:", len(df))

# Connect to existing ChromaDB
client = chromadb.PersistentClient(path=str(CHROMA_PATH))

collection = client.get_collection(name="yojana_schemes")

print("Schemes currently in ChromaDB:", collection.count())

# Prepare metadata
ids = df["scheme_id"].astype(str).tolist()

metadatas = []

for _, row in df.iterrows():

    metadata = {
        "scheme_id": str(row["scheme_id"]),
        "scheme_name": str(row["scheme_name"]) if pd.notna(row["scheme_name"]) else "",
        "state": str(row["state"]) if pd.notna(row["state"]) else "",
        "central_or_state": str(row["central_or_state"]) if pd.notna(row["central_or_state"]) else "",
        "category": str(row["category"]) if pd.notna(row["category"]) else "",
        "beneficiary_type": str(row["beneficiary_type"]) if pd.notna(row["beneficiary_type"]) else "",
        "occupation": str(row["occupation"]) if pd.notna(row["occupation"]) else "",
        "social_category": str(row["social_category"]) if pd.notna(row["social_category"]) else "",
        "gender": str(row["gender"]) if pd.notna(row["gender"]) else "",

        "min_age": str(row["min_age"]) if pd.notna(row["min_age"]) else "",
        "max_age": str(row["max_age"]) if pd.notna(row["max_age"]) else "",
        "income_limit": str(row["income_limit"]) if pd.notna(row["income_limit"]) else "",

        "disability_required": str(row["disability_required"])
        if pd.notna(row["disability_required"]) else "",

        "bpl_required": str(row["bpl_required"])
        if pd.notna(row["bpl_required"]) else "",

        "residence_requirement": str(row["residence_requirement"])
        if pd.notna(row["residence_requirement"]) else "",

        "eligibility_verified": str(row["eligibility_verified"])
        if pd.notna(row["eligibility_verified"]) else "",

        "data_quality_score": str(row["data_quality_score"])
        if pd.notna(row["data_quality_score"]) else "",

        "official_source_url": str(row["official_source_url"])
        if pd.notna(row["official_source_url"]) else "",

        "application_url": str(row["application_url"])
        if pd.notna(row["application_url"]) else ""
    }

    metadatas.append(metadata)


# Update metadata in batches
BATCH_SIZE = 500

for start in range(0, len(ids), BATCH_SIZE):

    end = min(start + BATCH_SIZE, len(ids))

    collection.update(
        ids=ids[start:end],
        metadatas=metadatas[start:end]
    )

    print(f"Updated {end}/{len(ids)} schemes")


print("\nMetadata update completed successfully.")
print("Total schemes in ChromaDB:", collection.count())