from .engine import yojana_query_v32


def clean_text(value):

    if value is None:
        return ""

    value = str(value).strip()

    if value.lower() in [
        "",
        "nan",
        "none",
        "null"
    ]:
        return ""

    return value


def format_documents(value):

    value = clean_text(value)

    if not value:
        return ""

    documents = [
        item.strip()
        for item in value.split(";")
        if item.strip()
    ]

    return ", ".join(
        documents
    )


def format_profile(profile):

    parts = []

    occupation = clean_text(
        profile.get("occupation")
    )

    state = clean_text(
        profile.get("state")
    )

    gender = clean_text(
        profile.get("gender")
    )

    age = profile.get("age")

    social_category = clean_text(
        profile.get("social_category")
    )

    if occupation:

        parts.append(
            f"as a {occupation}"
        )

    if state:

        parts.append(
            f"from {state.title()}"
        )

    if gender:

        parts.append(
            f"who is {gender}"
        )

    if age is not None:

        parts.append(
            f"aged {age}"
        )

    if social_category:

        parts.append(
            f"in the {social_category.upper()} category"
        )

    if not parts:

        return "the information you provided"

    return " ".join(parts)


def eligibility_sentence(
    status,
    checks
):

    checks = checks or {}

    matched = []

    if checks.get("state") == "eligible":
        matched.append("state")

    if checks.get("occupation") == "eligible":
        matched.append("occupation")

    if checks.get("gender") == "eligible":
        matched.append("gender")

    if checks.get("age") == "eligible":
        matched.append("age")

    if checks.get("income") == "eligible":
        matched.append("income")

    if status == "eligible":

        if matched:

            if len(matched) == 1:

                return (
                    f"Your {matched[0]} matches the "
                    "available eligibility information."
                )

            if len(matched) == 2:

                return (
                    f"Your {matched[0]} and "
                    f"{matched[1]} match the "
                    "available eligibility information."
                )

            return (
                "Your "
                + ", ".join(matched[:-1])
                + " and "
                + matched[-1]
                + " match the available "
                "eligibility information."
            )

        return (
            "Your profile matches the available "
            "eligibility information."
        )

    if status == "partially_verified":

        if matched:

            if len(matched) == 1:

                return (
                    f"Your {matched[0]} matches the "
                    "available eligibility information, "
                    "but additional conditions may need "
                    "to be checked."
                )

            if len(matched) == 2:

                return (
                    f"Your {matched[0]} and "
                    f"{matched[1]} match the "
                    "available eligibility information, "
                    "but additional conditions may need "
                    "to be checked."
                )

            return (
                "Your "
                + ", ".join(matched[:-1])
                + " and "
                + matched[-1]
                + " match the available "
                "eligibility information, but "
                "additional conditions may need "
                "to be checked."
            )

        return (
            "The scheme may be relevant to your "
            "profile, but additional conditions may "
            "need to be checked."
        )

    if status == "not_eligible":

        return (
            "The available eligibility information "
            "indicates that your profile does not "
            "match this scheme."
        )

    return (
        "The available information is not sufficient "
        "to fully confirm eligibility."
    )


def format_exact_field(
    retrieval
):

    scheme = clean_text(
        retrieval.get("scheme")
    )

    value = clean_text(
        retrieval.get("answer")
    )

    intent = retrieval.get(
        "intent"
    )

    if intent == "benefits":

        if not value:

            return (
                f"I could not find benefit information "
                f"for {scheme} in the current database."
            )

        return (
            f"The benefits of {scheme} are: "
            f"{value}"
        )

    if intent == "required_documents":

        if not value:

            return (
                f"The current database does not list "
                f"the required documents for {scheme}."
            )

        documents = format_documents(
            value
        )

        return (
            f"The documents required for {scheme} "
            f"are {documents}."
        )

    if intent == "application_process":

        if not value:

            return (
                f"The application process for {scheme} "
                "is not available in the current database."
            )

        return (
            f"The application process for {scheme} "
            f"is: {value}"
        )

    if intent == "eligibility":

        if not value:

            return (
                f"The current database does not contain "
                f"sufficient eligibility information for "
                f"{scheme}."
            )

        return (
            f"The available eligibility information "
            f"for {scheme} is: {value}"
        )

    if intent == "description":

        if not value:

            return (
                f"A description for {scheme} is not "
                "available in the current database."
            )

        return (
            f"{scheme} is described as follows: "
            f"{value}"
        )

    if intent == "state":

        if not value:

            return (
                f"The state information for {scheme} "
                "is not available."
            )

        return (
            f"{scheme} is listed under {value}."
        )

    return value


