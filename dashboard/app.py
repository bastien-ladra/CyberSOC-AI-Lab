import json
import os
import sys
from pathlib import Path
from typing import Any

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.alert_analytics import build_distribution
from utils.csv_export import build_csv_export
from utils.human_review import save_human_review
from utils.report_export import build_markdown_report

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


def get_alert_number(path: Path) -> str:
    return path.stem.split("_")[-1]


def get_human_review_path(alert_number: str) -> Path:
    human_review_write_path = HUMAN_REVIEW_WRITE_DIR / f"review_{alert_number}.json"
    human_review_read_path = HUMAN_REVIEW_READ_DIR / f"review_{alert_number}.json"

    return (
        human_review_write_path
        if human_review_write_path.exists()
        else human_review_read_path
    )


def get_human_review_decision(alert_number: str) -> str:
    human_review_path = get_human_review_path(alert_number)

    if not human_review_path.exists():
        return "Non revue"

    try:
        human_review = load_json_file(human_review_path)
    except (OSError, json.JSONDecodeError):
        return "Erreur lecture"

    decision = human_review.get("decision")

    if decision:
        return str(decision)

    return "Revue sans décision"


def get_human_review_timestamp(path: Path) -> str:
    try:
        review_data = load_json_file(path)
    except (OSError, json.JSONDecodeError):
        return ""

    return str(review_data.get("timestamp", ""))


def list_human_review_files() -> list[Path]:
    review_files_by_name: dict[str, Path] = {}

    if HUMAN_REVIEW_READ_DIR.exists():
        for path in HUMAN_REVIEW_READ_DIR.glob("review_*.json"):
            review_files_by_name[path.name] = path

    if HUMAN_REVIEW_WRITE_DIR.exists():
        for path in HUMAN_REVIEW_WRITE_DIR.glob("review_*.json"):
            review_files_by_name[path.name] = path

    return sorted(
        review_files_by_name.values(),
        key=get_human_review_timestamp,
        reverse=True,
    )


def build_human_review_summary(review_files: list[Path]) -> list[dict[str, Any]]:
    summary = []

    for path in review_files:
        try:
            review_data = load_json_file(path)
        except (OSError, json.JSONDecodeError):
            continue

        summary.append(
            {
                "Horodatage": review_data.get("timestamp", "N/A"),
                "Alerte": review_data.get("alert_number", "N/A"),
                "Type": review_data.get("alert_type", "N/A"),
                "Criticité": review_data.get("severity", "N/A"),
                "Priorité": review_data.get("priority_label", "N/A"),
                "Score": review_data.get("priority_score", "N/A"),
                "IP source": review_data.get("source_ip", "N/A"),
                "Technique": review_data.get("mitre_technique", "N/A"),
                "ID technique": review_data.get("mitre_technique_id", "N/A"),
                "Décision": review_data.get("decision", "N/A"),
                "Note analyste": review_data.get("analyst_note", ""),
            }
        )

    return summary

def alert_matches_search(
    path: Path,
    alert_data: dict[str, Any],
    search_query: str,
) -> bool:
    normalized_query = search_query.strip().lower()

    if not normalized_query:
        return True

    alert_number = get_alert_number(path)
    mitre_attack = alert_data.get("mitre_attack", {})

    searchable_values = [
        path.name,
        alert_number,
        str(alert_data.get("alert_type", "")),
        str(alert_data.get("severity", "")),
        str(alert_data.get("priority_label", "")),
        str(alert_data.get("priority_score", "")),
        str(alert_data.get("source_ip", "")),
        str(mitre_attack.get("framework", "")),
        str(mitre_attack.get("tactic", "")),
        str(mitre_attack.get("technique", "")),
        str(mitre_attack.get("technique_id", "")),
        get_human_review_decision(alert_number),
    ]

    human_review_path = get_human_review_path(alert_number)

    if human_review_path.exists():
        try:
            human_review = load_json_file(human_review_path)
            searchable_values.extend(
                [
                    str(human_review.get("decision", "")),
                    str(human_review.get("analyst_note", "")),
                ]
            )
        except (OSError, json.JSONDecodeError):
            pass

    searchable_text = " ".join(searchable_values).lower()

    return normalized_query in searchable_text

def get_alert_priority(path: Path) -> int:
    try:
        alert_data = load_json_file(path)
    except (OSError, json.JSONDecodeError):
        return 0

    priority_score = alert_data.get("priority_score", 0)

    if isinstance(priority_score, int):
        return priority_score

    return 0


def list_alerts() -> list[Path]:
    return sorted(
        ALERT_DIR.glob("alert_*.json"),
        key=get_alert_priority,
        reverse=True,
    )


