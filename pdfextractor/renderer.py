import html


def render_html_table(field_to_value: dict[str, str]) -> str:
    rows = []
    for field_label, value in field_to_value.items():
        rows.append(
            f"<tr><td style='padding:8px;border:1px solid #ddd;font-weight:600'>{html.escape(field_label)}</td><td style='padding:8px;border:1px solid #ddd'>{html.escape(value)}</td></tr>"
        )
    table = "".join(
        [
            "<table style='border-collapse:collapse;width:100%;max-width:720px'>",
            "<thead><tr>",
            "<th style='text-align:left;padding:8px;border:1px solid #ddd'>Field</th>",
            "<th style='text-align:left;padding:8px;border:1px solid #ddd'>Value</th>",
            "</tr></thead>",
            "<tbody>",
            "".join(rows),
            "</tbody></table>",
        ]
    )
    return table
