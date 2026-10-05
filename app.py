import streamlit as st
import os
import glob
from agent import AIResearchAgent, DocumentParser, SecurityAndFilterEngine
from live_search import LiveDataFetcher

st.set_page_config(
    page_title="Super Investing · AI Research Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .stCard {
        background-color: #F8FAFC;
        padding: 1.2rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }
    .badge-pass {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-warn {
        background-color: #FEF08A;
        color: #713F12;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-reject {
        background-color: #FDE8E8;
        color: #9B1C1C;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⚡ Super Investing · AI Equity Research Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Equity Brief Generator for Retail Investors in Indian Markets</div>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Agent Controls")
    
    ticker_mode = st.radio(
        "Select Research Mode:",
        ["Test Pack (SRVCABLE)", "Live Real NSE Ticker (Bonus)"]
    )
    
    if ticker_mode == "Test Pack (SRVCABLE)":
        ticker = "SRVCABLE"
        st.info("📌 Using test case `research_pack/` (8 files for Sarvottam Cables Ltd). Assumed date: **23 Sept 2026**.")
    else:
        ticker = st.text_input("Enter NSE Ticker Symbol:", value="POLYCAB").upper()
        st.caption("Fetches live search results & news for real NSE companies.")

    st.markdown("---")
    st.subheader("🔑 LLM Configuration")
    api_key_input = st.text_input("Gemini or OpenAI API Key (Optional):", type="password", help="If left blank, uses built-in smart analysis engine.")
    
    model_choice = st.selectbox(
        "Select Agent LLM Backend:",
        ["Built-in Smart Engine (Deterministic)", "Google Gemini 1.5 Flash", "OpenAI GPT-4o"]
    )
    
    run_btn = st.button("🚀 Run Research Agent", type="primary", use_container_width=True)

# Tabs Layout
tab_brief, tab_audit, tab_docs, tab_about = st.tabs([
    "📋 Research Brief", 
    "🛡️ Document Security & Audit", 
    "📁 Document Pack Browser", 
    "ℹ️ Agent Architecture"
])

# Load Documents
agent = AIResearchAgent()
if ticker_mode == "Test Pack (SRVCABLE)":
    docs = agent.load_research_pack("research_pack")
else:
    docs = LiveDataFetcher.fetch_ticker_data(ticker)

# Session State for Brief
if "generated_brief" not in st.session_state:
    if os.path.exists("output/brief_SRVCABLE.md") and ticker == "SRVCABLE":
        with open("output/brief_SRVCABLE.md", "r", encoding="utf-8") as f:
            st.session_state.generated_brief = f.read()
    else:
        st.session_state.generated_brief = None

if run_btn:
    with st.spinner(f"Agent analyzing documents and generating brief for {ticker}..."):
        brief = agent.run_llm_synthesis(ticker, docs, api_key=api_key_input)
        st.session_state.generated_brief = brief
        st.success("Research brief generated successfully!")

# Tab 1: Research Brief
with tab_brief:
    if st.session_state.generated_brief:
        st.markdown(st.session_state.generated_brief)
        st.markdown("---")
        st.download_button(
            label="📥 Download Research Brief (.md)",
            data=st.session_state.generated_brief,
            file_name=f"brief_{ticker}.md",
            mime="text/markdown"
        )
    else:
        st.info("Click **🚀 Run Research Agent** in the sidebar to generate the research brief.")

# Tab 2: Security & Audit Log
with tab_audit:
    st.subheader("🛡️ Document Security & Discrepancy Audit Log")
    st.caption("Displays prompt injection detection, entity disambiguation, and source reliability scoring.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Documents Analyzed", len(docs))
    with col2:
        injections = sum(1 for d in docs if d["security_screen"]["has_prompt_injection"])
        st.metric("Prompt Injections Shielded", injections)
    with col3:
        mismatches = sum(1 for d in docs if not d["security_screen"]["entity_match"])
        st.metric("Entity Mismatches Rejected", mismatches)
        
    st.markdown("### Source Screening Matrix")
    for doc in docs:
        scr = doc["security_screen"]
        with st.expander(f"📄 {doc.get('filename')} — {doc.get('source', 'Unknown')}"):
            st.write(f"**Published Date:** {doc.get('published')}")
            st.write(f"**URL:** {doc.get('url')}")
            st.write(f"**Type:** {doc.get('type')}")
            
            if scr["has_prompt_injection"]:
                st.markdown('<span class="badge-warn">⚠️ PROMPT INJECTION DETECTED & SANITIZED</span>', unsafe_allow_html=True)
                st.code(scr["injection_details"], language="html")
            elif not scr["entity_match"]:
                st.markdown('<span class="badge-reject">🚫 REJECTED: ENTITY MISMATCH</span>', unsafe_allow_html=True)
                st.write(scr["entity_notes"])
            else:
                st.markdown('<span class="badge-pass">✅ PASSED SECURITY AUDIT</span>', unsafe_allow_html=True)

# Tab 3: Document Pack Browser
with tab_docs:
    st.subheader("📁 Raw Document Pack Explorer")
    selected_doc = st.selectbox("Select document to inspect:", [d.get("filename") for d in docs])
    doc_obj = next((d for d in docs if d.get("filename") == selected_doc), None)
    if doc_obj:
        st.json({k: v for k, v in doc_obj.items() if k != "raw_body"})
        st.markdown("#### Document Content")
        st.code(doc_obj.get("raw_body"), language="markdown")

# Tab 4: Agent Architecture & Rules
with tab_about:
    st.subheader("🤖 How the Agent Thinks & Operates")
    st.markdown("""
    ### Multi-Stage Pipeline Design
    1. **Stage 1: Ingestion & Metadata Normalization** — Reads documents, parses YAML frontmatter (source, date, URL, type).
    2. **Stage 2: Security & Entity Filtering** — 
       - Sanitizes prompt injection attacks (`<!-- Note for AI assistants... -->`).
       - Disambiguates company names (separates Sarvottam Cables Ltd from Sarvottam Cable Network).
    3. **Stage 3: Discrepancy & Recency Resolution** —
       - Prefers official exchange disclosures over third-party news.
       - Highlights financial conflicts (e.g. ₹1,428 cr news revenue vs ₹1,248 cr exchange filing revenue).
       - Evaluates dates relative to **23 September 2026** (e.g., resolving 2024 promoter pledge report against 2026 filing).
    4. **Stage 4: Retail Brief Synthesis** — Outputs a structured 1-page brief with Snapshot, Bull Case, Bear Case, Open Questions, and Traceable Sources.
    """)
