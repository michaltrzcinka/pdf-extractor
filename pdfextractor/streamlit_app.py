import html
import logging
import sys

import streamlit as st
from extract import extract

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


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


st.set_page_config(page_title="PDF Extractor", layout="centered")
st.title("PDF Extractor")

st.header("Fields")
closed_fields = ["Customer name", "Branch name", "Claim type"]
selected_fields = st.multiselect(
    "Select fields", closed_fields, default=["Customer name"]
)

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
extract_clicked = st.button("Extract", type="primary")

if extract_clicked:
    if uploaded_file is None:
        st.warning("Please upload a PDF.")
        st.stop()
    if not selected_fields:
        st.warning("Please select at least one field.")
        st.stop()

    progress_placeholder = st.empty()
    label_placeholder = st.empty()
    progress_bar = progress_placeholder.progress(0)
    label_placeholder.write("processing")
    progress_bar.progress(50)

    extracted_fields = extract(uploaded_file, selected_fields)

    progress_placeholder.empty()
    label_placeholder.empty()

    html_table = render_html_table(extracted_fields)
    st.html(html_table)