def format_exact_scheme(
    retrieval
):

    scheme = clean_text(
        retrieval.get("scheme")
    )

    row = retrieval.get(
        "source_row",
        {}
    )

    status = retrieval.get(
        "eligibility",
        "unknown"
    )

    checks = retrieval.get(
        "eligibility_checks",
        {}
    )

    lines = []

    lines.append(
        scheme
    )

    lines.append(
        eligibility_sentence(
            status,
            checks
        )
    )

    benefits = clean_text(
        row.get("benefits")
    )

    if benefits:

        lines.append(
            f"Benefits: {benefits}"
        )

    documents = format_documents(
        row.get(
            "required_documents"
        )
    )

    if documents:

        lines.append(
            f"Required documents: {documents}"
        )

    application = clean_text(
        row.get(
            "application_process"
        )
    )

    if application:

        lines.append(
            f"Application process: {application}"
        )

    official_source = clean_text(
        row.get(
            "official_source_url"
        )
    )

    if official_source:

        lines.append(
            f"Official source: {official_source}"
        )

    return "\n\n".join(
        lines
    )


def format_scheme(
    item
):

    scheme = clean_text(
        item.get("scheme_name")
    )

    state = clean_text(
        item.get("state")
    )

    occupation = clean_text(
        item.get("occupation")
    )

    benefits = clean_text(
        item.get("benefits")
    )

    documents = format_documents(
        item.get("documents")
    )

    status = item.get(
        "eligibility",
        "unknown"
    )

    checks = item.get(
        "eligibility_checks",
        {}
    )

    lines = []

    lines.append(
        scheme
    )

    description_parts = []

    if state:

        description_parts.append(
            f"listed for {state}"
        )

    if occupation:

        occupation_text = (
            occupation.replace(
                "_",
                " "
            )
        )

        description_parts.append(
            f"for {occupation_text}"
        )

    if description_parts:

        lines.append(
            "This scheme is "
            + " and ".join(
                description_parts
            )
            + "."
        )

    lines.append(
        eligibility_sentence(
            status,
            checks
        )
    )

    if benefits:

        lines.append(
            f"Benefits: {benefits}"
        )

    if documents:

        lines.append(
            f"Required documents: {documents}"
        )

    official_source = clean_text(
        item.get(
            "official_source_url"
        )
    )

    if official_source:

        lines.append(
            f"Official source: {official_source}"
        )

    return "\n\n".join(
        lines
    )


def yojana_answer(
    query,
    top_k=3
):

    retrieval = yojana_query_v32(
        query,
        top_k=max(
            12,
            top_k
        )
    )

    retrieval_type = retrieval.get(
        "retrieval_type",
        ""
    )

    # ========================================================
    # INSUFFICIENT PROFILE
    # ========================================================

    if retrieval_type == "insufficient_profile":

        return {
            "query": query,
            "answer": (
                "I can help you find suitable "
                "government schemes. Please provide "
                "at least one detail such as your "
                "state, occupation, age, gender, "
                "income, or social category."
            ),
            "retrieval": retrieval
        }

    # ========================================================
    # EXACT FIELD
    # ========================================================

    if retrieval_type == "exact_scheme_field":

        return {
            "query": query,
            "answer":
                format_exact_field(
                    retrieval
                ),
            "retrieval": retrieval
        }

    # ========================================================
    # EXACT SCHEME
    # ========================================================

    if retrieval_type == "exact_scheme":

        return {
            "query": query,
            "answer":
                format_exact_scheme(
                    retrieval
                ),
            "retrieval": retrieval
        }

    # ========================================================
    # NORMAL SEARCH
    # ========================================================

    results = retrieval.get(
        "results",
        []
    )

    if not results:

        return {
            "query": query,
            "answer": (
                "I couldn't find a suitable "
                "government scheme in the current "
                "database based on the information "
                "you provided."
            ),
            "retrieval": retrieval
        }

    selected = results[:top_k]

    profile = retrieval.get(
        "profile",
        {}
    )

    profile_text = format_profile(
        profile
    )

    if len(selected) == 1:

        intro = (
            f"Based on the information you provided "
            f"({profile_text}), I found one government "
            "scheme that may be relevant to you."
        )

    else:

        intro = (
            f"Based on the information you provided "
            f"({profile_text}), I found {len(selected)} "
            "government schemes that may be relevant "
            "to you."
        )

    scheme_answers = []

    for item in selected:

        scheme_answers.append(
            format_scheme(
                item
            )
        )

    answer = (
        intro
        + "\n\n"
        + "\n\n".join(
            scheme_answers
        )
        + "\n\n"
        + "These results are based on the information "
        + "available in the current scheme database. "
        + "Where some eligibility conditions are "
        + "missing, additional verification may be "
        + "required."
    )

    return {
        "query": query,
        "answer": answer,
        "retrieval": retrieval
    }


if __name__ == "__main__":

    queries = [

        "I am a student from Telangana. What government schemes are available for me?",

        "I'm a farmer from Rajasthan. What government schemes are available?",

        "What government schemes are available for women in Karnataka?",

        "I'm a farmer. What agriculture schemes are available in Telangana?",

        "I am a 25-year-old farmer from Telangana with an income of 3 lakh. What schemes can I get?",

        "I am an SC farmer from Rajasthan. What schemes are available?",

        "What are the benefits of PM KISAN?",

        "What documents are required for PM KISAN?"
    ]

    for query in queries:

        print()
        print("=" * 80)
        print("USER:")
        print(query)

        result = yojana_answer(
            query,
            top_k=3
        )

        print()
        print("CHATBOT:")
        print(result["answer"])