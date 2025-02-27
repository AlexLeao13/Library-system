import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
from collections import Counter
from pybliometrics.scopus.author_retrieval import AuthorRetrieval

# ✅ Configuration de l'environnement (Utilisation de pybliometrics.cfg)
os.environ["PYBLIOMETRICS_CONFIG"] = r"C:\\Users\\alima\\.config\\pybliometrics.cfg"

# 🔍 Demander l'ID Scopus de l'auteur
author_id = input("🔍 Entrez l'ID Scopus de l’auteur : ").strip()

# ✅ Récupération des données de l'auteur via Scopus
try:
    author = AuthorRetrieval(author_id)
    print(f"✅ Données récupérées pour l'auteur : {author.indexed_name}")
except Exception as e:
    print(f"❌ Erreur lors de la récupération des données Scopus : {e}")
    exit()

# ✅ API Key (Doit être configurée dans pybliometrics.cfg ou définie ici)
SCOPUS_API_KEY = "YOUR_SCOPUS_API_KEY"  # 🔹 Remplacez par votre clé API si nécessaire

# ✅ Construire la requête API vers Scopus
scopus_url = "https://api.elsevier.com/content/search/scopus"
headers = {
    "X-ELS-APIKey": SCOPUS_API_KEY,
    "Accept": "application/json"
}
params = {
    "query": f"AU-ID({author_id})",  # Recherche des publications de l'auteur
    "count": "200",  # Nombre maximal de publications
    "facets": "subjarea"  # Récupérer les domaines de recherche
}

# ✅ Envoyer la requête GET
response = requests.get(scopus_url, headers=headers, params=params)

# ✅ Vérifier si la requête a réussi
if response.status_code != 200:
    print(f"❌ Erreur API Scopus : {response.status_code} - {response.text}")
    exit()

# ✅ Convertir la réponse en JSON
data = response.json()

# ✅ Extraire les Subject Areas
subject_areas = []
if "search-results" in data and "facet" in data["search-results"]:
    for facet in data["search-results"]["facet"]:
        if facet["@name"] == "subjarea":  # Récupération des sujets
            for category in facet["category"]:
                subject_areas.append((category["@name"], int(category["@count"])))

# ✅ Vérification si les données ont bien été récupérées
if not subject_areas:
    print("🚨 Aucun Subject Area trouvé via l'API Scopus.")
    exit()

# ✅ Création du DataFrame avec le format attendu
df_subjects = pd.DataFrame(subject_areas, columns=["Subject Area", "Scholarly Output"])
df_subjects = df_subjects.sort_values(by="Scholarly Output", ascending=False)

# 📂 Définition du dossier de sortie
output_folder = r"C:\\Users\\alima\\Desktop\\AlexStage\\Code_graphique_test_project\\output"
os.makedirs(output_folder, exist_ok=True)

# 📌 Générer un graphique des domaines de recherche
plt.figure(figsize=(10, 6))
plt.bar(df_subjects["Subject Area"], df_subjects["Scholarly Output"], color='skyblue')
plt.xticks(rotation=45, ha="right")
plt.xlabel("Subject Areas")
plt.ylabel("Scholarly Output (Nb. of Publications)")
plt.title(f"Subject Areas of {author.indexed_name}")
plt.tight_layout()

# 📂 Sauvegarde du graphique
graph_file = os.path.join(output_folder, f"subject_areas_{author_id}.png")
plt.savefig(graph_file)
plt.show()

# 📌 Sauvegarde des résultats en Excel
excel_file = os.path.join(output_folder, f"subject_areas_{author_id}.xlsx")
df_subjects.to_excel(excel_file, index=False)

print(f"✅ Extraction terminée ! Résultats enregistrés dans '{excel_file}'.")
