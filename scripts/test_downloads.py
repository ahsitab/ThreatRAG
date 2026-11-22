import urllib.request
import json
import hashlib
import os

print("Testing direct HTTPS downloads...")

# Test CISA KEV
cisa_url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
try:
    req = urllib.request.Request(cisa_url, headers={'User-Agent': 'ThreatRAG-Research-Agent/1.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(f"CISA KEV download success: {data.get('count')} vulnerabilities listed, catalogVersion: {data.get('catalogVersion')}")
except Exception as e:
    print(f"CISA KEV download error: {e}")

# Test MITRE ATT&CK Enterprise STIX
mitre_url = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json"
try:
    req = urllib.request.Request(mitre_url, headers={'User-Agent': 'ThreatRAG-Research-Agent/1.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        header_sample = resp.read(1024)
        print(f"MITRE ATT&CK download accessible: read {len(header_sample)} bytes sample header")
except Exception as e:
    print(f"MITRE ATT&CK download error: {e}")
