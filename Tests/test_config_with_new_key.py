from pybliometrics.scopus.utils import get_config

try:
    config = get_config()
    print("✔️ Configuration actuelle :")
    print(config.get("Authentication", "APIKey"))
except Exception as e:
    print(f"❌ Erreur lors de la lecture du fichier de configuration : {e}")
