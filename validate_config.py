import os
from pybliometrics.scopus.utils.constants import CONFIG_FILE

print(f"🔍 Pybliometrics cherche le fichier de configuration ici : {CONFIG_FILE}")

# Vérifier si le fichier existe réellement
if os.path.exists(CONFIG_FILE):
    print("✔️ Le fichier existe bien.")
else:
    print("❌ Le fichier est introuvable.")
