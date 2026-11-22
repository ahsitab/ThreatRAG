import urllib.request
import json

print("Checking candidate intrusion dataset sources...")

# Check Hugging Face datasets API for CIC-IDS2017 or UNSW-NB15
urls = [
    ("UNSW-NB15 CSV on GitHub/Raw", "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/README.md"),
    ("Hugging Face cicids2017 parquet/csv", "https://huggingface.co/api/datasets/cicids2017"),
    ("Hugging Face unsw-nb15", "https://huggingface.co/api/datasets/argilla/unsw-nb15"),
    ("Stratosphere IPS / Malware capture", "https://huggingface.co/api/datasets/m4r10/cicids2017"),
]

for name, url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ThreatRAG-Research-Agent/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"  [OK] {name}: HTTP {resp.status}")
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