def format_alert_option(path: Path) -> str:
    try:
        alert_data = load_json_file(path)
    except (OSError, json.JSONDecodeError):
        return path.name

    alert_type = alert_data.get("alert_type", "N/A")
    priority_label = alert_data.get("priority_label", "N/A")
    priority_score = alert_data.get("priority_score", "N/A")
    source_ip = alert_data.get("source_ip", "N/A")

    return (
        f"{path.name} — {alert_type} — "
        f"{priority_label} ({priority_score}/100) — {source_ip}"
    )


def build_alert_summary(alert_files: list[Path]) -> list[dict[str, Any]]:
    summary = []

    for path in alert_files:
        try:
            alert_data = load_json_file(path)
        except (OSError, json.JSONDecodeError):
            continue

        mitre_attack = alert_data.get("mitre_attack", {})
        alert_number = get_alert_number(path)

        summary.append(
            {
                "Fichier": path.name,
                "Type": alert_data.get("alert_type", "N/A"),
                "Criticité": alert_data.get("severity", "N/A"),
                "Priorité": alert_data.get("priority_label", "N/A"),
                "Score": alert_data.get("priority_score", "N/A"),
                "IP source": alert_data.get("source_ip", "N/A"),
                "Technique": mitre_attack.get("technique", "N/A"),
                "ID technique": mitre_attack.get("technique_id", "N/A"),
                "Validation humaine": alert_data.get(
                    "human_validation_required",
                    "N/A",
                ),
                "Décision analyste": get_human_review_decision(alert_number),
            }
        )

    return summary

def get_alert_filter_options(
    alert_files: list[Path],
) -> tuple[list[str], list[str], list[str], list[str]]:
    alert_types = set()
    severities = set()
    priority_labels = set()
    review_decisions = set()

    for path in alert_files:
        try:
            alert_data = load_json_file(path)
        except (OSError, json.JSONDecodeError):
            continue

        alert_types.add(str(alert_data.get("alert_type", "N/A")))
        severities.add(str(alert_data.get("severity", "N/A")))
        priority_labels.add(str(alert_data.get("priority_label", "N/A")))
        review_decisions.add(get_human_review_decision(get_alert_number(path)))

    priority_order = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
        "N/A": 99,
    }

    return (
        sorted(alert_types),
        sorted(severities),
        sorted(priority_labels, key=lambda value: priority_order.get(value, 98)),
        sorted(review_decisions),
    )


def filter_alert_files(
    alert_files: list[Path],
    selected_alert_types: list[str],
    selected_severities: list[str],
    selected_priority_labels: list[str],
    selected_review_decisions: list[str],
    search_query: str,
) -> list[Path]:
    filtered_files = []

    for path in alert_files:
        try:
            alert_data = load_json_file(path)
        except (OSError, json.JSONDecodeError):
            continue

        alert_type = str(alert_data.get("alert_type", "N/A"))
        severity = str(alert_data.get("severity", "N/A"))
        priority_label = str(alert_data.get("priority_label", "N/A"))
        review_decision = get_human_review_decision(get_alert_number(path))
        
        if not alert_matches_search(path, alert_data, search_query):
            continue

        if alert_type not in selected_alert_types:
            continue

        if severity not in selected_severities:
            continue

        if priority_label not in selected_priority_labels:
            continue

        if review_decision not in selected_review_decisions:
            continue

        filtered_files.append(path)

    return filtered_files


def build_alert_metrics(alert_files: list[Path]) -> dict[str, int]:
    metrics = {
        "total": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "human_validation_required": 0,
        "reviewed": 0,
        "not_reviewed": 0,
    }

    for path in alert_files:
        try:
            alert_data = load_json_file(path)
        except (OSError, json.JSONDecodeError):
            continue

        metrics["total"] += 1

        priority_label = str(alert_data.get("priority_label", "")).upper()

        if priority_label == "CRITICAL":
            metrics["critical"] += 1
        elif priority_label == "HIGH":
            metrics["high"] += 1
        elif priority_label == "MEDIUM":
            metrics["medium"] += 1
        elif priority_label == "LOW":
            metrics["low"] += 1

        if alert_data.get("human_validation_required") is True:
            metrics["human_validation_required"] += 1

        review_decision = get_human_review_decision(get_alert_number(path))

        if review_decision == "Non revue":
            metrics["not_reviewed"] += 1
        else:
            metrics["reviewed"] += 1

    return metrics


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
        f"Aucune alerte trouvée dans `{DATA_DIR}`. "
        "Lance `python main.py` ou vérifie le dossier configuré."
    )
    st.stop()

alert_types, severities, priority_labels, review_decisions = get_alert_filter_options(
    alert_files
)

st.sidebar.markdown("## Filtres")

selected_alert_types = st.sidebar.multiselect(
    "Type d'alerte",
    alert_types,
    default=alert_types,
)

