# Report Writer Node

**AI-powered tool that transforms CSV or tabular performance data into clean, executive-ready summaries using GPT-based natural language output.**  
Designed to reduce reporting overhead and bridge raw data → narrative decision support.

---

## Section 1: For Recruiters & Strategy Leads

### What It Is
A lightweight LLM-powered node that ingests structured business data (CSVs, ops tables, snapshots) and outputs readable decision-focused reports in seconds.

### Why It Matters
Most teams spend hours manually summarizing operations, sales, or financial KPIs. This node auto-generates:
- Executive summaries
- Weekly performance briefs
- Change-over-time insights

Useful in environments with high reporting demands, low analyst bandwidth, or growing data complexity.

### Problems It Solves
- Analysts stuck summarizing data weekly
- Managers needing clarity without deep spreadsheet dives
- Strategy teams needing consistent internal updates

### Who Uses It
- Ops managers, product leads, analysts, founders
- Any org running recurring reporting cycles (rev ops, growth, finance, internal comms)

### Key Questions It Answers
- “What changed since last report?”
- “What do I need to focus on?”
- “Is this trend expected or out of bounds?”

---

## Section 2: For Technical Reviewers

### Data Input
- Streamlit UI allows CSV upload
- Tested with synthetic + real tabular data
- Assumes one versioning column (e.g. date, week, snapshot)

### Architecture
```plaintext
[Upload CSV]
   ↓
[Pandas Normalization]
   ↓
[Prompt Template Builder]
   ↓
[OpenAI GPT-4 API Call]
   ↓
[Formatted Report Output]
   ↓
[Streamlit Preview + Download]


Core Modules

    analysis.py → column validation, deltas, ranges

    prompts.py → structured prompt builder

    llm_wrapper.py → GPT call logic (can be swapped)

    output.py → structured report formatter

    app.py → Streamlit UI

Prompt Logic

    Templates for: summary, change detection, anomaly flags

    Adaptable to trend shift, table comparison, or multi-level analysis

    Forkable for industry-specific report types

## Tradeoffs & Limitations

Tradeoffs

    Prioritizes interpretability over model complexity

    Best with labeled and clean input formats

    No real-time data connection (yet)

## Known Limitations

    No auth layer — not production secure

    Generic output if input lacks context columns

    GPT output requires light human review before final delivery

 Run Locally
Setup

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Launch

streamlit run app.py

## Future Enhancements

Add editable template layer for custom report formats

Support Excel uploads and column mapping UI

    Optional embedding of visuals (charts/tables)


