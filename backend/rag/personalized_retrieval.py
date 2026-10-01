import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

import chromadb

from backend.rag.embeddings import create_embeddings
from backend.rag.eligibility import get_candidate_schemes


# -----------------------------------------
# ChromaDB setup
# -----------------------------------------

CHROMA_PATH = BASE_DIR / "data" / "chroma"

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_collection(
    name="yojana_schemes"
)


# -----------------------------------------
# Personalized search
# -----------------------------------------

def personalized_search(
    user_profile,
    query,
    top_k=5
):

    # Get schemes that are not explicitly
    # ruled out by the user's profile
    candidates = get_candidate_schemes(
        user_profile
    )

    # Get valid scheme IDs
    candidate_ids = [
        str(candidate["scheme_id"])
        for candidate in candidates
        if candidate.get("scheme_id") is not None
    ]

    # No candidate schemes
    if not candidate_ids:
        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }

    # Create embedding for user's question
    query_embedding = create_embeddings(
        [query]
    )[0]

    # Search only among personalized candidates
    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=min(
            top_k,
            len(candidate_ids)
        ),
        where={
            "scheme_id": {
                "$in": candidate_ids
            }
        }
    )

    return results


# -----------------------------------------
# Direct testing
# -----------------------------------------

if __name__ == "__main__":

    user_profile = {
        "age": 21,
        "state": "Telangana",
        "occupation": "Student",
        "income": 300000,
        "gender": "Male",
        "social_category": "General"
    }

    query = "What scholarship schemes are available for me?"

    print("\nPersonalized retrieval test")
    print("=" * 70)

    results = personalized_search(
        user_profile,
        query,
        top_k=5
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    print(
        "\nRetrieved schemes:",
        len(documents)
    )

    for i, metadata in enumerate(metadatas):

        print(
            "\n",
            i + 1,
            ".",
            metadata.get(
                "scheme_name",
                "Unknown scheme"
            )
        )

        print(
            "State:",
            metadata.get("state", "")
        )

        print(
            "Category:",
            metadata.get("category", "")
        )