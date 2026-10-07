from pathlib import Path
import re
import math
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = BACKEND_DIR.parent

MASTER_CSV = (
    PROJECT_DIR
    / "data"
    / "csv"
    / "yojana_mitra_master.csv"
)


# ============================================================
# LOAD MASTER DATABASE
# ============================================================

master = pd.read_csv(MASTER_CSV)

print(
    f"Master database loaded: {master.shape}"
)


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(value):

    if value is None:
        return ""

    if isinstance(value, float) and math.isnan(value):
        return ""

    value = str(value).lower().strip()

    value = re.sub(
        r"[^a-z0-9₹]+",
        " ",
        value
    )

    return re.sub(
        r"\s+",
        " ",
        value
    ).strip()


# ============================================================
# PROFILE EXTRACTION
# ============================================================

def extract_user_profile_v31(query):

    q = normalize_text(query)

    profile = {
        "state": "",
        "occupation": "",
        "category": "",
        "gender": None,
        "age": None,
        "income": None,
        "social_category": "",
        "disability": None,
        "bpl": None,
        "raw_query": query
    }

    states = [
        "andhra pradesh",
        "arunachal pradesh",
        "assam",
        "bihar",
        "chhattisgarh",
        "goa",
        "gujarat",
        "haryana",
        "himachal pradesh",
        "jharkhand",
        "karnataka",
        "kerala",
        "madhya pradesh",
        "maharashtra",
        "manipur",
        "meghalaya",
        "mizoram",
        "nagaland",
        "odisha",
        "punjab",
        "rajasthan",
        "sikkim",
        "tamil nadu",
        "telangana",
        "tripura",
        "uttar pradesh",
        "uttarakhand",
        "west bengal",
        "delhi",
        "jammu and kashmir",
        "ladakh"
    ]

    occupations = [
        "farmer",
        "farmers",
        "student",
        "students",
        "self employed",
        "self-employed",
        "salaried",
        "worker",
        "workers",
        "daily wage",
        "daily wages",
        "artisan",
        "entrepreneur",
        "fisherman",
        "fishermen",
        "teacher",
        "unemployed"
    ]

    categories = [
        "agriculture",
        "education",
        "health",
        "housing",
        "employment",
        "business",
        "women",
        "minority",
        "disability"
    ]

    social_categories = [
        "sc",
        "st",
        "obc",
        "ebc",
        "general",
        "minority"
    ]

    # ========================================================
    # STATE
    # ========================================================

    for state in states:

        if state in q:

            profile["state"] = state
            break

    # ========================================================
    # OCCUPATION
    # ========================================================

    for occupation in occupations:

        if occupation in q:

            occupation = occupation.replace(
                "self-employed",
                "self_employed"
            )

            occupation = occupation.replace(
                "daily wages",
                "daily_wages"
            )

            occupation = occupation.replace(
                "daily wage",
                "daily_wages"
            )

            if occupation.endswith("s"):
                occupation = occupation[:-1]

            profile["occupation"] = occupation
            break

    # ========================================================
    # CATEGORY
    # ========================================================

    for category in categories:

        if category in q:

            profile["category"] = category
            break

    # ========================================================
    # GENDER
    # ========================================================

    if re.search(
        r"\b(woman|women|female|girl|girls)\b",
        q
    ):

        profile["gender"] = "female"

    elif re.search(
        r"\b(man|men|male|boy|boys)\b",
        q
    ):

        profile["gender"] = "male"

    # ========================================================
    # SOCIAL CATEGORY
    # ========================================================

    for category in social_categories:

        if re.search(
            rf"\b{re.escape(category)}\b",
            q
        ):

            profile["social_category"] = category
            break

    # ========================================================
    # AGE
    # ========================================================

    age_patterns = [

        r"\b(\d{1,3})\s*[- ]?\s*year[- ]?old\b",

        r"\bage\s*(?:is|of)?\s*(\d{1,3})\b",

        r"\baged\s*(\d{1,3})\b"
    ]

    for pattern in age_patterns:

        match = re.search(
            pattern,
            q
        )

        if match:

            profile["age"] = int(
                match.group(1)
            )

            break

    # ========================================================
    # INCOME
    # ========================================================

    income_match = re.search(
        r"(?:income|earn|earning|salary)"
        r".{0,20}?"
        r"(\d+(?:\.\d+)?)\s*"
        r"(lakh|lakhs|l|crore|crores|k)?",
        q
    )

    if income_match:

        number = float(
            income_match.group(1)
        )

        unit = income_match.group(2)

        if unit in [
            "lakh",
            "lakhs",
            "l"
        ]:

            number *= 100000

        elif unit in [
            "crore",
            "crores"
        ]:

            number *= 10000000

        elif unit == "k":

            number *= 1000

        profile["income"] = int(
            number
        )

    if profile["income"] is None:

        income_match = re.search(
            r"(\d+(?:\.\d+)?)\s*"
            r"(lakh|lakhs|l|crore|crores|k)"
            r".{0,15}?"
            r"income",
            q
        )

        if income_match:

            number = float(
                income_match.group(1)
            )

            unit = income_match.group(2)

            if unit in [
                "lakh",
                "lakhs",
                "l"
            ]:

                number *= 100000

            elif unit in [
                "crore",
                "crores"
            ]:

                number *= 10000000

            elif unit == "k":

                number *= 1000

            profile["income"] = int(
                number
            )

    # ========================================================
    # DISABILITY
    # ========================================================

    if re.search(
        r"\b(disabled|disability|person with disability|pwd)\b",
        q
    ):

        profile["disability"] = True

    # ========================================================
    # BPL
    # ========================================================

    if re.search(
        r"\b(bpl|below poverty line)\b",
        q
    ):

        profile["bpl"] = True

    return profile


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(query):

    q = normalize_text(query)

    if any(
        phrase in q
        for phrase in [
            "benefits",
            "benefit",
            "what does",
            "what do i get",
            "how much",
            "amount",
            "financial assistance"
        ]
    ):

        return "benefits"

    if any(
        phrase in q
        for phrase in [
            "documents",
            "document",
            "required documents",
            "what do i need",
            "papers required"
        ]
    ):

        return "required_documents"

    if any(
        phrase in q
        for phrase in [
            "how to apply",
            "application process",
            "apply",
            "where can i apply",
            "how can i apply"
        ]
    ):

        return "application_process"

    if any(
        phrase in q
        for phrase in [
            "eligible",
            "eligibility",
            "can i get",
            "am i eligible",
            "qualify",
            "qualification"
        ]
    ):

        return "eligibility"

    if any(
        phrase in q
        for phrase in [
            "description",
            "what is",
            "tell me about"
        ]
    ):

        return "description"

    if any(
        phrase in q
        for phrase in [
            "state",
            "which state"
        ]
    ):

        return "state"

    return "find_scheme"


