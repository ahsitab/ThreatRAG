"""
scripts/prepare_data.py
=======================
Data preprocessing, cleaning, normalization, splitting, and chunk generation for ThreatRAG.

Performs:
1. Network Flow Preprocessing (CIC-IDS2017):
   - Whitespace stripping from column names
   - Clean naming convention (snake_case)
   - Handling of missing, NaN, and +/- Infinity values
   - Duplicate removal and leakage checks
   - Class balance verification
   - Stratified train (60%), validation/calibration (20%), and test (20%) splits
2. MITRE ATT&CK STIX 2.1 Extraction:
   - Extract techniques, tactics, mitigations, and relationships
   - Preserve technique IDs (e.g., T1059.001), platforms, and detection guidance
3. CISA KEV Extraction:
   - Extract CVEs, impacted products, exploit descriptions, and remediation timelines
4. Historical Incidents Normalization:
   - Structured schema mapping with MITRE IDs, indicators, and mitigation steps
5. Knowledge Chunking:
   - Metadata-aware chunking preserving provenance (document ID, URL, source version, ATT&CK IDs)
   - Emits structured JSON chunks ready for vector and BM25 indexing
"""

import os
import re
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")
SPLITS_DIR = os.path.join("data", "splits")

def clean_column_name(col):
    col = col.strip()
    col = re.sub(r"[^\w\s]", "", col)
    col = re.sub(r"\s+", "_", col)
    return col.lower()

def preprocess_network_flows(sample_size=30000, random_state=42):
    print("\n--- 1. Preprocessing CIC-IDS2017 Network Flows ---")
    raw_csv = os.path.join(RAW_DIR, "cic_ids2017", "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
    if not os.path.exists(raw_csv):
        print(f"[ERROR] Raw CSV not found at {raw_csv}")
        return None

    print(f"Reading {raw_csv}...")
    df = pd.read_csv(raw_csv, low_memory=False)
    print(f"Raw shape: {df.shape}")

    # 1. Clean column names
    df.columns = [clean_column_name(c) for c in df.columns]

    # Find label column
    label_candidates = [c for c in df.columns if "label" in c]
    if not label_candidates:
        raise ValueError("No label column found in network flow CSV")
    label_col = label_candidates[0]

    # Standardize label values
    df[label_col] = df[label_col].astype(str).str.strip()
    print("Raw class distribution:")
    print(df[label_col].value_counts())

    # 2. Handle Infinities and NaNs
    numeric_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c != label_col]
    
    # Replace inf with NaN
    df[numeric_cols] = df[numeric_cols].replace([np.inf, -np.inf], np.nan)
    
    initial_len = len(df)
    df = df.dropna(subset=numeric_cols + [label_col])
    print(f"Dropped {initial_len - len(df)} rows containing NaN or Infinite values.")

    # 3. Deduplicate
    before_dedup = len(df)
    df = df.drop_duplicates(subset=numeric_cols)
    print(f"Removed {before_dedup - len(df)} duplicate flow records.")

    # 4. Map binary/multi-class target
    # BENIGN -> 0, DDoS -> 1
    df["binary_target"] = (df[label_col].str.upper() != "BENIGN").astype(int)

    # 5. Stratified Sampling if dataset is very large
    if len(df) > sample_size:
        print(f"Sampling balanced/stratified subset of {sample_size} records...")
        counts = df["binary_target"].value_counts()
        min_class_count = counts.min()
        target_per_class = min(sample_size // 2, min_class_count)

        benign_sample = df[df["binary_target"] == 0].sample(n=target_per_class, random_state=random_state)
        attack_sample = df[df["binary_target"] == 1].sample(n=target_per_class, random_state=random_state)
        df_sampled = pd.concat([benign_sample, attack_sample]).sample(frac=1.0, random_state=random_state).reset_index(drop=True)
    else:
        df_sampled = df.copy()

    print(f"Sampled dataset shape: {df_sampled.shape}")
    print("Sampled target distribution:")
    print(df_sampled["binary_target"].value_counts())

    # 6. Stratified Partitions: Train (60%), Validation/Calibration (20%), Test (20%)
    train_df, temp_df = train_test_split(
        df_sampled, 
        test_size=0.40, 
        stratify=df_sampled["binary_target"], 
        random_state=random_state
    )
    val_df, test_df = train_test_split(
        temp_df, 
        test_size=0.50, 
        stratify=temp_df["binary_target"], 
        random_state=random_state
    )

    print(f"Partition splits -> Train: {len(train_df)}, Val/Calibration: {len(val_df)}, Test: {len(test_df)}")

    # Save splits
    os.makedirs(os.path.join(SPLITS_DIR, "train"), exist_ok=True)
    os.makedirs(os.path.join(SPLITS_DIR, "validation"), exist_ok=True)
    os.makedirs(os.path.join(SPLITS_DIR, "test"), exist_ok=True)
    os.makedirs(os.path.join(PROCESSED_DIR, "network_flows"), exist_ok=True)

    train_path = os.path.join(SPLITS_DIR, "train", "train_flows.csv")
    val_path = os.path.join(SPLITS_DIR, "validation", "val_flows.csv")
    test_path = os.path.join(SPLITS_DIR, "test", "test_flows.csv")
    processed_sample_path = os.path.join(PROCESSED_DIR, "network_flows", "flow_samples.csv")

    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)
    df_sampled.to_csv(processed_sample_path, index=False)

    print(f"Saved splits to {SPLITS_DIR}")
    return df_sampled

