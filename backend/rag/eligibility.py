import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
CSV_PATH = BASE_DIR / "data" / "csv" / "yojana_mitra_master.csv"

df = pd.read_csv(CSV_PATH)


def clean(value):
    if value is None or pd.isna(value):
        return None

    value = str(value).strip().lower()

    if value in ["", "nan", "none", "null"]:
        return None

    return value


def split_values(value):
    value = clean(value)

    if value is None:
        return []

    value = (
        value.replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace('"', "")
        .replace(",", ";")
        .replace("|", ";")
        .replace("/", ";")
    )

    return [x.strip() for x in value.split(";") if x.strip()]


def check_age(user_age, min_age, max_age):

    if user_age is None:
        return "unknown"

    try:
        user_age = float(user_age)

        min_age = clean(min_age)
        max_age = clean(max_age)

        if min_age is not None and user_age < float(min_age):
            return "not_eligible"

        if max_age is not None and user_age > float(max_age):
            return "not_eligible"

        return "eligible"

    except (ValueError, TypeError):
        return "unknown"


def check_income(user_income, income_limit):

    if user_income is None:
        return "unknown"

    income_limit = clean(income_limit)

    if income_limit is None:
        return "unknown"

    try:
        user_income = float(user_income)
        income_limit = float(income_limit)

        if user_income <= income_limit:
            return "eligible"

        return "not_eligible"

    except (ValueError, TypeError):
        return "unknown"


def check_category(user_value, scheme_value):

    user_value = clean(user_value)
    scheme_values = split_values(scheme_value)

    if user_value is None:
        return "unknown"

    # No restriction recorded
    if not scheme_values:
        return "unknown"

    # General unrestricted values
    unrestricted = {
        "all",
        "all india",
        "india",
        "national",
        "nationwide",
        "any",
        "anyone"
    }

    if any(value in unrestricted for value in scheme_values):
        return "eligible"

    # Direct match
    if user_value in scheme_values:
        return "eligible"

    return "not_eligible"


def check_state(user_state, scheme_state):

    user_state = clean(user_state)

    if user_state is None:
        return "unknown"

    scheme_values = split_values(scheme_state)

    if not scheme_values:
        return "unknown"

    unrestricted = {
        "all",
        "all india",
        "india",
        "national",
        "nationwide"
    }

    if any(value in unrestricted for value in scheme_values):
        return "eligible"

    if user_state in scheme_values:
        return "eligible"

    return "not_eligible"


def check_scheme(user_profile, scheme):

    checks = {}

    checks["age"] = check_age(
        user_profile.get("age"),
        scheme.get("min_age"),
        scheme.get("max_age")
    )

    checks["income"] = check_income(
        user_profile.get("income"),
        scheme.get("income_limit")
    )

    checks["state"] = check_state(
        user_profile.get("state"),
        scheme.get("state")
    )

    checks["occupation"] = check_category(
        user_profile.get("occupation"),
        scheme.get("occupation")
    )

    checks["gender"] = check_category(
        user_profile.get("gender"),
        scheme.get("gender")
    )

    checks["social_category"] = check_category(
        user_profile.get("social_category"),
        scheme.get("social_category")
    )

    # Explicit contradiction = exclude
    if "not_eligible" in checks.values():
        status = "not_eligible"

    # No contradiction, but some information is missing
    elif "unknown" in checks.values():
        status = "unknown"

    else:
        status = "eligible"

    return {
        "status": status,
        "checks": checks
    }


def get_candidate_schemes(user_profile):

    candidates = []

    for _, row in df.iterrows():

        scheme = row.to_dict()

        result = check_scheme(user_profile, scheme)

        if result["status"] != "not_eligible":

            candidates.append({
                "scheme_id": scheme.get("scheme_id"),
                "scheme_name": scheme.get("scheme_name"),
                "state": scheme.get("state"),
                "category": scheme.get("category"),
                "eligibility_status": result["status"],
                "checks": result["checks"],
                "official_source_url": scheme.get("official_source_url")
            })

    return candidates


if __name__ == "__main__":

    user_profile = {
        "age": 21,
        "state": "Telangana",
        "occupation": "Student",
        "income": 300000,
        "gender": "Male",
        "social_category": "General"
    }

    candidates = get_candidate_schemes(user_profile)

    print("\nPersonalized scheme filtering")
    print("-" * 60)

    print("User profile:")
    print(user_profile)

    print("\nCandidate schemes:", len(candidates))

    print("\nFirst 10 candidates:")

    for scheme in candidates[:10]:

        print("\nScheme:", scheme["scheme_name"])
        print("State:", scheme["state"])
        print("Category:", scheme["category"])
        print("Status:", scheme["eligibility_status"])
        print("Checks:", scheme["checks"])