import os
import requests

# ✅ Configuration de Scopus
os.environ["PYBLIOMETRICS_CONFIG"] = r"C:\\Users\\alima\\.config\\pybliometrics.cfg"

# 📌 Ta clé API Scopus
API_KEY = "TA_CLE_API_ICI"  # Remplace par ta clé API Scopus

# 📌 ID Scopus de l'auteur
AUTHOR_ID = "35726950800"  # Remplace par un ID d’auteur valide

# 📌 URL pour récupérer les infos de l'auteur
url = f"https://api.elsevier.com/content/author/author_id/{AUTHOR_ID}"

# 📌 Headers pour l'API Scopus
headers = {
    "Accept": "application/json",
    "X-ELS-APIKey": API_KEY
}

# 🔍 Requête API
response = requests.get(url, headers=headers)

# 🔥 Vérifier si la requête est réussie
if response.status_code == 200:
    data = response.json()

    # 📌 Vérifier s'il y a un lien vers SciVal dans la réponse
    if "author-retrieval-response" in data:
        author_data = data["author-retrieval-response"][0]
        
        # Chercher un lien vers SciVal
        scival_link = None
        for link in author_data.get("link", []):
            if "scival" in link["@ref"]:
                scival_link = link["@href"]
                break

        # 🔥 Afficher le lien SciVal si trouvé
        if scival_link:
            print(f"✅ Lien SciVal trouvé : {scival_link}")
        else:
            print("❌ Aucun lien SciVal trouvé pour cet auteur.")

    else:
        print("⚠️ Réponse Scopus invalide. Vérifie ton ID d’auteur.")

else:
    print(f"❌ Erreur API Scopus : {response.status_code}")
