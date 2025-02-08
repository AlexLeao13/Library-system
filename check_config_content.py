import configparser

config_path = r"C:\Users\alima\.config\pybliometrics.cfg"
config = configparser.ConfigParser()

config.read(config_path)

print(f"✔️ Lecture du fichier : {config_path}")
print("📂 Sections trouvées :", config.sections())

if "Authentication" not in config or "APIKey" not in config["Authentication"]:
    print("❌ Erreur : La section 'Authentication' ou la clé API est absente.")
else:
    print("✔️ Clé API détectée :", config["Authentication"]["APIKey"])
