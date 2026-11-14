def detect_gaps(records):
    gaps=[]
    if not any(r.get("gravity_regime") in ("partial gravity","lunar gravity","martian gravity") for r in records):
        gaps.append({
            "title":"Partial-gravity combustion evidence",
            "severity":"High",
            "detail":"No partial-gravity combustion records are represented in this starter dataset. Treat this as a dataset coverage gap, not proof that no related research exists anywhere.",
            "recommendation":"Track future LUCI and FM2 datasets and compare microgravity with normal-gravity evidence."
        })
    for field, label in [("oxygen_pct","oxygen concentration"),("pressure_psi","pressure"),("airflow_m_s","airflow speed")]:
        missing=sum(r.get(field) is None for r in records)
        if missing:
            gaps.append({
                "title":f"Missing {label} metadata",
                "severity":"Medium",
                "detail":f"{missing} of {len(records)} starter investigation records do not yet contain a verified numeric {label} value.",
                "recommendation":"Extract run-level conditions from the source investigation records before drawing quantitative conclusions."
            })
    return gaps