# ============================================================
# EXACT SCHEME ALIASES
# ============================================================

SCHEME_ALIASES = {

    "pm kisan":
        "pm kisan samman nidhi",

    "pm-kisan":
        "pm kisan samman nidhi",

    "pm kisan samman nidhi":
        "pm kisan samman nidhi",

    "pm kisan nidhi":
        "pm kisan samman nidhi",

    "pmkisan":
        "pm kisan samman nidhi",

    "kisan samman nidhi":
        "pm kisan samman nidhi"
}


# ============================================================
# EXACT SCHEME FINDER
# ============================================================

def find_exact_scheme(query):

    q = normalize_text(
        query
    )

    normalized_names = (
        master["scheme_name"]
        .fillna("")
        .astype(str)
        .map(normalize_text)
    )

    # ========================================================
    # KNOWN ALIASES
    # ========================================================

    for alias, official_name in SCHEME_ALIASES.items():

        alias_normalized = normalize_text(
            alias
        )

        if alias_normalized not in q:
            continue

        exact_matches = master[
            normalized_names == official_name
        ]

        if len(exact_matches) > 0:

            return exact_matches.iloc[0]

        partial_matches = master[
            normalized_names.str.contains(
                official_name,
                regex=False,
                na=False
            )
        ]

        if len(partial_matches) > 0:

            return partial_matches.iloc[0]

    # ========================================================
    # DIRECT SCHEME NAME MATCH
    # ========================================================

    for idx, scheme_name in normalized_names.items():

        if not scheme_name:
            continue

        if scheme_name in q:

            return master.loc[idx]

    return None


