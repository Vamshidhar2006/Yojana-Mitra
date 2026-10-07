from backend.yojanaLM.retrieval.answer import yojana_answer


def chatbot_response(query: str):
    """
    YojanaLM chatbot bridge.

    Takes a plain-text query and returns ONLY the
    final natural-language answer.
    """

    if not query or not query.strip():
        return "Please enter a question."

    try:
        result = yojana_answer(
            query=query.strip(),
            top_k=3
        )

        # answer.py returns a dictionary containing:
        # {
        #     "query": ...,
        #     "answer": ...,
        #     "retrieval": ...
        # }
        #
        # The API must expose only the "answer" field.

        if isinstance(result, dict):
            answer = result.get("answer", "")
        else:
            answer = str(result)

        if not answer or not str(answer).strip():
            return "I couldn't find any relevant government schemes."

        return str(answer).strip()

    except Exception as e:

        import traceback

        print("\n========== YOJANALM ERROR ==========")
        print(repr(e))
        traceback.print_exc()
        print("====================================\n")

        return "Sorry, I couldn't process your question right now."