import json
from pathlib import Path

import streamlit as st


ALERT_DIR = Path("alerts")
REPORT_DIR = Path("reports")
PROMPT_DIR = Path("prompts")
AI_OUTPUT_DIR = Path("ai_outputs")
AUDIT_FILE = Path("audit/audit_log.jsonl")


st.set_page_config(
    page_title="CyberSOC-AI-Lab",
    page_icon="🛡️",
    layout="wide",
)


def load_json_file(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_text_file(path: Path) -> str:
    if not path.exists():
        return "Fichier non disponible."
    return path.read_text(encoding="utf-8")


def list_alerts() -> list[Path]:
    return sorted(ALERT_DIR.glob("alert_*.json"))


st.title("CyberSOC-AI-Lab")
st.subheader("Prototype de SOC augmenté par IA")

st.markdown(
    """
Ce tableau de bord permet de visualiser les alertes détectées, les rapports générés,
les prompts IA, les analyses IA locales et les évaluations automatiques des réponses IA.
"""
)

alert_files = list_alerts()

if not alert_files:
    st.warning("Aucune alerte trouvée. Lance d'abord `python main.py` ou `python main.py --enable-ai`.")
    st.stop()

selected_alert_file = st.sidebar.selectbox(
    "Sélectionner une alerte",
    alert_files,
    format_func=lambda path: path.name,
)

alert = load_json_file(selected_alert_file)

alert_number = selected_alert_file.stem.split("_")[-1]

report_path = REPORT_DIR / f"incident_{alert_number}.md"
prompt_path = PROMPT_DIR / f"incident_prompt_{alert_number}.md"
ai_analysis_path = AI_OUTPUT_DIR / f"incident_ai_analysis_{alert_number}.md"
ai_evaluation_path = AI_OUTPUT_DIR / f"incident_ai_evaluation_{alert_number}.json"

st.markdown("## Vue synthétique")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Type", alert.get("alert_type", "N/A"))
col2.metric("Criticité", alert.get("severity", "N/A"))
col3.metric("IP source", alert.get("source_ip", "N/A"))
col4.metric("Validation humaine", str(alert.get("human_validation_required", "N/A")))

if ai_evaluation_path.exists():
    evaluation = load_json_file(ai_evaluation_path)

    st.markdown("## Évaluation IA")

    col1, col2, col3 = st.columns(3)

    col1.metric("Score IA", f"{evaluation.get('score')}/{evaluation.get('max_score')}")
    col2.metric("Acceptable", str(evaluation.get("is_acceptable")))
    col3.metric("Validation humaine mentionnée", str(evaluation.get("human_validation_mentioned")))

    if evaluation.get("dangerous_matches"):
        st.error(f"Recommandations dangereuses détectées : {evaluation.get('dangerous_matches')}")
    else:
        st.success("Aucune recommandation dangereuse détectée.")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Alerte JSON",
        "Rapport",
        "Prompt IA",
        "Analyse IA",
        "Audit",
    ]
)

with tab1:
    st.json(alert)

with tab2:
    st.markdown(load_text_file(report_path))

with tab3:
    st.code(load_text_file(prompt_path), language="markdown")

with tab4:
    if ai_analysis_path.exists():
        st.markdown(load_text_file(ai_analysis_path))
    else:
        st.info("Aucune analyse IA disponible. Lance `python main.py --enable-ai`.")

with tab5:
    if AUDIT_FILE.exists():
        st.code(load_text_file(AUDIT_FILE), language="json")
    else:
        st.info("Aucun journal d'audit disponible.")