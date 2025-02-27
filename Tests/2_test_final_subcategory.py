import requests
import configparser
import json
from collections import defaultdict
import time

# 📌 Load API Configuration
config = configparser.ConfigParser()
config.read(r"C:\Users\alima\.config\pybliometrics.cfg")

API_KEY = config['Authentication']['APIKey']
INST_TOKEN = config['Authentication']['InstToken']

# ✅ Define Query Parameters
AUTHOR_ID = '35726950800'
start_year = 2019
end_year = 2025
search_url = "https://api.elsevier.com/content/search/scopus"
abstract_url = "https://api.elsevier.com/content/abstract/scopus_id/"

headers = {
    "X-ELS-APIKey": API_KEY,
    "X-ELS-Insttoken": INST_TOKEN,
    "Accept": "application/json"
}

# ✅ Step 1: Get All Document IDs for the Author (Limited to 10 at a Time)
batch_size = 10  # 🚀 Small batch to avoid API limits
offset = 0
all_scopus_ids = []

while True:
    params = {
        "query": f"AU-ID({AUTHOR_ID}) AND PUBYEAR > {start_year-1} AND PUBYEAR < {end_year+1}",
        "count": str(batch_size),  # 🚀 Limit batch size
        "start": str(offset),
        "view": "COMPLETE"
    }

    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"❌ Scopus API Error: {response.status_code} - {response.text}")
        break

    data = response.json()
    entries = data.get("search-results", {}).get("entry", [])

    if not entries:
        print("✅ No more documents found. Stopping batch processing.")
        break

    # ✅ Extract SCOPUS_IDs
    batch_scopus_ids = [entry.get("dc:identifier", "").replace("SCOPUS_ID:", "").strip() for entry in entries if entry.get("dc:identifier")]
    
    if not batch_scopus_ids:
        print("⚠️ No SCOPUS_IDs found in this batch.")
        break

    all_scopus_ids.extend(batch_scopus_ids)
    offset += batch_size

    # 🚀 Respect API Rate Limits
    time.sleep(2)  # ✅ Wait 2 seconds to avoid rate limit issues

# ✅ Step 2: Query Abstract API in Batches
subcategory_data = defaultdict(int)
subcategory_asjc_codes = {}

print(f"\n🔹 Total SCOPUS_IDs to Process: {len(all_scopus_ids)}\n")

for index, scopus_id in enumerate(all_scopus_ids, start=1):
    print(f"🔍 Fetching subject areas for SCOPUS_ID {scopus_id} ({index}/{len(all_scopus_ids)})...")

    abstract_response = requests.get(f"{abstract_url}{scopus_id}", headers=headers)

    if abstract_response.status_code == 429:  # 🚀 Too Many Requests Error
        print("⚠️ Rate limit reached. Pausing for 10 seconds...")
        time.sleep(10)  # Wait longer before retrying
        continue

    if abstract_response.status_code != 200:
        print(f"⚠️ Failed to retrieve SCOPUS_ID {scopus_id}. Skipping...")
        continue

    abstract_data = abstract_response.json()

    # ✅ Extract Subject Areas
    subject_areas = abstract_data.get("abstracts-retrieval-response", {}).get("subject-areas", {}).get("subject-area", [])

    if isinstance(subject_areas, list):
        for subject in subject_areas:
            subject_name = subject.get("$", "").strip()
            asjc_code = subject.get("@code", "N/A")
            if subject_name:
                subcategory_data[subject_name] += 1
                subcategory_asjc_codes[subject_name] = asjc_code
    elif isinstance(subject_areas, dict):
        subject_name = subject_areas.get("$", "").strip()
        asjc_code = subject_areas.get("@code", "N/A")
        if subject_name:
            subcategory_data[subject_name] += 1
            subcategory_asjc_codes[subject_name] = asjc_code

    # ✅ Respect API Rate Limits (Wait 2 Seconds Between Requests)
    time.sleep(2)

# ✅ Step 3: Format Results
subcategory_results = [
    {
        "ASJC Code": subcategory_asjc_codes.get(subject, "N/A"),
        "Category": subject,
        "Scholarly Output": count
    }
    for subject, count in subcategory_data.items()
]

# ✅ Display Results
print("\n🔹 Subcategories Retrieved:")
print(json.dumps(subcategory_results, indent=4))
