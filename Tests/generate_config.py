from pybliometrics.scopus import utils

try:
    # Crée le fichier de configuration
    utils.create_config()
    print("✔️ Fichier de configuration créé avec succès.")

    print("Veuillez éditer manuellement le fichier pour ajouter votre clé API et votre token.")
    print("Le fichier se trouve généralement ici : C:\\Users\\alima\\.config\\pybliometrics.cfg")

except Exception as e:
    print(f"Erreur lors de la création du fichier de configuration : {e}")
