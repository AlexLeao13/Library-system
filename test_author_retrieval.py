import os
from pybliometrics.scopus import AuthorRetrieval

# Forcer Pybliometrics à utiliser le fichier de configuration
os.environ["PYBLIOMETRICS_CONFIG_FILE"] = r"C:\Users\alima\.config\pybliometrics.cfg"

try:
    author_id = "35726950800"  # Exemple d'ID Scopus
    author = AuthorRetrieval(author_id)
    print(f"✔️ Nom de l'auteur : {author.given_name} {author.surname}")
    print(f"✔️ Affiliation actuelle : {author.affiliation_current[0].name if author.affiliation_current else 'Aucune affiliation'}")
except Exception as e:
    print(f"❌ Erreur lors de la récupération des données : {e}")
