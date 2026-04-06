import json
import streamlit as st
from src.ingest import save_uploaded_file, build_vector_store, clear_vector_db
from src.rag_pipeline import get_vector_store, evaluate_candidate
from src.score import apply_weighting
from src.utils import flatten_result

import os
os.environ["PYDANTIC_V1_FORCE"] = "1"

st.set_page_config(page_title="CV Screening with Ollama RAG", layout="wide")
st.title("CV Screening with Ollama RAG and LangChain")

if "results" not in st.session_state:
    st.session_state.results = []

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

with st.sidebar:
    st.header("Settings")
    llm_model = st.text_input("LLM model", value="llama3")
    embedding_model = st.text_input("Embedding model", value="nomic-embed-text")
    top_k = st.selectbox("Top K retrieved chunks", [3, 4, 5], index=1)

    st.markdown("### Actions")
    if st.button("Clear database"):
        clear_vector_db()
        st.session_state.results = []
        st.session_state.processed_files = []
        st.success("Vector database cleared.")

job_description = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste the full job description here..."
)

uploaded_files = st.file_uploader(
    "Upload CV files",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Build Vector Store", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload at least one CV.")
        else:
            saved_paths = []
            for uploaded_file in uploaded_files:
                file_path = save_uploaded_file(uploaded_file)
                saved_paths.append(file_path)

            build_vector_store(saved_paths, embedding_model=embedding_model)
            st.session_state.processed_files = [f.name for f in uploaded_files]
            st.success("Vector store built successfully.")

with col2:
    if st.button("Evaluate Candidates", use_container_width=True):
        if not job_description.strip():
            st.error("Please enter a job description.")
        elif not st.session_state.processed_files:
            st.error("Please build the vector store first.")
        else:
            vector_store = get_vector_store(embedding_model=embedding_model)
            results = []

            progress = st.progress(0)
            total = len(st.session_state.processed_files)

            