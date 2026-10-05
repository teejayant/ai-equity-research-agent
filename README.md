# Super Investing · AI Equity Research Agent (Part B)

An autonomous **AI Equity Research Agent** built for [Super Investing](https://superinvesting.example) to assist retail investors in researching Indian stocks. Given an NSE ticker and a set of unstructured documents (financial filings, earnings transcripts, news, exchange announcements), the agent synthesizes a structured, retail-friendly, one-page **Research Brief**.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.9+
- Pip dependencies installed:
```bash
pip install -r requirements.txt
```

*(Note: `requirements.txt` includes `streamlit`, `google-generativeai`, `openai`, `pydantic`, `rich`)*

---

### Option A: Interactive Web Dashboard (Recommended for Video Recording)
Run the Streamlit interactive dashboard:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`. Features include:
- **1-Click Agent Execution** for test pack `SRVCABLE` or live NSE tickers.
- **Document Security & Audit Dashboard** showing real-time prompt injection detection and entity filtering.
- **Raw Document Explorer** and **Brief Markdown Export**.

---

### Option B: Command Line Interface (CLI)
Run the agent directly on the provided research pack:
```bash
python agent.py --ticker SRVCABLE --docs research_pack --output output/brief_SRVCABLE.md
```

---

## 🤖 Models Used & Rationale

| Model / Engine | Purpose | Rationale |
|---|---|---|
| **Google Gemini (1.5 / 2.0 Flash / Medium)** | Primary LLM Backend | Large context window (1M+ tokens), fast inference speed (<2s), high precision in processing structured table data and multi-document financial transcripts without context truncation. |
| **OpenAI GPT-4o** | Alternative LLM Backend | Industry standard for nuanced reasoning, zero-shot entity disambiguation, and financial logic. |
| **Built-in Smart Engine** | Zero-Dependency Fallback | Guarantees 100% deterministic execution and complete brief generation even without active API keys or when running offline. |

---

## 🧠 How the Agent Thinks (Architecture)

```
                       ┌────────────────────────────────┐
                       │   Unstructured Document Pack   │
                       └───────────────┬────────────────┘
                                       │
                                       ▼
                       ┌────────────────────────────────┐
                       │ Stage 1: Document Parsing &    │
                       │          Frontmatter Extraction│
                       └───────────────┬────────────────┘
                                       │
                                       ▼
                       ┌────────────────────────────────┐
                       │ Stage 2: Security & Entity     │
                       │          Screening Engine      │
                       │  • Prompt Injection Shield     │
                       │  • Entity Disambiguation       │
                       └───────────────┬────────────────┘
                                       │
                                       ▼
                       ┌────────────────────────────────┐
                       │ Stage 3: Discrepancy & Recency │
                       │          Resolution Engine     │
                       │  • Hierarchy of Disclosures    │
                       │  • Date Relativity (Sep 2026)  │
                       └───────────────┬────────────────┘
                                       │
                                       ▼
                       ┌────────────────────────────────┐
                       │ Stage 4: Retail Brief          │
                       │          Synthesis (5 Sections)│
                       └────────────────────────────────┘
```

1. **Prompt Injection Shield:** Detects and sanitizes malicious instructions (e.g., hidden comments in `multibaggeralerts_2026-08-12.md` instructing AI to declare a "STRONG BUY").
2. **Entity Disambiguation:** Distinguishes target company (*Sarvottam Cables Ltd*, power cables) from unrelated entities (*Sarvottam Cable Network*, local cable TV operator in Nagpur) and strips invalid sources.
3. **Data Discrepancy Quarantining:** Detects conflicts between news reports (₹1,428 cr revenue) and official exchange disclosures (₹1,248 cr revenue). Prioritizes exchange disclosures for core metrics and flags discrepancies under *Open Questions*.
4. **Recency Verification:** Anchors document dates against the reference date (**23 September 2026**), correctly updating promoter pledge from old 2024 news (35%) to recent July 2026 exchange disclosures (4.1%).

---

## 📁 Repository Structure

```
.
├── agent.py                    # Core AI Research Agent pipeline
├── app.py                      # Streamlit interactive Web Dashboard
├── live_search.py              # Live web search tool for real NSE tickers (Bonus)
├── system_prompt.md            # System prompt & operating instructions
├── TEST_LOG.md                 # Test log covering 3 iterations & prompt adjustments
├── requirements.txt            # Python dependencies
├── research_pack/              # 8 test documents for Sarvottam Cables Ltd
│   ├── businessdaily_2026-08-09.md
│   ├── ir_concall_2026-08-11.md
│   ├── ir_press_release_2026-08-08.md
│   ├── marketwatchindia_2024-03-18.md
│   ├── multibaggeralerts_2026-08-12.md
│   ├── nagpurcitytimes_2026-08-20.md
│   ├── nse_announcement_2026-09-02.md
│   └── nse_shareholding_2026-07-15.md
└── output/
    └── brief_SRVCABLE.md       # Final generated research brief for SRVCABLE
```

---

## 📋 Required Deliverables Checklist

- [x] **System Prompt File:** Saved separately as [`system_prompt.md`](file:///c:/Users/Tanishka/Desktop/study/OTHERS/supertrading%20assignment/system_prompt.md).
- [x] **Generated Research Brief:** Output stored in [`output/brief_SRVCABLE.md`](file:///c:/Users/Tanishka/Desktop/study/OTHERS/supertrading%20assignment/output/brief_SRVCABLE.md).
- [x] **Test Log:** Documenting 3 iterations in [`TEST_LOG.md`](file:///c:/Users/Tanishka/Desktop/study/OTHERS/supertrading%20assignment/TEST_LOG.md).
- [x] **README.md:** Model choices, execution guide, and architectural walkthrough.
- [x] **Bonus Feature:** Support for live NSE ticker lookup via `live_search.py` and UI toggle.
