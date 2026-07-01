from collections import Counter
from typing import Any


def build_distribution(
    rows: list[dict[str, Any]],
    field_name: str,
    order: list[str] | None = None,
) -> list[dict[str, int | str]]:
    counts: Counter[str] = Counter()

    for row in rows:
        value = row.get(field_name, "N/A")

        if value is None or value == "":
            value = "N/A"

        counts[str(value)] += 1

    if order is None:
        labels = sorted(counts)
    else:
        ordered_labels = [label for label in order if counts.get(label, 0) > 0]
        remaining_labels = sorted(label for label in counts if label not in order)
        labels = ordered_labels + remaining_labels

    return [
        {
            "Label": label,
            "Nombre": counts[label],
        }
        for label in labels
    ]