selected_severities = st.sidebar.multiselect(
    "Criticité",
    severities,
    default=severities,
)

selected_priority_labels = st.sidebar.multiselect(
    "Priorité",
    priority_labels,
    default=priority_labels,
)

selected_review_decisions = st.sidebar.multiselect(
    "Décision analyste",
    review_decisions,
    default=review_decisions,
)

search_query = st.sidebar.text_input(
    "Recherche",
    placeholder="IP, type, technique, décision, note analyste...",
)

filtered_alert_files = filter_alert_files(
    alert_files,
    selected_alert_types,
    selected_severities,
    selected_priority_labels,
    selected_review_decisions,
    search_query,
)

if not filtered_alert_files:
    st.warning("Aucune alerte ne correspond aux filtres sélectionnés.")
    st.stop()

alert_metrics = build_alert_metrics(filtered_alert_files)

st.markdown("## Indicateurs SOC")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

col1.metric("Alertes affichées", alert_metrics["total"])
col2.metric("CRITICAL", alert_metrics["critical"])
col3.metric("HIGH", alert_metrics["high"])
col4.metric("MEDIUM", alert_metrics["medium"])
col5.metric("Validation humaine", alert_metrics["human_validation_required"])
col6.metric("Revues", alert_metrics["reviewed"])
col7.metric("Non revues", alert_metrics["not_reviewed"])

alert_summary = build_alert_summary(filtered_alert_files)

if alert_summary:
    st.markdown("## Vue d'ensemble des alertes")
    st.dataframe(alert_summary, use_container_width=True)

    st.download_button(
        label="Exporter les alertes filtrées en CSV",
        data=build_csv_export(alert_summary),
        file_name="cybersoc_alerts_filtered.csv",
        mime="text/csv",
    )

priority_distribution = build_distribution(
    alert_summary,
    "Priorité",
    order=["CRITICAL", "HIGH", "MEDIUM", "LOW", "N/A"],
)

review_distribution = build_distribution(
    alert_summary,
    "Décision analyste",
    order=[
        "Non revue",
        "À revoir",
        "Validée",
        "Rejetée",
        "Faux positif",
        "Escalade nécessaire",
        "Erreur lecture",
        "Revue sans décision",
    ],
)

if priority_distribution or review_distribution:
    st.markdown("## Graphiques SOC")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("### Répartition par priorité")
        st.bar_chart(priority_distribution, x="Label", y="Nombre")

    with chart_col2:
        st.markdown("### Répartition par décision analyste")
        st.bar_chart(review_distribution, x="Label", y="Nombre")
        
human_review_files = list_human_review_files()
human_review_summary = build_human_review_summary(human_review_files)

if human_review_summary:
    st.markdown("## Historique des validations humaines")
    st.dataframe(human_review_summary, use_container_width=True)

    st.download_button(
        label="Exporter l'historique des validations en CSV",
        data=build_csv_export(human_review_summary),
        file_name="cybersoc_human_reviews.csv",
        mime="text/csv",
    )
else:
    st.info("Aucune validation humaine enregistrée pour le moment.")

st.download_button(
    label="Exporter un rapport Markdown de synthèse",
    data=build_markdown_report(
        metrics=alert_metrics,
        alert_summary=alert_summary,
        human_review_summary=human_review_summary,
    ),
    file_name="cybersoc_dashboard_report.md",
    mime="text/markdown",
)

selected_alert_file = st.sidebar.selectbox(
    "Sélectionner une alerte",
    filtered_alert_files,
    format_func=format_alert_option,
)

alert = load_json_file(selected_alert_file)
alert_number = get_alert_number(selected_alert_file)

report_path = REPORT_DIR / f"incident_{alert_number}.md"
prompt_path = PROMPT_DIR / f"incident_prompt_{alert_number}.md"
ai_analysis_path = AI_OUTPUT_DIR / f"incident_ai_analysis_{alert_number}.md"
ai_evaluation_path = AI_OUTPUT_DIR / f"incident_ai_evaluation_{alert_number}.json"
human_review_path = get_human_review_path(alert_number)

st.markdown("## Vue synthétique")

priority_score = alert.get("priority_score", "N/A")

if isinstance(priority_score, int):
    priority_score_display = f"{priority_score}/100"
else:
    priority_score_display = str(priority_score)

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Type", alert.get("alert_type", "N/A"))
col2.metric("Criticité", alert.get("severity", "N/A"))
col3.metric("IP source", alert.get("source_ip", "N/A"))
col4.metric("Priorité", alert.get("priority_label", "N/A"))
col5.metric("Score", priority_score_display)
col6.metric(
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
            "Recommandations dangereuses détectées : "
            f"{evaluation.get('dangerous_matches')}"
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