# ============================================================
# VALUE MATCHING
# ============================================================

def value_contains(
    cell,
    values
):

    cell = normalize_text(
        cell
    )

    if not cell:
        return False

    for value in values:

        value = normalize_text(
            value
        )

        if value and value in cell:

            return True

    return False


# ============================================================
# BASE ELIGIBILITY
# ============================================================

def determine_eligibility(
    row,
    states,
    occupations,
    gender,
    age,
    income
):

    checks = {}

    contradictions = []

    row_state = normalize_text(
        row.get(
            "state",
            ""
        )
    )

    row_occupation = normalize_text(
        row.get(
            "occupation",
            ""
        )
    )

    row_gender = normalize_text(
        row.get(
            "gender",
            ""
        )
    )

    # ========================================================
    # STATE
    # ========================================================

    if states:

        if (
            not row_state
            or "all india" in row_state
            or value_contains(
                row_state,
                states
            )
        ):

            checks["state"] = "eligible"

        else:

            checks["state"] = "not_eligible"

            contradictions.append(
                "state"
            )

    else:

        checks["state"] = "unknown"

    # ========================================================
    # OCCUPATION
    # ========================================================

    if occupations:

        occupation_match = False

        for occupation in occupations:

            if value_contains(
                row_occupation,
                [occupation]
            ):

                occupation_match = True
                break

        if (
            occupation_match
            or not row_occupation
            or row_occupation in [
                "all",
                "any",
                "all occupations"
            ]
        ):

            checks["occupation"] = "eligible"

        else:

            checks["occupation"] = "not_eligible"

            contradictions.append(
                "occupation"
            )

    else:

        checks["occupation"] = "unknown"

    # ========================================================
    # GENDER
    # ========================================================

    if gender is not None:

        if (
            not row_gender
            or row_gender in [
                "any",
                "all",
                "both",
                "male female"
            ]
            or gender in row_gender
        ):

            checks["gender"] = "eligible"

        else:

            checks["gender"] = "not_eligible"

            contradictions.append(
                "gender"
            )

    else:

        checks["gender"] = "unknown"

    # ========================================================
    # AGE
    # ========================================================

    min_age = row.get(
        "min_age"
    )

    max_age = row.get(
        "max_age"
    )

    if age is not None:

        age_ok = True

        try:

            if (
                pd.notna(min_age)
                and float(min_age) > age
            ):

                age_ok = False

            if (
                pd.notna(max_age)
                and float(max_age) < age
            ):

                age_ok = False

        except Exception:

            pass

        if age_ok:

            checks["age"] = "eligible"

        else:

            checks["age"] = "not_eligible"

            contradictions.append(
                "age"
            )

    else:

        checks["age"] = "unknown"

    # ========================================================
    # INCOME
    # ========================================================

    income_limit = row.get(
        "income_limit"
    )

    if income is not None:

        if (
            pd.isna(income_limit)
            or str(income_limit).strip() == ""
        ):

            checks["income"] = "eligible"

        else:

            try:

                limit = float(
                    income_limit
                )

                if income <= limit:

                    checks["income"] = "eligible"

                else:

                    checks["income"] = "not_eligible"

                    contradictions.append(
                        "income"
                    )

            except Exception:

                checks["income"] = "unknown"

    else:

        checks["income"] = "unknown"

    # ========================================================
    # RESULT
    # ========================================================

    if contradictions:

        return (
            "not_eligible",
            checks
        )

    known_checks = [
        value
        for value in checks.values()
        if value != "unknown"
    ]

    if known_checks and all(
        value == "eligible"
        for value in known_checks
    ):

        return (
            "eligible",
            checks
        )

    return (
        "unknown",
        checks
    )


# ============================================================
# ADDITIONAL REQUIREMENTS
# ============================================================

