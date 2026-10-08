from .engine import yojana_query_v32
import re


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(value):
    if value is None:
        return ""

    value = str(value).strip()

    if value.lower() in {
        "",
        "nan",
        "none",
        "null",
        "n/a",
        "na",
    }:
        return ""

    return value


def clean_sentence(value):
    value = clean_text(value)

    if not value:
        return ""

    value = value.replace("**", "")
    value = value.replace("__", "")
    value = value.replace('"""', '"')

    # Remove accidental wrapping quotes
    if len(value) >= 2:
        if (
            (value.startswith('"') and value.endswith('"'))
            or
            (value.startswith("'") and value.endswith("'"))
        ):
            value = value[1:-1].strip()

    # Normalize whitespace
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def normalize_name(value):
    value = clean_text(value)

    if not value:
        return ""

    value = value.lower()

    # Normalize punctuation
    value = value.replace("&", " and ")
    value = value.replace("-", " ")
    value = value.replace("_", " ")
    value = value.replace("/", " ")

    # Remove common punctuation
    value = re.sub(r"[^\w\s]", " ", value)

    # Normalize whitespace
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def normalize_label(value):
    value = clean_text(value)

    if not value:
        return ""

    value = value.replace("_", " ")
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def format_documents(value):
    value = clean_text(value)

    if not value:
        return ""

    documents = []

    for item in value.split(";"):
        item = normalize_label(item)

        if item:
            documents.append(item)

    return ", ".join(documents)


# ============================================================
# PROFILE FORMATTING
# ============================================================

def format_profile(profile):
    profile = profile or {}

    parts = []

    occupation = clean_text(
        profile.get("occupation")
    )

    state = clean_text(
        profile.get("state")
    )

    age = profile.get("age")

    gender = clean_text(
        profile.get("gender")
    )

    social_category = clean_text(
        profile.get("social_category")
    )

    income = profile.get("income")

    if occupation:
        parts.append(
            f"a {occupation.lower()}"
        )

    if state:
        parts.append(
            f"from {state.title()}"
        )

    if age is not None:
        parts.append(
            f"aged {age}"
        )

    if gender:
        parts.append(
            gender.lower()
        )

    if social_category:
        parts.append(
            f"in the {social_category.upper()} category"
        )

    if not parts:
        return "your profile"

    if len(parts) == 1:
        return parts[0]

    if len(parts) == 2:
        return f"{parts[0]} {parts[1]}"

    return (
        ", ".join(parts[:-1])
        + " and "
        + parts[-1]
    )


# ============================================================
# QUERY INTENT
# ============================================================

def detect_answer_style(query):

    q = normalize_name(query)

    # --------------------------------------------------------
    # WHY NOT ELIGIBLE
    # --------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "why am i not eligible",
            "why am i ineligible",
            "why am i not qualify",
            "why do i not qualify",
            "why dont i qualify",
            "why cant i get",
            "why can i not get",
            "why am i rejected",
            "why was i rejected",
        ]
    ):
        return "why_not_eligible"

    # --------------------------------------------------------
    # ELIGIBILITY
    # --------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "am i eligible",
            "am i qualify",
            "do i qualify",
            "can i get",
            "can i apply",
            "eligibility",
            "eligible for",
            "qualify for",
        ]
    ):
        return "eligibility"

    # --------------------------------------------------------
    # BENEFITS
    # --------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "what are the benefits",
            "what benefits",
            "benefits of",
            "what does it provide",
            "what does this provide",
            "what do i get",
            "what will i get",
            "how much does it provide",
            "how much money",
            "financial assistance",
            "financial support",
            "what is the use",
            "use of",
        ]
    ):
        return "benefits"

    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "what documents",
            "documents required",
            "required documents",
            "documents do i need",
            "which documents",
            "what paperwork",
        ]
    ):
        return "documents"

    # --------------------------------------------------------
    # APPLICATION
    # --------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "how do i apply",
            "how can i apply",
            "where can i apply",
            "where do i apply",
            "how to apply",
            "application process",
            "how can someone apply",
        ]
    ):
        return "application"

    # --------------------------------------------------------
    # SCHOLARSHIPS
    # --------------------------------------------------------

    if any(
        word in q.split()
        for word in [
            "scholarship",
            "scholarships",
        ]
    ):
        return "scholarships"

    # --------------------------------------------------------
    # OVERVIEW
    # --------------------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "tell me about",
            "what is",
            "what's",
            "explain",
            "give me information",
            "information about",
            "details about",
            "about this scheme",
            "about the scheme",
        ]
    ):
        return "overview"

    # --------------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------------

    return "recommendations"


