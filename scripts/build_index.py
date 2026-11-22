"""
scripts/build_index.py
======================
Builds and persists the ChromaDB vector database and BM25 sparse index for ThreatRAG.
"""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.ingestion import KnowledgeBaseManager

def main():
    force = "--force" in sys.argv
    print("=" * 70)
    print("ThreatRAG: Building Vector Store and BM25 Retrieval Indexes")
    print(f"Force rebuild: {force}")
    print("=" * 70)

    manager = KnowledgeBaseManager()
    res = manager.initialize_from_preprocessed(force_rebuild=force)
    print("Result:", res)
    status = manager.get_status()
    print("Knowledge Base Status:", status)
    print("=" * 70)

if __name__ == "__main__":
    main()