def check_additional_requirements_v32(
    row,
    profile
):

    requirements = []

    exclusions = []

    checks = {}

    social_category = normalize_text(
        profile.get(
            "social_category",
            ""
        )
    )

    disability = profile.get(
        "disability"
    )

    bpl = profile.get(
        "bpl"
    )

    row_social = normalize_text(
        row.get(
            "social_category",
            ""
        )
    )

    row_disability = normalize_text(
        row.get(
            "disability_required",
            ""
        )
    )

    row_bpl = normalize_text(
        row.get(
            "bpl_required",
            ""
        )
    )

    # ========================================================
    # SOCIAL CATEGORY
    # ========================================================

    if row_social:

        if social_category:

            if social_category in row_social:

                checks[
                    "social_category"
                ] = "eligible"

            else:

                checks[
                    "social_category"
                ] = "not_eligible"

        else:

            checks[
                "social_category"
            ] = "unknown"

            requirements.append(
                f"Social category may be required: {row_social}"
            )

    # ========================================================
    # DISABILITY
    # ========================================================

    if row_disability:

        required = (
            row_disability
            in [
                "yes",
                "true",
                "required",
                "1"
            ]
        )

        if required:

            if disability is True:

                checks[
                    "disability"
                ] = "eligible"

            elif disability is False:

                checks[
                    "disability"
                ] = "not_eligible"

            else:

                checks[
                    "disability"
                ] = "unknown"

                requirements.append(
                    "Disability status needs verification."
                )

    # ========================================================
    # BPL
    # ========================================================

    if row_bpl:

        required = (
            row_bpl
            in [
                "yes",
                "true",
                "required",
                "1"
            ]
        )

        if required:

            if bpl is True:

                checks[
                    "bpl"
                ] = "eligible"

            elif bpl is False:

                checks[
                    "bpl"
                ] = "not_eligible"

            else:

                checks[
                    "bpl"
                ] = "unknown"

                requirements.append(
                    "BPL status needs verification."
                )

    return (
        requirements,
        exclusions,
        checks
    )


# ============================================================
# FINAL V3.2 ELIGIBILITY
# ============================================================

def determine_eligibility_v32(
    row,
    profile
):

    base_eligibility, base_checks = (
        determine_eligibility(
            row,
            [profile["state"]]
            if profile["state"]
            else [],
            [profile["occupation"]]
            if profile["occupation"]
            else [],
            profile["gender"],
            profile["age"],
            profile["income"]
        )
    )

    requirements, exclusions, extra_checks = (
        check_additional_requirements_v32(
            row,
            profile
        )
    )

    all_checks = {
        **base_checks,
        **extra_checks
    }

    if any(
        value == "not_eligible"
        for value in all_checks.values()
    ):

        return (
            "not_eligible",
            all_checks,
            requirements,
            exclusions
        )

    unknown_checks = [
        key
        for key, value in extra_checks.items()
        if value == "unknown"
    ]

    if unknown_checks:

        return (
            "partially_verified",
            all_checks,
            requirements,
            exclusions
        )

    if base_eligibility == "unknown":

        return (
            "partially_verified",
            all_checks,
            requirements,
            exclusions
        )

    return (
        "eligible",
        all_checks,
        requirements,
        exclusions
    )


# ============================================================
# CANDIDATE RETRIEVAL
# ============================================================

def get_candidates(
    state,
    occupation,
    category,
    gender
):

    candidates = set()

    for idx, row in master.iterrows():

        row_state = normalize_text(
            row.get(
                "state",
                ""
            )
        )

        row_occupation = normalize_text(
            row.get(
                "occupation",
                ""
            )
        )

        row_category = normalize_text(
            row.get(
                "category",
                ""
            )
        )

        row_gender = normalize_text(
            row.get(
                "gender",
                ""
            )
        )

        state_match = (
            not state
            or "all india" in row_state
            or state in row_state
        )

        occupation_match = (
            not occupation
            or not row_occupation
            or occupation in row_occupation
        )

        category_match = (
            not category
            or not row_category
            or category in row_category
        )

        gender_match = (
            gender is None
            or not row_gender
            or gender in row_gender
            or row_gender in [
                "any",
                "all"
            ]
        )

        if (
            state_match
            and occupation_match
            and category_match
            and gender_match
        ):

            candidates.add(
                idx
            )

    return candidates


