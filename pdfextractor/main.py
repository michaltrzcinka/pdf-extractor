import logging
import sys
from io import BytesIO

import streamlit as st
from extractor import extract

from pdfextractor.logger import app_logger
from pdfextractor.renderer import render_html_table

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def try_extraction(file: BytesIO, fields: list[str]) -> dict[str, str] | None:
    try:
        return extract(file, fields)
    except Exception as e:
        app_logger.exception("Error while extracting fields")
        st.error(f"Error while extracting fields: {e}")
        st.stop()


def try_rendering(field_to_value: dict[str, str]) -> str | None:
    try:
        return render_html_table(field_to_value)
    except Exception as e:
        app_logger.exception("Error while rendering")
        st.error(f"Error while rendering: {e}")
        st.stop()


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

    label_placeholder = st.empty()
    label_placeholder.write("processing")
    progress_placeholder = st.empty()
    progress_bar = progress_placeholder.progress(0)

    progress_bar.progress(50)
    extracted_fields = try_extraction(uploaded_file, selected_fields)
    progress_bar.progress(100)

    progress_placeholder.empty()
    label_placeholder.empty()
    html_table = try_rendering(extracted_fields)
    st.header("Result")
    st.html(html_table)
