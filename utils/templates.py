EXECUTIVE = """
# Executive Brief: {{ dataset_name }}

## Key Insights
{% for insight in insights %}
- {{ insight }}
{% endfor %}

## Top Rows Sample

## Column Summary
{% for col in col_summary %}
- **{{ col.name }}** | type: {{ col.dtype }}, unique: {{ col.n_unique }}, nulls: {{ col.n_null }} ({{ col.pct_null }}%)
{% endfor %}

## Notes on Missing Data
{{ missing_report }}

Provide a brief summary and recommendation based on the data structure.
"""

WHITEPAPER = """
# Whitepaper Overview: {{ dataset_name }}

## Dataset Overview
- Rows: {{ n_rows }}, Columns: {{ n_cols }}

## Insights
{% for insight in insights %}
- {{ insight }}
{% endfor %}

## Data Sample

## Column Schema
{% for col in col_summary %}
- {{ col.name }} ({{ col.dtype }}) — {{ col.n_unique }} unique, {{ col.pct_null }}% null
{% endfor %}

Write this as a formal whitepaper summary suitable for technical or investor audiences.
"""

SYSTEMS = """
# Systems Analysis: {{ dataset_name }}

## Overview
- {{ n_rows }} rows × {{ n_cols }} columns

## Components
{% for col in col_summary %}
- {{ col.name }} | Type: {{ col.dtype }}
{% endfor %}

## Missing Data
{{ missing_report }}

## Observations
{% for insight in insights %}
- {{ insight }}
{% endfor %}

End with 2–3 operational recommendations based on structure and observed patterns.
"""

TEMPLATES = {
    "Executive Brief": EXECUTIVE,
    "Whitepaper Overview": WHITEPAPER,
    "Systems Analysis": SYSTEMS
}