# ============================================================
# QUERY RELEVANCE TERMS
# ============================================================

def get_query_relevance_terms(query):

    q = normalize_text(
        query
    )

    terms = set(
        q.split()
    )

    agriculture_terms = {
        "agriculture",
        "agricultural",
        "farmer",
        "farmers",
        "farming",
        "crop",
        "crops",
        "cultivation",
        "irrigation",
        "livestock",
        "dairy",
        "fisheries",
        "fisherman",
        "fishermen",
        "horticulture",
        "piggery",
        "poultry",
        "seed",
        "seeds",
        "fertilizer",
        "fertilizers",
        "farm"
    }

    education_terms = {
        "education",
        "student",
        "students",
        "school",
        "college",
        "university",
        "scholarship",
        "scholarships",
        "engineering",
        "study",
        "studies",
        "academic",
        "higher",
        "learning"
    }

    women_terms = {
        "woman",
        "women",
        "female",
        "girl",
        "girls"
    }

    employment_terms = {
        "employment",
        "job",
        "jobs",
        "worker",
        "workers",
        "unemployed",
        "skill",
        "skills",
        "training"
    }

    business_terms = {
        "business",
        "entrepreneur",
        "entrepreneurship",
        "startup",
        "enterprise",
        "self",
        "employed",
        "loan",
        "loans"
    }

    housing_terms = {
        "housing",
        "house",
        "home",
        "homes",
        "construction"
    }

    health_terms = {
        "health",
        "medical",
        "medicine",
        "hospital",
        "healthcare",
        "insurance",
        "treatment"
    }

    return {

        "agriculture":
            len(terms & agriculture_terms),

        "education":
            len(terms & education_terms),

        "women":
            len(terms & women_terms),

        "employment":
            len(terms & employment_terms),

        "business":
            len(terms & business_terms),

        "housing":
            len(terms & housing_terms),

        "health":
            len(terms & health_terms)
    }


# ============================================================
# RANK CANDIDATES
# ============================================================

