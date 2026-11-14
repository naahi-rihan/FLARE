from modules.relevance_engine import score_investigation

def test_missing_atmosphere_is_not_scored_as_match():
    record={"oxygen_pct":None,"pressure_psi":None,"airflow_m_s":None,"fuel_category":"solid","safety_pillars":["prevention"]}
    target={"oxygen_pct":30,"pressure_psi":10.2,"airflow_m_s":0.5,"material_categories":["solid"],"safety_pillars":["prevention"]}
    result=score_investigation(record,target)
    assert result["score"] is not None
    assert result["coverage"] < 100
    assert result["components"]["atmosphere"] is None

def test_full_match_scores_higher_than_nonmatch():
    target={"oxygen_pct":30,"pressure_psi":10.2,"airflow_m_s":0.5,"material_categories":["solid"],"safety_pillars":["prevention"]}
    good={"oxygen_pct":30,"pressure_psi":10.2,"airflow_m_s":0.5,"fuel_category":"solid","safety_pillars":["prevention"]}
    bad={"oxygen_pct":80,"pressure_psi":18,"airflow_m_s":4,"fuel_category":"gas","safety_pillars":["detection"]}
    assert score_investigation(good,target)["score"] > score_investigation(bad,target)["score"]
