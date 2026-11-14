from math import exp

WEIGHTS = {"atmosphere": 0.40, "material": 0.25, "airflow": 0.15, "pillar": 0.20}

def _similarity(value, target, scale):
    if value is None or target is None:
        return None
    return max(0.0, 100.0 * exp(-abs(float(value)-float(target))/scale))

def score_investigation(record, target):
    # Missing values are excluded from the weighted average, never silently scored as matches.
    components = {}
    o2 = _similarity(record.get("oxygen_pct"), target.get("oxygen_pct"), 25.0)
    pressure = _similarity(record.get("pressure_psi"), target.get("pressure_psi"), 5.0)
    known_atmosphere = [x for x in (o2, pressure) if x is not None]
    components["atmosphere"] = sum(known_atmosphere)/len(known_atmosphere) if known_atmosphere else None

    target_materials = set(target.get("material_categories", []))
    record_material = record.get("fuel_category")
    components["material"] = 100.0 if record_material in target_materials else (55.0 if record_material in ("mixed", None) else 0.0)

    flow = _similarity(record.get("airflow_m_s"), target.get("airflow_m_s"), 1.0)
    components["airflow"] = flow

    requested = set(target.get("safety_pillars", []))
    available = set(record.get("safety_pillars") or [])
    components["pillar"] = 100.0 * len(requested & available)/len(requested) if requested else None

    active = [(WEIGHTS[k], v) for k,v in components.items() if v is not None]
    if not active:
        return {"score": None, "coverage": 0, "components": components, "confidence": "Insufficient metadata"}
    score = sum(w*v for w,v in active)/sum(w for w,_ in active)
    coverage = 100.0 * sum(w for w,_ in active)/sum(WEIGHTS.values())
    confidence = "High" if coverage >= 80 else "Moderate" if coverage >= 50 else "Low"
    return {"score": round(score,1), "coverage": round(coverage,1), "components": components, "confidence": confidence}

def rank_investigations(records, target):
    results=[]
    for record in records:
        result=score_investigation(record,target)
        results.append({**record, **result})
    return sorted(results, key=lambda x: (x["score"] is not None, x["score"] or -1), reverse=True)