# ============================================================
# EXACT SCHEME NAME EXTRACTION
# ============================================================

def extract_scheme_phrase(query):

    q = clean_text(query)

    patterns = [
        r"tell me about (.+)",
        r"what are the benefits of (.+)",
        r"what benefits does (.+) provide",
        r"what benefits does (.+) have",
        r"what documents are required for (.+)",
        r"what documents do i need for (.+)",
        r"what is the eligibility for (.+)",
        r"am i eligible for (.+)",
        r"do i qualify for (.+)",
        r"how do i apply for (.+)",
        r"how can i apply for (.+)",
        r"what is (.+)",
        r"what's (.+)",
        r"why am i not eligible for (.+)",
        r"why am i ineligible for (.+)",
        r"what is the use of (.+)",
        r"use of (.+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            q,
            flags=re.IGNORECASE
        )

        if match:
            phrase = match.group(1).strip()

            # Remove trailing question punctuation
            phrase = phrase.rstrip(" ?.")

            if phrase:
                return phrase

    return ""


def find_scheme_in_results(
    query,
    retrieval
):
    """
    Looks for a scheme explicitly mentioned by the user
    among the schemes returned by retrieval.

    This does NOT invent or substitute another scheme.
    """

    phrase = extract_scheme_phrase(query)

    if not phrase:
        return None

    target = normalize_name(phrase)

    results = retrieval.get(
        "results",
        []
    )

    exact_candidates = []

    for item in results:

        name = clean_text(
            item.get("scheme_name")
        )

        if not name:
            continue

        normalized = normalize_name(name)

        if normalized == target:
            return item

        if target in normalized or normalized in target:
            exact_candidates.append(item)

    if len(exact_candidates) == 1:
        return exact_candidates[0]

    return None


# ============================================================
# ELIGIBILITY HELPERS
# ============================================================

def eligibility_label(key):

    labels = {
        "state": "state",
        "occupation": "occupation",
        "gender": "gender",
        "age": "age",
        "income": "income",
        "social_category": "social category",
        "disability": "disability requirement",
        "bpl": "BPL requirement",
        "residence": "residence requirement",
    }

    return labels.get(
        key,
        normalize_label(key).lower()
    )


def get_checks(checks):

    if not isinstance(checks, dict):
        return {}

    return checks


def matching_conditions(checks):

    matched = []

    for key, value in get_checks(checks).items():

        if value == "eligible":
            matched.append(
                eligibility_label(key)
            )

    return matched


def failed_conditions(checks):

    failed = []

    for key, value in get_checks(checks).items():

        if value in {
            "not_eligible",
            "ineligible",
            "failed",
            "mismatch",
        }:
            failed.append(
                eligibility_label(key)
            )

    return failed


def unknown_conditions(checks):

    unknown = []

    for key, value in get_checks(checks).items():

        if value in {
            "unknown",
            "not_verified",
            "partially_verified",
        }:
            unknown.append(
                eligibility_label(key)
            )

    return unknown


def join_conditions(items):

    if not items:
        return ""

    if len(items) == 1:
        return items[0]

    if len(items) == 2:
        return f"{items[0]} and {items[1]}"

    return (
        ", ".join(items[:-1])
        + " and "
        + items[-1]
    )


def eligibility_sentence(
    status,
    checks=None
):

    checks = get_checks(checks)

    matched = matching_conditions(checks)
    failed = failed_conditions(checks)

    if status == "eligible":

        if matched:

            return (
                "Your "
                + join_conditions(matched)
                + " match the eligibility information "
                "currently available for this scheme."
            )

        return (
            "Your profile appears to meet the eligibility "
            "information currently available for this scheme."
        )

    if status == "partially_verified":

        if matched:

            return (
                "Your "
                + join_conditions(matched)
                + " match the available information, "
                "but some additional conditions still need "
                "to be verified."
            )

        return (
            "This scheme may be suitable for your profile, "
            "but the available information is not sufficient "
            "to confirm every eligibility condition."
        )

    if status == "not_eligible":

        if failed:

            return (
                "You do not appear to meet the recorded "
                + join_conditions(failed)
                + " requirement"
                + ("s" if len(failed) > 1 else "")
                + " for this scheme."
            )

        return (
            "Based on the eligibility information currently "
            "available, your profile does not meet the "
            "recorded requirements for this scheme."
        )

    return (
        "The available information is not sufficient to "
        "confirm your eligibility for this scheme."
    )


