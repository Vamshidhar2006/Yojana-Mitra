import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

from api.gemini_llm import client
from backend.rag.personalized_retrieval import personalized_search


def generate_answer(
    user_profile,
    question,
    language="English",
    top_k=5
):

    # -----------------------------------------
    # Personalized retrieval
    # -----------------------------------------

    results = personalized_search(
        user_profile,
        question,
        top_k=top_k
    )

    # -----------------------------------------
    # No results found
    # -----------------------------------------

    if not results["documents"][0]:

        if language == "English":
            return (
                "I couldn't find any relevant government "
                "schemes in the available scheme information."
            )

        return (
            "I couldn't find any relevant government "
            "schemes in the available scheme information."
        )

    # -----------------------------------------
    # Build retrieved context
    # -----------------------------------------

    context_parts = []

    for i, document in enumerate(
        results["documents"][0]
    ):

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

        context = f"""
Scheme {i + 1}

Scheme Name: {scheme_name}

State: {state}

Category: {category}

Official Source: {source}

Information:
{document}
"""

        context_parts.append(context)

    context = "\n".join(context_parts)

    # -----------------------------------------
    # Gemini prompt
    # -----------------------------------------

    prompt = f"""
You are Yojana Mitra, a helpful and conversational
government scheme information assistant.

Your purpose is to help users understand Indian government
schemes using ONLY the scheme information provided below.

USER PROFILE:
{user_profile}

USER QUESTION:
{question}

RESPONSE LANGUAGE:
{language}

RETRIEVED SCHEME INFORMATION:
{context}

IMPORTANT RULES:

1. Use only the retrieved scheme information.

2. Do not invent schemes, eligibility requirements,
benefits, application procedures, qualifications, or URLs.

3. Never say the user is definitely eligible unless the
retrieved information clearly establishes this.

4. If an eligibility condition is missing, say that it
needs to be verified.

5. Consider relevant conditions such as age, state,
residence, income, gender, social category, disability,
education, occupation, and examination requirements when
they are present in the retrieved information.

6. Do not treat unknown conditions as satisfied.

7. If the user asks about a specific scheme and that scheme
is not present in the retrieved information, clearly say
that the scheme could not be found in the available data.

8. Do not replace a missing requested scheme with unrelated
schemes unless the user asks for alternatives.

9. Answer the user's actual question first.

10. Use natural conversational language.

11. Avoid repeating the same headings such as
"Why it may be relevant",
"Important eligibility conditions",
and "Benefits" for every scheme.

12. Keep the answer reasonably concise.

13. If several schemes are relevant, use a numbered list.

14. Include the official source URL when it is available.

15. Do not expose internal retrieval, embedding, ChromaDB,
metadata, or implementation details.

16. Do not make a definitive eligibility decision.

17. End with a short reminder to verify the latest official
scheme information before applying.

18. Write the ENTIRE answer in the selected response language.

19. Do not switch back to English unless the selected
language is English or a technical term, scheme name,
proper noun, or official URL needs to remain unchanged.

20. The selected response language is:
{language}

21. Do not translate official scheme names unless doing so
would make the answer clearer. Keep official names intact
when appropriate.

ANSWER STYLE:

Write like a helpful government scheme assistant.

For multiple schemes, naturally explain why each may be
relevant, the important conditions, and the main benefit.

For a direct question about one scheme, focus on that scheme.

For eligibility questions, clearly separate:
- conditions that appear to match the user's profile
- conditions that are still unknown
- conditions that need verification

Use phrases appropriate to the selected language.

Do not automatically produce a generic scheme list for
every question.
"""

    # -----------------------------------------
    # Generate answer with Gemini
    # -----------------------------------------

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


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

    question = (
        "What scholarship schemes can I apply for?"
    )

    print("\nGenerating Yojana Mitra response...")
    print("=" * 70)

    answer = generate_answer(
        user_profile=user_profile,
        question=question,
        language="Telugu",
        top_k=5
    )

    print(answer)