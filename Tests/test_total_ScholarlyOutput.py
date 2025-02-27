import requests
import configparser

# 📌 Charger la configuration depuis pybliometrics.cfg
config = configparser.ConfigParser()
config.read(r"C:\Users\alima\.config\pybliometrics.cfg")

API_KEY = config["Authentication"]["APIKey"]
INST_TOKEN = config["Authentication"]["InstToken"]

# ✅ Vérifier si l'API Key et le Token sont bien récupérés
if not API_KEY or not INST_TOKEN:
    print("❌ Erreur : Impossible de récupérer l'API Key ou le Token Institutionnel depuis pybliometrics.cfg")
    exit()

print(f"✅ API Key récupérée : {API_KEY[:5]}******")
print(f"✅ Institution Token récupéré : {INST_TOKEN[:5]}******\n")

# ✅ Demander l'ID de l’auteur
AUTHOR_ID = input("🔍 Entrez l'ID Scopus de l’auteur : ").strip()

if not AUTHOR_ID:
    print("❌ Erreur : L'ID de l'auteur ne peut pas être vide.")
    exit()

# ✅ Définition de l'URL de l'API Scopus pour récupérer le total des publications AVEC FILTRE DE DATE
SCOPUS_SEARCH_URL = "https://api.elsevier.com/content/search/scopus"

params = {
    "query": f"AU-ID({AUTHOR_ID})",  # Recherche des publications de l’auteur
    "date": "2019-2025",  # 📌 Filtrage par année 2019-2025
    "count": "0"  # On ne veut que le total, pas les détails des publications
}

headers = {
    "X-ELS-APIKey": API_KEY,
    "X-ELS-Insttoken": INST_TOKEN,
    "Accept": "application/json"
}

# ✅ Envoi de la requête
response = requests.get(SCOPUS_SEARCH_URL, headers=headers, params=params)

# ✅ Vérification du statut de la réponse
if response.status_code == 200:
    data = response.json()
    try:
        total_publications = int(data["search-results"]["opensearch:totalResults"])
        print(f"\n✅ Nombre total de publications (2019-2025) pour l'auteur {AUTHOR_ID} : {total_publications}")
    except KeyError:
        print("⚠️ Impossible de récupérer le nombre total de publications. Vérifiez l’API Key et l’ID de l’auteur.")
else:
    print(f"❌ Erreur API Scopus : {response.status_code} - {response.text}")
