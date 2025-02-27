import os
from pybliometrics.scopus import ScopusSearch

# 🔧 Forcer l'utilisation du bon fichier de configuration
config_path = r"C:\Users\alima\.config\pybliometrics.cfg"
os.environ["PYBLIOMETRICS_CONFIG_FILE"] = config_path

# ✅ Vérification que le fichier de configuration existe
if not os.path.exists(config_path):
    print("❌ Fichier de configuration introuvable. Vérifiez que Pybliometrics est bien configuré.")
    exit(1)

print(f"✔️ Utilisation du fichier de configuration : {config_path}")

# 🔍 Test de recherche sur Scopus
query = "AUTHOR-NAME(Silvio Melhado)"
try:
    search = ScopusSearch(query, subscriber=False)  # Mode non-abonné
    results_count = search.get_results_size()
    print(f"✔️ Nombre de résultats trouvés : {results_count}")
except Exception as e:
    print(f"❌ Une erreur s'est produite : {e}")