def rank_candidates(
    query,
    candidates,
    state,
    occupation,
    category,
    gender,
    age,
    income
):

    ranked = []

    q = normalize_text(
        query
    )

    query_words = set(
        q.split()
    )

    relevance_terms = (
        get_query_relevance_terms(
            query
        )
    )

    strongest_intent = None

    if relevance_terms:

        strongest_intent = max(
            relevance_terms,
            key=relevance_terms.get
        )

        if relevance_terms[
            strongest_intent
        ] == 0:

            strongest_intent = None

    for idx in candidates:

        row = master.iloc[idx]

        score = 0.0

        scheme_name = normalize_text(
            row.get(
                "scheme_name",
                ""
            )
        )

        description = normalize_text(
            row.get(
                "description",
                ""
            )
        )

        benefits = normalize_text(
            row.get(
                "benefits",
                ""
            )
        )

        eligibility_text = normalize_text(
            row.get(
                "eligibility",
                ""
            )
        )

        row_state = normalize_text(
            row.get(
                "state",
                ""
            )
        )

        row_occupation = normalize_text(
            row.get(
                "occupation",
                ""
            )
        )

        row_category = normalize_text(
            row.get(
                "category",
                ""
            )
        )

        row_gender = normalize_text(
            row.get(
                "gender",
                ""
            )
        )

        # ====================================================
        # 1. SCHEME NAME RELEVANCE
        # ====================================================

        scheme_words = set(
            scheme_name.split()
        )

        name_overlap = len(
            query_words
            & scheme_words
        )

        score += name_overlap * 25

        # ====================================================
        # 2. STATE
        # ====================================================

        if state:

            if state in row_state:

                score += 70

            elif "all india" in row_state:

                score += 25

            else:

                score -= 80

        # ====================================================
        # 3. OCCUPATION
        # ====================================================

        if occupation:

            if occupation in row_occupation:

                score += 60

            elif not row_occupation:

                score += 15

            else:

                score -= 50

        # ====================================================
        # 4. CATEGORY
        # ====================================================

        if category:

            if category in row_category:

                score += 70

            elif not row_category:

                score += 10

            else:

                score -= 35

        # ====================================================
        # 5. GENDER
        # ====================================================

        if gender is not None:

            if gender in row_gender:

                score += 50

            elif row_gender in [
                "",
                "any",
                "all"
            ]:

                score += 15

            else:

                score -= 80

        # ====================================================
        # 6. QUERY RELEVANCE
        # ====================================================

        combined_text = (
            scheme_name
            + " "
            + description
            + " "
            + benefits
            + " "
            + eligibility_text
            + " "
            + row_category
            + " "
            + row_occupation
        )

        combined_words = set(
            combined_text.split()
        )

        semantic_overlap = len(
            query_words
            & combined_words
        )

        score += min(
            semantic_overlap * 3,
            30
        )

        # ====================================================
        # 7. DOMAIN RELEVANCE
        # ====================================================

        if strongest_intent:

            if strongest_intent == "agriculture":

                agriculture_hits = 0

                for term in [
                    "agriculture",
                    "agricultural",
                    "farmer",
                    "farming",
                    "crop",
                    "cultivation",
                    "irrigation",
                    "livestock",
                    "dairy",
                    "fisheries",
                    "horticulture",
                    "piggery",
                    "poultry",
                    "farm"
                ]:

                    if term in combined_text:

                        agriculture_hits += 1

                score += min(
                    agriculture_hits * 8,
                    40
                )

            elif strongest_intent == "education":

                education_hits = 0

                for term in [
                    "education",
                    "student",
                    "students",
                    "school",
                    "college",
                    "university",
                    "scholarship",
                    "engineering",
                    "study",
                    "academic"
                ]:

                    if term in combined_text:

                        education_hits += 1

                score += min(
                    education_hits * 8,
                    40
                )

            elif strongest_intent == "women":

                if (
                    "women" in combined_text
                    or "woman" in combined_text
                    or "female" in combined_text
                ):

                    score += 40

            elif strongest_intent == "employment":

                employment_hits = 0

                for term in [
                    "employment",
                    "job",
                    "worker",
                    "training",
                    "skill"
                ]:

                    if term in combined_text:

                        employment_hits += 1

                score += min(
                    employment_hits * 8,
                    40
                )

            elif strongest_intent == "business":

                business_hits = 0

                for term in [
                    "business",
                    "entrepreneur",
                    "enterprise",
                    "loan",
                    "startup"
                ]:

                    if term in combined_text:

                        business_hits += 1

                score += min(
                    business_hits * 8,
                    40
                )

            elif strongest_intent == "health":

                health_hits = 0

                for term in [
                    "health",
                    "medical",
                    "hospital",
                    "insurance",
                    "treatment"
                ]:

                    if term in combined_text:

                        health_hits += 1

                score += min(
                    health_hits * 8,
                    40
                )

            elif strongest_intent == "housing":

                housing_hits = 0

                for term in [
                    "housing",
                    "house",
                    "home",
                    "construction"
                ]:

                    if term in combined_text:

                        housing_hits += 1

                score += min(
                    housing_hits * 8,
                    40
                )

        # ====================================================
        # 8. AGE
        # ====================================================

        if age is not None:

            min_age = row.get(
                "min_age"
            )

            max_age = row.get(
                "max_age"
            )

            age_ok = True

            try:

                if (
                    pd.notna(min_age)
                    and age < float(min_age)
                ):

                    age_ok = False

                if (
                    pd.notna(max_age)
                    and age > float(max_age)
                ):

                    age_ok = False

            except Exception:

                pass

            if age_ok:

                score += 30

            else:

                score -= 150

        # ====================================================
        # 9. INCOME
        # ====================================================

        if income is not None:

            limit = row.get(
                "income_limit"
            )

            if pd.isna(limit):

                score += 10

            else:

                try:

                    if income <= float(limit):

                        score += 35

                    else:

                        score -= 150

                except Exception:

                    pass

        # ====================================================
        # 10. ELIGIBILITY
        # ====================================================

        eligibility, checks = (
            determine_eligibility(
                row,
                [state]
                if state
                else [],
                [occupation]
                if occupation
                else [],
                gender,
                age,
                income
            )
        )

        if eligibility == "eligible":

            score += 20

        elif eligibility == "not_eligible":

            score -= 150

        ranked.append({

            "index":
                idx,

            "score":
                round(
                    score,
                    2
                ),

            "eligibility":
                eligibility,

            "eligibility_checks":
                checks,

            "row":
                row
        })

    ranked.sort(
        key=lambda x:
        x["score"],
        reverse=True
    )

    return ranked


