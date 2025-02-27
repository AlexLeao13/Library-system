import os
import requests
import pandas as pd
from datetime import datetime
from openpyxl import Workbook

# ✅ Définition du dossier de sortie
output_dir = r"C:\Users\alima\Desktop\AlexStage\Code_graphique_test_project\output"
os.makedirs(output_dir, exist_ok=True)

# ✅ Configuration de l'API Elsevier (Scopus)
API_KEY = "85c7f7feb66ebceade90364e20252d21"
INST_TOKEN = "477bdb554065fcad05f9c375f5e10cab"
HEADERS = {
    "X-ELS-APIKey": API_KEY,
    "X-ELS-Insttoken": INST_TOKEN,
    "Accept": "application/json"
}

# ======================
# 📊 Récupération des données de l'API Scopus
# ======================
from pybliometrics.scival import AuthorMetrics

def fetch_subject_areas(author_id):
    """ Récupère les Subject Areas et leurs Scholarly Output depuis SciVal API """

    try:
        # 🔍 Récupérer les métriques de SciVal
        metrics = AuthorMetrics(author_id, metric_types="ScholarlyOutput")

        # 🔍 Extraction des données
        subjects_data = []
        for entry in metrics.results:
            subject_area = entry['SubjectArea']['name']  # Ex: Engineering
            subcategory = entry['SubCategory']['name'] if 'SubCategory' in entry else "-"  # Ex: Civil Engineering
            scholarly_output = entry['Metric']['value']  # Nombre d'articles

            # Nettoyage des noms pour éviter les erreurs d'affichage
            subject_area = subject_area.replace(" (all)", "")
            subcategory = subcategory.replace(" (all)", "") if subcategory != "-" else "-"

            # Ajouter à la liste seulement si Scholarly Output > 0
            if scholarly_output > 0:
                subjects_data.append((subject_area, subcategory, scholarly_output))

        # ✅ DEBUG : Afficher la liste propre des Subject Areas avec Scholarly Output
        print("\n🔍 Debug - Liste des Subject Areas et Subcategories avec Scholarly Output:")
        for row in subjects_data:
            print(row)

        return subjects_data

    except Exception as e:
        print(f"❌ Erreur : Impossible de récupérer les Subject Areas depuis SciVal. {str(e)}")
        return []



# ======================
# 📄 Génération du fichier Excel
# ======================
def generate_excel_file(disciplines, excel_path):
    """Crée un fichier Excel contenant Subject Areas, Subcategories et Scholarly Output"""

    # ✅ Création du dataframe
    df = pd.DataFrame(disciplines)

    # ✅ Création d'un nouveau fichier Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Disciplines"

    # ✅ Ajouter les en-têtes
    ws.append(["Subject Area", "Subcategory", "Scholarly Output"])

    # ✅ Ajouter les données
    for row in df.itertuples(index=False):
        ws.append(row)

    # ✅ Sauvegarde du fichier Excel
    wb.save(excel_path)
    print(f"✅ Fichier Excel généré : {excel_path}")

# ======================
# 🔥 Exécution du script
# ======================
def main():
    researcher_name = input("Entrez le nom du chercheur (Format : Nom Prenom) : ").strip()
    last_name, first_name = researcher_name.split(" ", 1)

    # 🔍 Effectuer la requête API pour récupérer l'ID de l'auteur
    url = f"https://api.elsevier.com/content/search/author?query=AUTHLASTNAME({last_name}) AND AUTHFIRST({first_name})"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    # 🏷️ Extraire l'ID du premier auteur trouvé
    author_id = data["search-results"]["entry"][0]['dc:identifier'].split(':')[-1]

    today = datetime.today().strftime('%Y-%m-%d')
    researcher_name_clean = researcher_name.replace(" ", "-")
    excel_output_name = f"{today}_{researcher_name_clean}.xlsx"
    excel_output_path = os.path.join(output_dir, excel_output_name)

    # 🔍 Récupérer les données
    disciplines = fetch_subject_areas(author_id)

    if not disciplines:
        print("❌ Aucune donnée trouvée !")
        return

    # 📄 Générer le fichier Excel
    generate_excel_file(disciplines, excel_output_path)

if __name__ == "__main__":
    main()