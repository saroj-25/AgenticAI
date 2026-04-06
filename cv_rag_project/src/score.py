def apply_weighting(result: dict) -> dict:
    def safe_float(value):
        try:
            return float(str(value).replace('%', '').strip())
        except:
            return 0.0

    result = result.copy()
    scores = result.get("scores", {})

    if not isinstance(scores, dict):
        scores = {}

    skill_score = safe_float(scores.get("required_skill_match_score", 0))
    edu_score = safe_float(scores.get("education_match_score", 0))
    experience_score = safe_float(scores.get("experience_match_score", 0))

    overall = round((skill_score * 0.5) + (experience_score * 0.3) + (edu_score * 0.2), 2)

    scores["overall_score"] = overall
    result["scores"] = scores

    # decision
    if overall < 60:
        result["decision"] = "REJECT"
    elif overall < 75:
        result["decision"] = "HOLD"
    else:
        result["decision"] = "SELECT"

    return result