# ============================================================
# EXACT SCHEME ANSWERS
# ============================================================

def format_exact_scheme(
    retrieval,
    style
):

    scheme = clean_text(
        retrieval.get("scheme")
    )

    row = retrieval.get(
        "source_row",
        {}
    )

    if not isinstance(row, dict):
        row = {}

    status = retrieval.get(
        "eligibility",
        "unknown"
    )

    checks = retrieval.get(
        "eligibility_checks",
        {}
    )

    benefits = clean_sentence(
        row.get("benefits")
    )

    description = clean_sentence(
        row.get("description")
    )

    documents = format_documents(
        row.get("required_documents")
    )

    application = clean_sentence(
        row.get("application_process")
    )

    state = clean_sentence(
        row.get("state")
    )

    official_source = clean_text(
        row.get("official_source_url")
    )

    # --------------------------------------------------------
    # BENEFITS
    # --------------------------------------------------------

    if style == "benefits":

        if not benefits:

            return (
                f"I couldn't find specific benefit information "
                f"for {scheme} in the current scheme database."
            )

        return (
            f"{scheme}\n\n"
            f"{benefits}"
        )

    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    if style == "documents":

        if not documents:

            return (
                f"The current scheme database does not list "
                f"specific required documents for {scheme}."
            )

        return (
            f"{scheme}\n\n"
            f"To apply for this scheme, the available records "
            f"list these documents:\n\n"
            f"{documents}."
        )

    # --------------------------------------------------------
    # APPLICATION
    # --------------------------------------------------------

    if style == "application":

        if not application:

            if official_source:

                return (
                    f"I couldn't find the application process "
                    f"for {scheme} in the current database.\n\n"
                    f"You can check the official source:\n"
                    f"{official_source}"
                )

            return (
                f"The application process for {scheme} is not "
                "available in the current scheme database."
            )

        return (
            f"{scheme}\n\n"
            f"Application process\n"
            f"{application}"
        )

    # --------------------------------------------------------
    # ELIGIBILITY
    # --------------------------------------------------------

    if style in {
        "eligibility",
        "why_not_eligible",
    }:

        lines = [
            scheme,
            "",
            "Eligibility",
            eligibility_sentence(
                status,
                checks
            ),
        ]

        if benefits:
            lines.extend([
                "",
                f"Benefits: {benefits}"
            ])

        if documents:
            lines.extend([
                "",
                f"Documents: {documents}"
            ])

        if official_source:
            lines.extend([
                "",
                f"Official source: {official_source}"
            ])

        return "\n".join(lines)

    # --------------------------------------------------------
    # OVERVIEW
    # --------------------------------------------------------

    if style == "overview":

        lines = [
            scheme
        ]

        if description:
            lines.extend([
                "",
                description
            ])
        elif benefits:
            lines.extend([
                "",
                benefits
            ])

        if state:
            lines.extend([
                "",
                f"Coverage: {state}"
            ])

        if benefits and description:
            lines.extend([
                "",
                f"Benefits: {benefits}"
            ])

        if documents:
            lines.extend([
                "",
                f"Documents: {documents}"
            ])

        if application:
            lines.extend([
                "",
                f"Application process: {application}"
            ])

        if official_source:
            lines.extend([
                "",
                f"Official source: {official_source}"
            ])

        return "\n".join(lines)

    # Fallback
    return format_exact_scheme(
        retrieval,
        "overview"
    )


# ============================================================
# CATEGORY / PERSONALIZED RESULT FORMATTING
# ============================================================

