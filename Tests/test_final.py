import requests
import configparser
import json
from collections import defaultdict

# 📌 Charger les configurations API
config = configparser.ConfigParser()
config.read(r"C:\Users\alima\.config\pybliometrics.cfg")  # Utilise le chemin Windows

API_KEY = config['Authentication']['APIKey']
INST_TOKEN = config['Authentication']['InstToken']

# ✅ Définition des paramètres
AUTHOR_ID = '35726950800'
start_year = 2019
end_year = 2025
url = "https://api.elsevier.com/content/search/scopus"

headers = {
    "X-ELS-APIKey": API_KEY,
    "X-ELS-Insttoken": INST_TOKEN,
    "Accept": "application/json"
}

params = {
    "query": f"AU-ID({AUTHOR_ID}) AND PUBYEAR > {start_year-1} AND PUBYEAR < {end_year+1}",
    "facets": "subjarea(count=100)",  # Demander jusqu'à 100 facettes de domaines de publication
    "count": "0"  # Nous n'avons besoin que des facettes, pas des documents
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    facets = data['search-results'].get('facet', {}).get('category', [])
    
    formatted_results = []
    subcategory_data = defaultdict(int)  # 📌 Stocker les résultats des sous-catégories
    subcategory_asjc_codes = {}  # 📌 Stocker les codes ASJC des sous-catégories
    
    print("\n🔹 Récupération des Catégories Principales...")

    for facet in facets:
        main_asjc_code = facet.get('id', 'No ID available')
        main_category = f"{facet.get('value', 'No value available')} - {facet['label']}"
        scholarly_output = int(facet['hitCount'])

        formatted_results.append({
            "ASJC Code": main_asjc_code,
            "Category": main_category,
            "Scholarly Output": scholarly_output
        })

        # ✅ Rechercher les publications de cette catégorie et récupérer les sous-catégories
        print(f"   ➜ Recherche des sous-catégories pour {main_category}...")
        sub_params = {
            "query": f"SUBJAREA({facet['value']}) AND PUBYEAR > {start_year-1} AND PUBYEAR < {end_year+1}",
            "view": "COMPLETE",  # Récupérer tous les détails des publications
            "count": "100"  # Augmenter le nombre de résultats
        }
        sub_response = requests.get(url, headers=headers, params=sub_params)

        if sub_response.status_code == 200:
            sub_data = sub_response.json()
            print(json.dumps(sub_data, indent=4))  # Debug: Print the API response
            for entry in sub_data.get('search-results', {}).get('entry', []):
                if 'subject-areas' in entry:
                    subjects = entry['subject-areas'].split(";") if entry['subject-areas'] else []
                    for subject in subjects:
                        subject = subject.strip()
                        if subject:
                            subcategory_data[subject] += 1
                            subcategory_asjc_codes[subject] = entry.get('asjc', 'N/A')
                else:
                    print(f"⚠️ Aucune sous-catégorie trouvée pour {main_category}.")

    # ✅ Ajouter les sous-catégories au format final
    subcategory_results = []
    print("\n🔹 Agrégation des sous-catégories...\n")
    for subject, count in subcategory_data.items():
        subcategory_results.append({
            "ASJC Code": subcategory_asjc_codes.get(subject, 'N/A'),  # Utiliser le code ASJC de la sous-catégorie
            "Category": subject,
            "Scholarly Output": count
        })

    # ✅ Fusionner les catégories principales et sous-catégories
    final_results = formatted_results + subcategory_results

    # ✅ Affichage des résultats formatés
    print(json.dumps(final_results, indent=4))

else:
    print(f"❌ Erreur API Scopus : {response.status_code} - {response.text}")
