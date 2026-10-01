import chromadb
from embeddings import create_embeddings

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_PATH = BASE_DIR / "data" / "chroma"

# Connect to existing ChromaDB
client = chromadb.PersistentClient(path=str(CHROMA_PATH))

collection = client.get_collection(name="yojana_schemes")


def search_schemes(query, top_k=5):
    # Convert the user query into an embedding
    query_embedding = create_embeddings([query])[0]

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    query = "scholarship schemes for students in Telangana"

    results = search_schemes(query, top_k=5)

    print("\nSearch results:\n")

    for i, document in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]

        print(f"Result {i + 1}")
        print("Scheme:", metadata.get("scheme_name"))
        print("State:", metadata.get("state"))
        print("Category:", metadata.get("category"))
        print("Source:", metadata.get("official_source_url"))
        print("Document:", document[:300], "...")
        print("-" * 70)