from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from truthlens_crew.config import load_settings
from truthlens_crew.evaluation import run_benchmark
from truthlens_crew.graphs import FactCheckCrew


st.set_page_config(page_title="TruthLens Crew", layout="wide")
st.title("TruthLens Crew")

settings = load_settings()
crew = FactCheckCrew(settings)
tabs = st.tabs(["Single Claim", "Evidence Courtroom", "Benchmark Results", "Agent Trace"])

with tabs[0]:
    claim = st.text_input("Claim", "Pakistan gained independence in 1947.")
    if st.button("Verify", type="primary"):
        st.session_state["result"] = crew.verify(claim)

with tabs[1]:
    result = st.session_state.get("result")
    if result:
        st.metric("Verdict", result.verdict.value)
        st.metric("Confidence", f"{result.confidence:.0%}")
        left, right = st.columns(2)
        with left:
            st.subheader("Supporter")
            for item in result.supporting_evidence:
                st.write(f"**{item.title}**")
                st.caption(item.url)
                st.write(item.snippet)
        with right:
            st.subheader("Skeptic")
            for item in result.counter_evidence:
                st.write(f"**{item.title}**")
                st.caption(item.url)
                st.write(item.snippet)
        st.subheader("Verifier Analysis")
        st.write(result.analysis)
    else:
        st.info("Verify a claim first.")

with tabs[2]:
    if st.button("Run sample benchmark"):
        rows = run_benchmark(Path("data/sample/claims.csv"), settings)
        st.dataframe(pd.DataFrame([row.__dict__ for row in rows]), use_container_width=True)

with tabs[3]:
    result = st.session_state.get("result")
    if result:
        st.json(result.model_dump(mode="json"))
    else:
        st.info("Agent trace appears after verification.")

