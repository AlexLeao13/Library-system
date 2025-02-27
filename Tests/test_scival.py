import os
import json
from pybliometrics.scival.author_lookup import AuthorLookup
from pybliometrics.scival.utils import get_api_key

# ✅ Définition du chemin de configuration SciVal
os.environ["PYBLIOMETRICS_CONFIG"] = r"C:\Users\alima\.config\pybliometrics.cfg"

# 📌 ID de test connu
AUTHOR_ID = "35726950800"

def fetch_scival_subject_areas(author_id):
    """ Récupère les Subject Areas et leurs Scholarly Output depuis SciVal. """
    print(f"🔍 Récupération des Subject Areas pour l'auteur {author_id}...")

    # ✅ Vérification de la clé API SciVal
    print("🔍 Vérification de la clé API SciVal...")
    api_key = get_api_key()
    
    if not api_key:
        print("❌ Aucune clé API détectée ! Vérifiez votre configuration `pybliometrics.cfg`.")
        return None
    else:
        print(f"✅ Clé API détectée : {api_key}")

    try:
        author = AuthorLookup(author_id=author_id, refresh=True)
        print("✅ Données récupérées avec succès depuis SciVal")  
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des données SciVal : {e}")
        return None

    # ✅ Extraction du nom de l'auteur
    author_name = author._results['author']['name']
    print(f"\n✅ **Auteur trouvé** : {author_name}")

    # 📌 Essai de récupération des métriques par Subject Area
    try:
        print("\n📌 **Envoi de la requête à SciVal...**")

        # ✅ Tentative de récupération
        subject_areas_raw = author._get_metrics_rawdata(
            metricType="ScholarlyOutput",
            yearRange="5yrs",
            subjectAreaFilterURI="All",
            includedDocs="AllPublicationTypes"
        )

        # ✅ Vérification de la réponse brute
        print("\n📌 **Réponse brute de SciVal :**")
        print(subject_areas_raw)  # ✅ Affiche la réponse brute

        if not subject_areas_raw:
            print("❌ Aucune donnée retournée par SciVal. Vérifiez vos paramètres API et l'auteur.")
            return None

        print("\n📌 **Subject Areas détectés :**")
        print(json.dumps(subject_areas_raw, indent=4))  # ✅ Affichage formaté du JSON complet

    except Exception as e:
        print(f"❌ Erreur lors de la récupération des Subject Areas : {e}")
        return None

# ✅ Exécution immédiate du test
if __name__ == "__main__":
    fetch_scival_subject_areas(AUTHOR_ID)
