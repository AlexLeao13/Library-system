import os
import json
import logging
from pybliometrics.scival.author_lookup import AuthorLookup

# Activer le mode débogage
logging.basicConfig(level=logging.DEBUG)

# ID de test
AUTHOR_ID = "56216876600"

# Définition du chemin de configuration SciVal
os.environ["PYBLIOMETRICS_CONFIG"] = r"C:\Users\alima\.config\pybliometrics.cfg"

def fetch_subject_areas(author_id):
    """ Récupère les Subject Areas et leurs Scholarly Output depuis SciVal. """
    print(f"Récupération des Subject Areas pour l'auteur {author_id}...\n")

    try:
        # Création de l'objet AuthorLookup
        author = AuthorLookup(author_id=author_id, refresh=True)

        # Récupération des Scholarly Outputs par Subject Area
        subject_areas_data = author.get_metrics_Other(
            metricType='ScholarlyOutput',  # Extraction des outputs
            subjectAreaFilterURI='AllSubjectAreas',  # On récupère toutes les Subject Areas
            includedDocs='AllPublicationTypes'  # Inclut tous les types de publications
        )

        # Debugging: Affichage de la réponse brute
        print("\nRaw Response:")
        print(subject_areas_data)

        # Vérifier si la réponse est vide ou invalide
        if not subject_areas_data:
            print("La réponse de l'API est vide. Vérifiez l'ID de l'auteur et votre connexion.")
            return

        # Vérifier si la réponse contient bien une liste
        if hasattr(subject_areas_data, "List") and subject_areas_data.List:
            print("\nSubject Areas détectés :")
            print(json.dumps(subject_areas_data.List, indent=4))  # Affichage formaté du JSON complet
        else:
            print("Aucun Subject Area trouvé pour cet auteur. Vérifiez l’ID et les filtres appliqués.")

    except Exception as e:
        print(f"Erreur lors de la récupération des Subject Areas : {e}")

# Exécute la fonction
fetch_subject_areas(AUTHOR_ID)