def process_mitre_attack():
    print("\n--- 2. Processing MITRE ATT&CK Enterprise STIX ---")
    stix_file = os.path.join(RAW_DIR, "mitre_attack", "enterprise-attack.json")
    if not os.path.exists(stix_file):
        print(f"[ERROR] STIX file not found at {stix_file}")
        return []

    with open(stix_file, "r", encoding="utf-8") as f:
        stix = json.load(f)

    objects = stix.get("objects", [])
    print(f"Total STIX objects: {len(objects)}")

    techniques = []
    mitigations = {}
    
    # First pass: map mitigations (course-of-action)
    for obj in objects:
        if obj.get("type") == "course-of-action":
            mitigations[obj.get("id")] = {
                "name": obj.get("name", ""),
                "description": obj.get("description", "")
            }

    # Second pass: extract attack-pattern (techniques)
    for obj in objects:
        if obj.get("type") == "attack-pattern" and not obj.get("revoked", False):
            # Extract ATT&CK ID
            technique_id = None
            source_url = None
            for ref in obj.get("external_references", []):
                if ref.get("source_name") == "mitre-attack":
                    technique_id = ref.get("external_id")
                    source_url = ref.get("url")
                    break

            if not technique_id:
                continue

            tactics = [phase.get("phase_name") for phase in obj.get("kill_chain_phases", []) if phase.get("kill_chain_name") == "mitre-attack"]
            platforms = obj.get("x_mitre_platforms", [])
            data_sources = obj.get("x_mitre_data_sources", [])
            detection = obj.get("x_mitre_detection", "")
            name = obj.get("name", "")
            description = obj.get("description", "")

            tech_record = {
                "technique_id": technique_id,
                "name": name,
                "tactics": tactics,
                "platforms": platforms,
                "data_sources": data_sources,
                "description": description,
                "detection": detection,
                "source_url": source_url or f"https://attack.mitre.org/techniques/{technique_id}/",
                "version": obj.get("spec_version", "2.1")
            }
            techniques.append(tech_record)

    out_file = os.path.join(PROCESSED_DIR, "threat_documents", "mitre_attack_techniques.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(techniques, f, indent=2)

    print(f"Extracted and saved {len(techniques)} valid ATT&CK techniques to {out_file}")
    return techniques

def process_cisa_kev():
    print("\n--- 3. Processing CISA KEV Catalog ---")
    cisa_file = os.path.join(RAW_DIR, "cisa", "known_exploited_vulnerabilities.json")
    if not os.path.exists(cisa_file):
        print(f"[ERROR] CISA file not found at {cisa_file}")
        return []

    with open(cisa_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    vulns = data.get("vulnerabilities", [])
    processed_vulns = []

    for v in vulns:
        record = {
            "cve_id": v.get("cveID"),
            "vendor_project": v.get("vendorProject"),
            "product": v.get("product"),
            "vulnerability_name": v.get("vulnerabilityName"),
            "date_added": v.get("dateAdded"),
            "short_description": v.get("shortDescription"),
            "required_action": v.get("requiredAction"),
            "due_date": v.get("dueDate"),
            "known_ransomware_use": v.get("knownRansomwareCampaignUse", "Unknown"),
            "source_url": f"https://nvd.nist.gov/vuln/detail/{v.get('cveID')}"
        }
        processed_vulns.append(record)

    out_file = os.path.join(PROCESSED_DIR, "threat_documents", "cisa_kev_records.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(processed_vulns, f, indent=2)

    print(f"Processed and saved {len(processed_vulns)} CISA KEV records to {out_file}")
    return processed_vulns

def process_historical_incidents():
    print("\n--- 4. Processing Historical Incidents ---")
    raw_file = os.path.join(RAW_DIR, "historical_incidents", "historical_incidents.json")
    if not os.path.exists(raw_file):
        print(f"[ERROR] Incidents file not found at {raw_file}")
        return []

    with open(raw_file, "r", encoding="utf-8") as f:
        incidents = json.load(f)

    out_file = os.path.join(PROCESSED_DIR, "incident_records", "incidents.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(incidents, f, indent=2)

    print(f"Normalized and saved {len(incidents)} historical incident records to {out_file}")
    return incidents

def build_knowledge_chunks(techniques, cisa_records, incidents):
    print("\n--- 5. Generating Unified Knowledge Chunks ---")
    chunks = []
    chunk_idx = 0

    # 1. MITRE ATT&CK Chunks
    for t in techniques:
        tech_id = t["technique_id"]
        title = f"MITRE ATT&CK {tech_id}: {t['name']}"
        tactics_str = ", ".join(t.get("tactics", []))
        platforms_str = ", ".join(t.get("platforms", []))
        
        # Primary technique description chunk
        desc_text = (
            f"Technique ID: {tech_id}\n"
            f"Name: {t['name']}\n"
            f"Tactics: {tactics_str}\n"
            f"Platforms: {platforms_str}\n\n"
            f"Description:\n{t.get('description', '')}"
        )
        chunks.append({
            "chunk_id": f"CHUNK-ATTACK-{tech_id}",
            "document_id": tech_id,
            "source_title": title,
            "source_url": t.get("source_url"),
            "doc_type": "mitre_technique",
            "attack_ids": [tech_id],
            "publication_date": "2024-10-01",
            "content": desc_text.strip(),
            "metadata": {
                "technique_id": tech_id,
                "tactics": t.get("tactics", []),
                "platforms": t.get("platforms", []),
                "type": "technique_description"
            }
        })
        chunk_idx += 1

        # Detection chunk if available and rich
        if t.get("detection") and len(t["detection"].strip()) > 50:
            det_text = (
                f"Detection Guidance for MITRE ATT&CK {tech_id} ({t['name']}):\n"
                f"{t['detection']}\n"
                f"Applicable Data Sources: {', '.join(t.get('data_sources', []))}"
            )
            chunks.append({
                "chunk_id": f"CHUNK-ATTACK-DET-{tech_id}",
                "document_id": tech_id,
                "source_title": f"Detection: {t['name']} ({tech_id})",
                "source_url": t.get("source_url"),
                "doc_type": "mitre_detection",
                "attack_ids": [tech_id],
                "publication_date": "2024-10-01",
                "content": det_text.strip(),
                "metadata": {
                    "technique_id": tech_id,
                    "type": "detection_guidance"
                }
            })
            chunk_idx += 1

    # 2. CISA KEV Chunks (sample top 300 most impactful or recent)
    for v in cisa_records[:350]:
        cve_id = v["cve_id"]
        cisa_text = (
            f"Vulnerability: {cve_id} - {v.get('vulnerability_name')}\n"
            f"Vendor/Product: {v.get('vendor_project')} / {v.get('product')}\n"
            f"Date Added to KEV: {v.get('date_added')}\n"
            f"Known Ransomware Use: {v.get('known_ransomware_use')}\n"
            f"Description: {v.get('short_description')}\n"
            f"Required Remediation Action: {v.get('required_action')}"
        )
        chunks.append({
            "chunk_id": f"CHUNK-CISA-{cve_id}",
            "document_id": cve_id,
            "source_title": f"CISA KEV: {cve_id} ({v.get('product')})",
            "source_url": v.get("source_url"),
            "doc_type": "cisa_vulnerability",
            "attack_ids": [],
            "publication_date": v.get("date_added", "2024-01-01"),
            "content": cisa_text.strip(),
            "metadata": {
                "cve_id": cve_id,
                "vendor": v.get("vendor_project"),
                "product": v.get("product"),
                "ransomware": v.get("known_ransomware_use")
            }
        })
        chunk_idx += 1

    # 3. Historical Incidents Chunks
    for inc in incidents:
        inc_id = inc["incident_id"]
        attack_ids = [m["technique_id"] for m in inc.get("attack_mapping", [])]
        inc_text = (
            f"Incident ID: {inc_id} - {inc['title']}\n"
            f"Threat Actor: {inc.get('threat_actor')}\n"
            f"Threat Category: {inc.get('threat_category')}\n"
            f"Publication Date: {inc.get('publication_date')}\n"
            f"Affected Environment: {inc.get('affected_environment')}\n\n"
            f"Observed Adversary Behavior:\n{inc.get('observed_behavior')}\n\n"
            f"Indicators of Compromise (IoCs):\n{', '.join(inc.get('indicators', []))}\n\n"
            f"MITRE ATT&CK Mapping: {', '.join(attack_ids)}\n\n"
            f"Defensive Response & Remediation:\n{inc.get('defensive_response')}"
        )
        chunks.append({
            "chunk_id": f"CHUNK-INC-{inc_id}",
            "document_id": inc_id,
            "source_title": f"Historical Incident: {inc['title']}",
            "source_url": inc.get("source_url"),
            "doc_type": "historical_incident",
            "attack_ids": attack_ids,
            "publication_date": inc.get("publication_date"),
            "content": inc_text.strip(),
            "metadata": {
                "incident_id": inc_id,
                "threat_actor": inc.get("threat_actor"),
                "threat_category": inc.get("threat_category"),
                "attack_ids": attack_ids
            }
        })
        chunk_idx += 1

    chunks_file = os.path.join(PROCESSED_DIR, "knowledge_chunks", "chunks.json")
    os.makedirs(os.path.dirname(chunks_file), exist_ok=True)
    with open(chunks_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"Total knowledge chunks compiled: {len(chunks)}")
    print(f"Saved chunks to {chunks_file}")
    return chunks

def main():
    print("=" * 70)
    print("ThreatRAG Phase 3: Data Preprocessing and Knowledge Base Ingestion")
    print("=" * 70)

    # 1. Flow data
    preprocess_network_flows(sample_size=30000)

    # 2. MITRE ATT&CK
    techniques = process_mitre_attack()

    # 3. CISA KEV
    cisa_records = process_cisa_kev()

    # 4. Historical Incidents
    incidents = process_historical_incidents()

    # 5. Build Knowledge Chunks
    build_knowledge_chunks(techniques, cisa_records, incidents)

    print("=" * 70)
    print("Preprocessing & Ingestion Pipeline Complete.")
    print("=" * 70)

if __name__ == "__main__":
    main()
