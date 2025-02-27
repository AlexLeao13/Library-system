import os
from pybliometrics.scival.author_lookup import AuthorLookup

os.environ["PYBLIOMETRICS_CONFIG"] = r"C:\Users\alima\.config\pybliometrics.cfg"

# 📌 ID de test
AUTHOR_ID = "35726950800"

author = AuthorLookup(AUTHOR_ID, refresh=True)

# 🔍 Liste toutes les méthodes disponibles dans AuthorLookup
methods = [method for method in dir(author) if not method.startswith("_")]

print("✅ **Méthodes disponibles dans AuthorLookup :**")
for method in methods:
    print(f"- {method}")
