import os
import streamlit as st
import pandas as pd
import markdown2
from weasyprint import HTML
import tempfile

from utils.analysis import analyze_dataframe
from utils.renderer import render_report_from_template
from llm_client import generate_text

st.set_page_config(page_title="Report Writer Node", layout="wide")
st.title("Report Writer Node")

# Sidebar Upload Section
with st.sidebar:
    st.header("Upload Dataset")
    uploaded_file = st.file_uploader("Choose CSV or JSON", type=["csv", "json"])
    report_type = st.radio("Report Type", ["Executive Brief", "Whitepaper Overview", "Systems Analysis"])
    sample_n = st.slider("Sample Rows", 3, 50, value=10)
    backend = st.selectbox("LLM Backend", ["openai", "local"])

# Early exit if no file
if not uploaded_file:
    st.info("Upload a CSV or JSON file to get started.")
    st.stop()

# Load Data
try:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_json(uploaded_file)
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# Preview + Summary
st.subheader("Dataset Preview")
st.dataframe(df.head(15), use_container_width=True)

with st.spinner("Analyzing dataset..."):
    summary = analyze_dataframe(df)

st.subheader("Data Summary")
st.markdown(f"**Rows:** {summary['n_rows']} | **Columns:** {summary['n_cols']}")
st.dataframe(summary["col_summary"], use_container_width=True)

# === Prompt Builder ===
def build_prompt(report_type, filename, df, sample_n):
    num_rows, num_columns = df.shape
    column_names = ', '.join(df.columns.tolist())

    insight_lines = []
    for col in df.select_dtypes(include='number'):
        nulls = df[col].isnull().sum()
        skew = df[col].skew()
        if nulls > 0:
            insight_lines.append(f"- Column `{col}` has {nulls} missing values.")
        if abs(skew) > 2:
            insight_lines.append(f"- Column `{col}` shows high skewness ({skew:.2f}).")

    insights = "\n".join(insight_lines) if insight_lines else "- No major skew or null values detected."

    prompt = f"""
You are an expert technical writer. Generate a **{report_type}** for the dataset `{filename}`.

### Dataset Metadata:
- Rows: {num_rows}
- Columns: {num_columns}
- Columns: {column_names}

### Key Observations:
{insights}

Write the report in Markdown format and include:
- A short introduction to the dataset
- Summary insights
- Comments on data quality/skewness
- Notable trends or flags (if applicable)
- Keep it concise and structured.
    """
    return prompt.strip()

# === Trigger Generation ===
if st.button("Generate Report"):
    with st.spinner("Generating report..."):
        filename = uploaded_file.name
        llm_prompt = build_prompt(report_type, filename, df, sample_n)
        report = generate_text(llm_prompt, backend=backend, max_tokens=1200)

        # Render to HTML
        html_report = markdown2.markdown(report)

        # Show output
        st.subheader("Markdown Output")
        st.code(report, language="markdown")

        st.subheader("HTML Preview")
        st.components.v1.html(html_report, height=600, scrolling=True)

        # Downloads
        st.download_button("Download .md", report, file_name=f"{filename}_{report_type}.md")
        st.download_button("Download .html", html_report, file_name=f"{filename}_{report_type}.html")

        # Optional: PDF Export
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            HTML(string=html_report).write_pdf(tmp_pdf.name)
            with open(tmp_pdf.name, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name=f"{filename}_{report_type}.pdf",
                    mime="application/pdf"
                )
