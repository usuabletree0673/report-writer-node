import pandas as pd

def analyze_dataframe(df: pd.DataFrame):
    n_rows, n_cols = df.shape
    col_info = []

    for col in df.columns:
        ser = df[col]
        n_null = ser.isna().sum()
        pct_null = round(100 * n_null / len(ser), 2)
        dtype = str(ser.dtype)
        n_unique = ser.nunique(dropna=True)
        col_info.append({
            "name": col,
            "dtype": dtype,
            "n_null": n_null,
            "pct_null": pct_null,
            "n_unique": n_unique,
        })

    col_summary = pd.DataFrame(col_info)
    missing_report = "No missing values." if col_summary['n_null'].sum() == 0 else \
        "; ".join(f"{row['name']}: {row['n_null']} nulls ({row['pct_null']}%)" for _, row in col_summary.iterrows() if row['n_null'] > 0)

    # quick heuristics
    insights = []
    for col in df.select_dtypes(include="number").columns[:3]:
        ser = df[col].dropna()
        if ser.nunique() == 1:
            insights.append(f"Column `{col}` has constant value.")
        elif ser.skew() > 2:
            insights.append(f"Column `{col}` is strongly skewed (skew = {round(ser.skew(), 2)}).")
    
    if not insights:
        insights = ["No immediate data flags. Dataset appears clean."]

    return {
        "n_rows": n_rows,
        "n_cols": n_cols,
        "col_summary": col_summary,
        "missing_report": missing_report,
        "auto_insights": insights
    }