# ============================================================
# FIELD MAP
# ============================================================

FIELD_MAP = {

    "benefits":
        "benefits",

    "eligibility":
        "eligibility",

    "required_documents":
        "required_documents",

    "application_process":
        "application_process",

    "description":
        "description",

    "state":
        "state"
}


# ============================================================
# MAIN QUERY ENGINE
# ============================================================

def yojana_query_v32(
    query,
    top_k=5
):

    profile = extract_user_profile_v31(
        query
    )

    intent = detect_intent(
        query
    )

    # ========================================================
    # EXACT SCHEME
    # ========================================================

    exact_scheme = find_exact_scheme(
        query
    )

    if exact_scheme is not None:

        field = FIELD_MAP.get(
            intent
        )

        # ====================================================
        # EXACT SCHEME FIELD
        # ====================================================

        if field is not None:

            value = exact_scheme.get(
                field,
                ""
            )

            if pd.isna(value):

                value = ""

            return {

                "query":
                    query,

                "intent":
                    intent,

                "retrieval_type":
                    "exact_scheme_field",

                "confidence":
                    1.0,

                "scheme":
                    exact_scheme[
                        "scheme_name"
                    ],

                "answer":
                    str(value),

                "profile":
                    profile,

                "source_row":
                    exact_scheme.to_dict()
            }

        # ====================================================
        # EXACT SCHEME ELIGIBILITY
        # ====================================================

        (
            eligibility,
            checks,
            requirements,
            exclusions
        ) = determine_eligibility_v32(
            exact_scheme,
            profile
        )

        return {

            "query":
                query,

            "intent":
                intent,

            "retrieval_type":
                "exact_scheme",

            "confidence":
                1.0,

            "scheme":
                exact_scheme[
                    "scheme_name"
                ],

            "answer":
                None,

            "eligibility":
                eligibility,

            "eligibility_checks":
                checks,

            "additional_requirements":
                requirements,

            "exclusions":
                exclusions,

            "profile":
                profile,

            "source_row":
                exact_scheme.to_dict()
        }

    # ========================================================
    # PROFILE CHECK
    # ========================================================

    has_profile = any([

        bool(
            profile["state"]
        ),

        bool(
            profile["occupation"]
        ),

        bool(
            profile["category"]
        ),

        profile["gender"]
        is not None,

        profile["age"]
        is not None,

        profile["income"]
        is not None,

        bool(
            profile["social_category"]
        ),

        profile["disability"]
        is not None,

        profile["bpl"]
        is not None
    ])

    if (
        intent == "find_scheme"
        and not has_profile
    ):

        return {

            "query":
                query,

            "intent":
                intent,

            "retrieval_type":
                "insufficient_profile",

            "confidence":
                0.0,

            "message":
                "Please provide at least one profile detail such as state, occupation, age, gender, income, social category, or category.",

            "profile":
                profile,

            "results":
                []
        }

    # ========================================================
    # CANDIDATES
    # ========================================================

    candidates = get_candidates(

        state=
            profile["state"],

        occupation=
            profile["occupation"],

        category=
            profile["category"],

        gender=
            profile["gender"]
    )

    fallback_used = False

    if not candidates:

        candidates = set(
            range(
                len(master)
            )
        )

        fallback_used = True

    # ========================================================
    # RANK
    # ========================================================

    ranked = rank_candidates(

        query=
            query,

        candidates=
            candidates,

        state=
            profile["state"],

        occupation=
            profile["occupation"],

        category=
            profile["category"],

        gender=
            profile["gender"],

        age=
            profile["age"],

        income=
            profile["income"]
    )

    # ========================================================
    # V3.2 ELIGIBILITY
    # ========================================================

    final_ranked = []

    for item in ranked:

        row = item[
            "row"
        ]

        (
            eligibility,
            checks,
            requirements,
            exclusions
        ) = determine_eligibility_v32(
            row,
            profile
        )

        item[
            "eligibility"
        ] = eligibility

        item[
            "eligibility_checks"
        ] = checks

        item[
            "additional_requirements"
        ] = requirements

        item[
            "exclusions"
        ] = exclusions

        if (
            eligibility
            == "partially_verified"
        ):

            item[
                "score"
            ] -= 8

        elif (
            eligibility
            == "not_eligible"
        ):

            item[
                "score"
            ] -= 150

        final_ranked.append(
            item
        )

    # ========================================================
    # SORT AGAIN AFTER ELIGIBILITY
    # ========================================================

    final_ranked.sort(
        key=lambda x:
        x["score"],
        reverse=True
    )

    # ========================================================
    # REMOVE HARD CONTRADICTIONS
    # ========================================================

    if has_profile:

        filtered = [

            item

            for item
            in final_ranked

            if item[
                "eligibility"
            ]
            != "not_eligible"
        ]

        if filtered:

            final_ranked = filtered

    final_ranked = final_ranked[
        :top_k
    ]

    # ========================================================
    # CONFIDENCE
    # ========================================================

    if not final_ranked:

        confidence = 0.0

    else:

        best_score = final_ranked[
            0
        ]["score"]

        if best_score >= 250:

            confidence = 0.95

        elif best_score >= 180:

            confidence = 0.90

        elif best_score >= 120:

            confidence = 0.80

        elif best_score >= 70:

            confidence = 0.65

        else:

            confidence = 0.40

    # ========================================================
    # FORMAT RESULTS
    # ========================================================

    results = []

    for item in final_ranked:

        row = item[
            "row"
        ]

        results.append({

            "scheme_name":
                row.get(
                    "scheme_name",
                    ""
                ),

            "score":
                round(
                    item[
                        "score"
                    ],
                    2
                ),

            "state":
                row.get(
                    "state",
                    ""
                ),

            "category":
                row.get(
                    "category",
                    ""
                ),

            "beneficiary_type":
                row.get(
                    "beneficiary_type",
                    ""
                ),

            "occupation":
                row.get(
                    "occupation",
                    ""
                ),

            "gender":
                row.get(
                    "gender",
                    ""
                ),

            "eligibility":
                item[
                    "eligibility"
                ],

            "eligibility_checks":
                item[
                    "eligibility_checks"
                ],

            "additional_requirements":
                item[
                    "additional_requirements"
                ],

            "exclusions":
                item[
                    "exclusions"
                ],

            "benefits":
                row.get(
                    "benefits",
                    ""
                ),

            "documents":
                row.get(
                    "required_documents",
                    ""
                ),

            "application":
                row.get(
                    "application_process",
                    ""
                ),

            "official_source_url":
                row.get(
                    "official_source_url",
                    ""
                )
        })

    return {

        "query":
            query,

        "intent":
            intent,

        "retrieval_type":
            "attribute_filtered_search",

        "confidence":
            confidence,

        "fallback_used":
            fallback_used,

        "profile":
            profile,

        "results":
            results
    }


# ============================================================
# TEST
# ============================================================

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

        print(
            "QUERY:"
        )

        print(
            query
        )

        result = yojana_query_v32(
            query,
            top_k=5
        )

        print()

        print(
            "TYPE:"
        )

        print(
            result[
                "retrieval_type"
            ]
        )

        if result.get(
            "scheme"
        ):

            print(
                "SCHEME:",
                result[
                    "scheme"
                ]
            )

        if (
            result.get(
                "answer"
            )
            is not None
        ):

            print(
                "ANSWER:",
                result[
                    "answer"
                ]
            )

        if result.get(
            "results"
        ):

            print()

            print(
                "RESULTS:"
            )

            for item in result[
                "results"
            ]:

                print(
                    item[
                        "scheme_name"
                    ],
                    "|",
                    item[
                        "eligibility"
                    ],
                    "|",
                    item[
                        "score"
                    ]
                )