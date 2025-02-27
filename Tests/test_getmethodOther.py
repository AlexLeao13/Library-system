import os
from pybliometrics.scival.author_lookup import AuthorLookup

# 📌 ID de test
AUTHOR_ID = "35726950800"

# ✅ Définition du chemin de configuration SciVal
os.environ["PYBLIOMETRICS_CONFIG"] = r"C:\Users\alima\.config\pybliometrics.cfg"

# 📌 Récupération des métriques disponibles
author = AuthorLookup(author_id=AUTHOR_ID, refresh=True)

# 📌 Affichage des métriques disponibles
print("\n✅ **Métriques disponibles pour get_metrics_Other() :**")
print(author.metricType_liste)
