# FLARE — Fire Learning, Analysis & Risk Exploration

An early-stage research intelligence dashboard for exploring NASA microgravity combustion investigations and their relevance to crewed space habitats.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
<img width="1272" height="674" alt="image" src="https://github.com/user-attachments/assets/0f1484c9-08cc-46b8-8a4d-d9b54f5508ef" />
<img width="1276" height="633" alt="image" src="https://github.com/user-attachments/assets/a562ea2a-e0a9-47fa-82d4-93055e898c6c" />
<img width="1278" height="630" alt="image" src="https://github.com/user-attachments/assets/bf4d718d-12cd-468b-8162-c1165d8b0fc8" />



## Current prototype scope

- Habitat scenario configuration (oxygen, pressure, airflow, material categories, safety priorities)
- Explainable heuristic relevance ranking with metadata coverage
- Experimental comparison
- Research/data-gap reporting
- Investigation catalogue export
- Atmosphere scatter plot activates when verified oxygen/pressure pairs are added

## Data integrity rules

- `null` means unknown or not yet extracted; it does not mean zero.
- Never infer a numeric test condition from a general investigation description.
- Preserve source URLs and field-level evidence.
- Separate investigation-level descriptions from run-level experimental values.
- Scores are discovery relevance heuristics, not fire-risk probabilities or certification results.
- The starter catalogue is a curated scaffold, not a complete or fully verified PSI export.

## Data sources to verify and expand

- NASA Physical Sciences Informatics: https://psi.nasa.gov/
- NASA PSI investigation search: https://psi.nasa.gov/physci/repo/search?data_source=psi&data_type=investigation
- NASA PSI investigations by research area: https://www.nasa.gov/physical-sciences-informatics-psi/psi-investigations-by-research-area/

## Next engineering milestones

1. Replace generic PSI source links with exact investigation record and publication URLs.
2. Extract run-level oxygen, pressure, flow, fuel geometry, sensors, and measurements.
3. Add field-level citations/evidence and automated schema validation.
4. Implement source-grounded RAG after corpus quality is established.
5. Add user-editable scoring weights and calibration tests with domain experts.
