import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from api.gemini_llm import client
from backend.rag.personalized_retrieval import personalized_search
from google.genai import types


def generate_answer(
    user_profile,
    question,
    language="English",
    top_k=3
):
    results = personalized_search(
        user_profile,
        question,
        top_k=top_k
    )

    if not results["documents"][0]:
        if language == "English":
            return (
                "I couldn't find any relevant government "
                "schemes for your question in the available information."
            )

        return (
            "I couldn't find any relevant government "
            "schemes for your question in the available information."
        )

    context_parts = []

    for i, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][i]

        scheme_name = metadata.get(
            "scheme_name",
            ""
        )

        state = metadata.get(
            "state",
            ""
        )

        category = metadata.get(
            "category",
            ""
        )

        source = metadata.get(
            "official_source_url",
            ""
        )

        document = str(document)[:5000]

        context = f"""
Scheme {i + 1}
Name: {scheme_name}
State: {state}
Category: {category}
Official Source: {source}

Information:
{document}
"""

        context_parts.append(context)

    context = "\n".join(context_parts)

    prompt = f"""
You are Yojana Mitra, a helpful government scheme assistant.

Answer the user's question using ONLY the retrieved scheme
information below.

USER PROFILE:
{user_profile}

QUESTION:
{question}

RESPONSE LANGUAGE:
{language}

RETRIEVED INFORMATION:
{context}

RULES:

1. Do not invent schemes, eligibility requirements,
benefits, application procedures, or URLs.

2. Do not claim that the user is definitely eligible
unless the retrieved information clearly proves it.

3. If an eligibility condition is unknown, say that it
needs verification.

4. Answer the user's question directly.

5. Keep the answer concise and useful.

6. If multiple schemes are relevant, use a short numbered list.

7. Include the official source URL when available.

8. Keep official scheme names unchanged.

9. Do not mention ChromaDB, embeddings, retrieval,
internal systems, or implementation details.

10. Write the ENTIRE answer in the selected language.

11. End with a short reminder to verify the latest
official information before applying.

IMPORTANT:
Do not give a generic list if the user asked about
a specific scheme.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=500
        )
    )

    return response.text


if __name__ == "__main__":

    user_profile = {
        "age": 21,
        "state": "Telangana",
        "occupation": "Student",
        "income": 300000,
        "gender": "Male",
        "social_category": "General"
    }

    question = "What scholarship schemes can I apply for?"

    print("\nGenerating Yojana Mitra response...")
    print("=" * 70)

    answer = generate_answer(
        user_profile=user_profile,
        question=question,
        language="English",
        top_k=3
    )

    print(answer)