def format_scheme_item(
    item,
    index,
    style
):

    scheme = clean_text(
        item.get("scheme_name")
    )

    description = clean_sentence(
        item.get("description")
    )

    benefits = clean_sentence(
        item.get("benefits")
    )

    documents = format_documents(
        item.get("documents")
    )

    state = clean_text(
        item.get("state")
    )

    occupation = normalize_label(
        item.get("occupation")
    )

    status = item.get(
        "eligibility",
        "unknown"
    )

    checks = item.get(
        "eligibility_checks",
        {}
    )

    official_source = clean_text(
        item.get("official_source_url")
    )

    lines = [
        f"{index}. {scheme}"
    ]

    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

    if description:
        lines.extend([
            "",
            description
        ])

    elif state or occupation:

        coverage = []

        if state:
            coverage.append(state)

        if occupation:
            coverage.append(occupation)

        if coverage:
            lines.extend([
                "",
                "Coverage: "
                + " and ".join(coverage)
            ])

    # --------------------------------------------------------
    # ELIGIBILITY
    # --------------------------------------------------------

    if status == "eligible":

        lines.extend([
            "",
            "Eligibility: "
            + eligibility_sentence(
                status,
                checks
            )
        ])

    elif status == "partially_verified":

        lines.extend([
            "",
            "Eligibility: "
            + eligibility_sentence(
                status,
                checks
            )
        ])

    elif status == "not_eligible":

        lines.extend([
            "",
            "Eligibility: "
            + eligibility_sentence(
                status,
                checks
            )
        ])

    # --------------------------------------------------------
    # BENEFITS
    # --------------------------------------------------------

    if benefits:
        lines.extend([
            "",
            f"Benefits: {benefits}"
        ])

    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    if documents:
        lines.extend([
            "",
            f"Documents: {documents}"
        ])

    # --------------------------------------------------------
    # SOURCE
    # --------------------------------------------------------

    if official_source:
        lines.extend([
            "",
            f"Official source: {official_source}"
        ])

    return "\n".join(lines)


# ============================================================
# CATEGORY INTRODUCTIONS
# ============================================================

def category_intro(
    style,
    count
):

    if style == "scholarships":

        return (
            f"I found {count} scholarship"
            + ("." if count == 1 else "s that may be relevant to you.")
        )

    if style == "recommendations":

        return (
            f"I found {count} government scheme"
            + (
                " that may be relevant to your profile."
                if count == 1
                else "s that may be relevant to your profile."
            )
        )

    return (
        f"I found {count} government scheme"
        + (
            " that may be relevant to your profile."
            if count == 1
            else "s that may be relevant to your profile."
        )
    )


# ============================================================
# NORMAL SEARCH ANSWER
# ============================================================

def format_normal_search(
    retrieval,
    selected,
    style
):

    profile = retrieval.get(
        "profile",
        {}
    )

    profile_text = format_profile(
        profile
    )

    count = len(selected)

    lines = [
        category_intro(
            style,
            count
        ),
        "",
        f"Your profile: {profile_text}.",
        "",
    ]

    for index, item in enumerate(
        selected,
        start=1
    ):

        lines.append(
            format_scheme_item(
                item,
                index,
                style
            )
        )

        if index != len(selected):
            lines.append("")

    lines.extend([
        "",
        "These results are based on the current scheme "
        "database. Some schemes may have additional "
        "conditions that are not fully captured in the "
        "available records."
    ])

    return "\n".join(lines)


# ============================================================
# NO EXACT MATCH
# ============================================================

def no_exact_scheme_answer(
    query,
    retrieval
):

    phrase = extract_scheme_phrase(
        query
    )

    if phrase:

        return (
            f"I couldn't find an exact match for "
            f"\"{phrase}\" in the current scheme database.\n\n"
            "I don't want to give you information about a "
            "different scheme just because its name is similar."
        )

    return (
        "I couldn't find a sufficiently relevant scheme in "
        "the current database for that question."
    )


# ============================================================
# MAIN YOJANA ANSWER
# ============================================================

