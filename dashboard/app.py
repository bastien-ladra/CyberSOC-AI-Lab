import json
import os
import sys
from pathlib import Path
from typing import Any

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from utils.human_review import save_human_review

def resolve_data_dir() -> Path:
    configured_dir = os.getenv("CYBERSOC_OUTPUT_DIR")

    if configured_dir:
        data_dir = Path(configured_dir)

        if not data_dir.is_absolute():
            data_dir = PROJECT_ROOT / data_dir

        return data_dir

    runtime_dir = PROJECT_ROOT / "runtime"
    examples_dir = PROJECT_ROOT / "examples"

    runtime_alerts_dir = runtime_dir / "alerts"

    if runtime_alerts_dir.exists() and any(runtime_alerts_dir.glob("*.json")):
        return runtime_dir

    return examples_dir

def resolve_write_dir(data_dir: Path) -> Path:
    configured_dir = os.getenv("CYBERSOC_OUTPUT_DIR")

    if configured_dir:
        return data_dir

    if data_dir == PROJECT_ROOT / "examples":
        return PROJECT_ROOT / "runtime"

    return data_dir

DATA_DIR = resolve_data_dir()
WRITE_DIR = resolve_write_dir(DATA_DIR)

ALERT_DIR = DATA_DIR / "alerts"
REPORT_DIR = DATA_DIR / "reports"
PROMPT_DIR = DATA_DIR / "prompts"
AI_OUTPUT_DIR = DATA_DIR / "ai_outputs"
AUDIT_FILE = DATA_DIR / "audit" / "audit_log.jsonl"

HUMAN_REVIEW_READ_DIR = DATA_DIR / "human_reviews"
HUMAN_REVIEW_READ_AUDIT_FILE = DATA_DIR / "audit" / "human_review_log.jsonl"

HUMAN_REVIEW_WRITE_DIR = WRITE_DIR / "human_reviews"
HUMAN_REVIEW_WRITE_AUDIT_FILE = WRITE_DIR / "audit" / "human_review_log.jsonl"

st.set_page_config(
    page_title="CyberSOC-AI-Lab",
    page_icon="🛡️",
    layout="wide",
)

st.caption(f"Dossier de données lu : `{DATA_DIR}`")
st.caption(f"Dossier d'écriture des validations : `{WRITE_DIR}`")

def load_json_file(path: Path) -> dict[str, Any]:
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
les prompts IA, les analyses IA locales, les évaluations automatiques des réponses IA
et les validations humaines.
"""
)

alert_files = list_alerts()

if not alert_files:
    st.warning(
    f"Aucune alerte trouvée dans `{DATA_DIR}`. Lance `python main.py` ou vérifie le dossier configuré."
    )
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
ai_evaluation_path = AI_OUTPUT_DIR / \
    f"incident_ai_evaluation_{alert_number}.json"
human_review_write_path = HUMAN_REVIEW_WRITE_DIR / f"review_{alert_number}.json"
human_review_read_path = HUMAN_REVIEW_READ_DIR / f"review_{alert_number}.json"

human_review_path = (
    human_review_write_path
    if human_review_write_path.exists()
    else human_review_read_path
)

st.markdown("## Vue synthétique")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Type", alert.get("alert_type", "N/A"))
col2.metric("Criticité", alert.get("severity", "N/A"))
col3.metric("IP source", alert.get("source_ip", "N/A"))
col4.metric(
    "Validation humaine",
    str(alert.get("human_validation_required", "N/A")),
)

mitre_attack = alert.get("mitre_attack")

if mitre_attack:
    st.markdown("## Enrichissement MITRE / Sécurité IA")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Framework", mitre_attack.get("framework", "N/A"))
    col2.metric("Tactique", mitre_attack.get("tactic", "N/A"))
    col3.metric("Technique", mitre_attack.get("technique", "N/A"))
    col4.metric("ID", mitre_attack.get("technique_id", "N/A"))

    reference_url = mitre_attack.get("reference_url")

    if reference_url:
        st.markdown(f"[Référence]({reference_url})")

recommended_actions = alert.get("recommended_actions", [])

if recommended_actions:
    st.markdown("## Recommandations analyste")

    for action in recommended_actions:
        st.markdown(f"- {action}")
        
if ai_evaluation_path.exists():
    evaluation = load_json_file(ai_evaluation_path)
    st.markdown("## Évaluation IA")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Score IA",
        f"{evaluation.get('score')}/{evaluation.get('max_score')}",
    )
    col2.metric("Acceptable", str(evaluation.get("is_acceptable")))
    col3.metric(
        "Validation humaine mentionnée",
        str(evaluation.get("human_validation_mentioned")),
    )

    if evaluation.get("dangerous_matches"):
        st.error(
            f"Recommandations dangereuses détectées : {evaluation.get('dangerous_matches')}"
        )
    else:
        st.success("Aucune recommandation dangereuse détectée.")
else:
    st.info("Aucune évaluation IA disponible pour cette alerte.")

st.markdown("## Validation humaine")

if human_review_path.exists():
    existing_review = load_json_file(human_review_path)
    st.info(
        f"Décision actuelle : **{existing_review.get('decision')}** — "
        f"{existing_review.get('analyst_note', '')}"
    )

with st.form("human_review_form"):
    decision = st.selectbox(
        "Décision analyste",
        [
            "À revoir",
            "Validée",
            "Rejetée",
            "Faux positif",
            "Escalade nécessaire",
        ],
    )

    analyst_note = st.text_area(
        "Note analyste",
        placeholder=(
            "Exemple : activité suspecte cohérente avec une phase de reconnaissance, "
            "à corréler avec les logs firewall."
        ),
    )

    submitted = st.form_submit_button("Enregistrer la validation humaine")

    if submitted:
        review_path = save_human_review(
        alert_number=alert_number,
        alert=alert,
        decision=decision,
        analyst_note=analyst_note,
        review_dir=HUMAN_REVIEW_WRITE_DIR,
        audit_file=HUMAN_REVIEW_WRITE_AUDIT_FILE,
    )

        st.success(f"Validation humaine enregistrée : {review_path}")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Alerte JSON",
        "Rapport",
        "Prompt IA",
        "Analyse IA",
        "Audit",
        "Validation humaine",
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
    st.markdown("### Audit système")

    if AUDIT_FILE.exists():
        st.code(load_text_file(AUDIT_FILE), language="json")
    else:
        st.info("Aucun journal d'audit système disponible.")

    st.markdown("### Audit des validations humaines")

    human_review_audit_file = (
    HUMAN_REVIEW_WRITE_AUDIT_FILE
    if HUMAN_REVIEW_WRITE_AUDIT_FILE.exists()
    else HUMAN_REVIEW_READ_AUDIT_FILE
    )

    if human_review_audit_file.exists():
        st.code(load_text_file(human_review_audit_file), language="json")
    else:
        st.info("Aucun journal de validation humaine disponible.")

with tab6:
    if human_review_path.exists():
        st.json(load_json_file(human_review_path))
    else:
        st.info("Aucune validation humaine enregistrée pour cette alerte.")
