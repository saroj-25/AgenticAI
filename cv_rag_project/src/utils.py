import pandas as pd 

def flatten_result(results: list[dict]) -> pd.DataFrame: 

    def safe_join(value):
        if isinstance(value, list):
            return ", ".join(map(str, value))
        return str(value)

    rows = []

    for item in results: 
        rows.append({
            "CV File": item.get("cv_file", ""),
            "Name": item.get("name", ""),
            "Email": item.get("email", ""),
            "Phone": item.get("phone", ""),
            "Total Experience (Years)": item.get("total_experience_years", 0),
            "Skills": safe_join(item.get("skills", [])),
            "Education": item.get("education", ""),
            "Recent Roles": item.get("recent_roles", ""),
            "Required Skills Match Score": item.get("scores", {}).get("required_skill_match_score", 0),
            "Experience Match Score": item.get("scores", {}).get("experience_match_score", 0),
            "Education Match Score": item.get("scores", {}).get("education_match_score", 0),
            "Overall Score": item.get("scores", {}).get("overall_score", 0),
            "Decision": item.get("decision", ""),
            "Reason": item.get("reason", ""),
            "Missing Skills": safe_join(item.get("missing_skills", [])),
            "Red Flags": safe_join(item.get("red_flags", []))
        })

    df = pd.DataFrame(rows)

    if not df.empty:
        df["Overall Score"] = pd.to_numeric(df["Overall Score"], errors="coerce")
        df = df.sort_values(by="Overall Score", ascending=False).reset_index(drop=True)

    return df