def yojana_answer(
    query,
    top_k=3
):

    query = clean_text(
        query
    )

    if not query:

        return {
            "query": query,
            "answer": "Please enter a question.",
            "retrieval": {}
        }

    # --------------------------------------------------------
    # RETRIEVAL
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # ANSWER STYLE
    # --------------------------------------------------------

    style = detect_answer_style(
        query
    )

    # --------------------------------------------------------
    # EXACT SCHEME FROM RETRIEVAL
    # --------------------------------------------------------

    exact_item = find_scheme_in_results(
        query,
        retrieval
    )

    # --------------------------------------------------------
    # EXACT SCHEME FIELD
    # --------------------------------------------------------

    if retrieval_type == "exact_scheme_field":

        return {
            "query": query,
            "answer": format_exact_scheme(
                retrieval,
                style
            ),
            "retrieval": retrieval
        }

    # --------------------------------------------------------
    # EXACT SCHEME
    # --------------------------------------------------------

    if retrieval_type == "exact_scheme":

        return {
            "query": query,
            "answer": format_exact_scheme(
                retrieval,
                style
            ),
            "retrieval": retrieval
        }

    # --------------------------------------------------------
    # IF USER CLEARLY NAMED A SCHEME AND WE FOUND IT
    # --------------------------------------------------------

    if exact_item is not None:

        # Convert the result into an exact-scheme style
        # structure without changing the retrieval engine.

        exact_retrieval = dict(retrieval)

        exact_retrieval["scheme"] = exact_item.get(
            "scheme_name",
            ""
        )

        exact_retrieval["source_row"] = {
            "scheme_name": exact_item.get(
                "scheme_name"
            ),
            "description": exact_item.get(
                "description"
            ),
            "benefits": exact_item.get(
                "benefits"
            ),
            "required_documents": exact_item.get(
                "documents"
            ),
            "application_process": exact_item.get(
                "application_process"
            ),
            "state": exact_item.get(
                "state"
            ),
            "official_source_url": exact_item.get(
                "official_source_url"
            ),
        }

        exact_retrieval["eligibility"] = exact_item.get(
            "eligibility",
            "unknown"
        )

        exact_retrieval["eligibility_checks"] = (
            exact_item.get(
                "eligibility_checks",
                {}
            )
        )

        return {
            "query": query,
            "answer": format_exact_scheme(
                exact_retrieval,
                style
            ),
            "retrieval": retrieval
        }

    # --------------------------------------------------------
    # EXPLICIT SCHEME QUESTION BUT NO MATCH
    # --------------------------------------------------------

    explicit_scheme_phrase = extract_scheme_phrase(
        query
    )

    if (
        explicit_scheme_phrase
        and style in {
            "overview",
            "benefits",
            "documents",
            "application",
            "eligibility",
            "why_not_eligible",
        }
    ):

        return {
            "query": query,
            "answer": no_exact_scheme_answer(
                query,
                retrieval
            ),
            "retrieval": retrieval
        }

    # --------------------------------------------------------
    # INSUFFICIENT PROFILE
    # --------------------------------------------------------

    if retrieval_type == "insufficient_profile":

        return {
            "query": query,
            "answer": (
                "I can help you find government schemes, but "
                "I need a little more information to personalize "
                "the results. You can provide details such as "
                "your state, occupation, age, gender, income "
                "or social category."
            ),
            "retrieval": retrieval
        }

    # --------------------------------------------------------
    # NORMAL SEARCH
    # --------------------------------------------------------

    results = retrieval.get(
        "results",
        []
    )

    if not results:

        return {
            "query": query,
            "answer": (
                "I couldn't find a suitable government scheme "
                "in the current database based on the information "
                "available for your profile."
            ),
            "retrieval": retrieval
        }

    selected = results[
        :top_k
    ]

    answer = format_normal_search(
        retrieval,
        selected,
        style
    )

    return {
        "query": query,
        "answer": answer,
        "retrieval": retrieval
    }


# ============================================================
# LOCAL TESTING
# ============================================================

if __name__ == "__main__":

    queries = [

        "Tell me about PM-KISAN",

        "What are the benefits of PM-KISAN?",

        "What documents are required for PM-KISAN?",

        "Am I eligible for PM-KISAN?",

        "Why am I not eligible for PM-KISAN?",

        "Tell me about Rythu Bandhu",

        "What are the benefits of Rythu Bandhu?",

        "Tell me about PM Kisan Maandhan",

        "Tell me about Deen Dayal SPARSH Yojana",

        "What schemes are available for disabled people?",

        "What scholarships can I get as a student?",

        "What schemes are available for farmers?",

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
        print(
            result["answer"]
        )