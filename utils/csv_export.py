import csv
from io import StringIO
from typing import Any


def build_csv_export(rows: list[dict[str, Any]]) -> bytes:
    if not rows:
        return b""

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))

    writer.writeheader()
    writer.writerows(rows)

    return output.getvalue().encode("utf-8-sig")