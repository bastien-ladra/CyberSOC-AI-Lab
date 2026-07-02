import csv
from io import StringIO
from typing import Any


def build_csv_export(rows: list[dict[str, Any]]) -> bytes:
    if not rows:
        return b""

    fieldnames = list(rows[0].keys())

    for row in rows[1:]:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(rows)

    return output.getvalue().encode("utf-8-sig")
