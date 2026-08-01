import streamlit as st

st.set_page_config(page_title="AITestKit Dashboard", layout="wide")

st.title("⚡ AITestKit — AI Evaluation Platform")
st.markdown("Unified Benchmark & Diagnostic Suite for LLMs, RAG, Safety & Vision")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select Engine", ["Overview", "LLM Benchmark", "RAG Pipeline", "Safety & Security", "Vision & OCR"])

if page == "Overview":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tests Run", "142", "+12 today")
    col2.metric("Avg Latency", "1.24s", "-0.15s")
    col3.metric("Safety Score", "98.2%", "Passed")
    col4.metric("RAG Faithfulness", "84.5%", "+2.1%")

    st.subheader("System Performance Benchmark")
    st.line_chart([1.2, 1.1, 1.4, 1.25, 1.0, 0.95, 1.15])

elif page == "Safety & Security":
    st.subheader("Safety Audit Status")
    st.error("Prompt Injection Detected in Session #89")
    st.json({
        "prompt_injection_risk": "50.0%",
        "jailbreak_risk": "0.0%",
        "pii_leakage": False,
        "status": "FAILED"
    })