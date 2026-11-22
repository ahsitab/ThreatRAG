import streamlit as st
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from rag.ingestion import KnowledgeBaseManager

st.set_page_config(page_title="ThreatRAG - Knowledge Manager", page_icon="🗄️", layout="wide")

st.title("🗄️ Knowledge Base Lifecycle & Updatable Index")
st.markdown("Manage, ingest, refresh, and inspect documents within the persistent ChromaDB and BM25 vector indices.")

@st.cache_resource
def get_kb():
    return KnowledgeBaseManager()

kb = get_kb()
status = kb.get_status()

# Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Indexed Chunks", f"{status.get('total_chunks', 0):,}")
m2.metric("Total Documents Tracked", f"{status.get('total_documents', 0):,}")
m3.metric("Embedding Dimension", f"{status.get('vector_dimension', 384)}")
m4.metric("Engine Status", status.get("status", "ready").upper())

st.markdown("---")

tab_upload, tab_manage, tab_refresh = st.tabs(["📥 Ingest New Document", "📋 Document Catalog", "🔄 Index Synchronization"])

with tab_upload:
    st.subheader("Ingest Single Security Document or Advisory")
    with st.form("upload_form"):
        doc_title = st.text_input("Document Title", placeholder="e.g., CISA Alert AA24-110A: Critical Infrastructure DDoS Targeting")
        doc_type = st.selectbox("Document Category:", ["advisory", "incident", "threat_report", "mitre_technique", "policy"])
        doc_url = st.text_input("Source URL or Reference", value="https://www.cisa.gov/news-events/cybersecurity-advisories")
        att_ck_tag = st.text_input("Associated ATT&CK ID (Optional)", placeholder="e.g., T1498.001")
        doc_content = st.text_area(
            "Document Text / Markdown Content:",
            placeholder="Paste raw cybersecurity advisory, threat intelligence report, or technical incident summary here...",
            height=200
        )
        submitted = st.form_submit_button("📥 Ingest Document", type="primary")

        if submitted:
            if not doc_title.strip() or not doc_content.strip():
                st.error("Please provide both a document title and content body.")
            else:
                with st.spinner("Chunking, embedding, and synchronizing with vector & BM25 indices..."):
                    res = kb.add_document(
                        title=doc_title,
                        content=doc_content,
                        source_type=doc_type,
                        source_url=doc_url,
                        att_ck_id=att_ck_tag if att_ck_tag.strip() else None
                    )
                st.success(f"Successfully indexed document `{res.get('document_id')}` creating {res.get('chunks_created')} new knowledge chunks!")

with tab_manage:
    st.subheader("Active Document Provenance Catalog")
    docs = kb.list_documents()
    if docs:
        df_docs = pd.DataFrame(docs)
        st.dataframe(df_docs, use_container_width=True, hide_index=True)
        
        st.markdown("#### Delete Document from Index")
        del_id = st.selectbox("Select Document ID to Remove:", [d["document_id"] for d in docs])
        if st.button("🗑️ Remove Document & Prune Chunks", type="secondary"):
            with st.spinner("Pruning chunks from vector store and BM25 index..."):
                ok = kb.delete_document(del_id)
            if ok:
                st.success(f"Document `{del_id}` and associated chunks purged.")
                st.rerun()
            else:
                st.error(f"Failed to delete `{del_id}`.")
    else:
        st.info("No manually uploaded documents tracked yet. Core preprocessed chunks are active in index.")

with tab_refresh:
    st.subheader("Full Re-indexing & Corpus Synchronization")
    st.markdown(
        "Synchronize and persist the vector store and BM25 sparse index against the full `data/processed/knowledge_chunks/chunks.json` repository."
    )
    if st.button("🔄 Trigger Full Index Refresh", type="primary"):
        with st.spinner("Rebuilding BM25 tokens and verifying ChromaDB embeddings..."):
            ref_res = kb.refresh_index()
        st.success(f"Index synchronization complete. Total active chunks: {ref_res.get('total_chunks')}.")
