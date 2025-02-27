from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus.exception import Scopus401Error, Scopus429Error, ScopusException

author_id = "35726950800"  # Exemple d'ID

try:
    author = AuthorRetrieval(author_id)
    print(f"Nom de l'auteur : {author.given_name} {author.surname}")
except Scopus401Error:
    print("❌ Erreur 401 : Vérifiez votre clé API ou votre connexion réseau.")
except Scopus429Error:
    print("❌ Erreur 429 : Quota API dépassé. Essayez avec une autre clé ou attendez.")
except ScopusException as e:
    print(f"❌ Une erreur Scopus s'est produite : {e}")
except Exception as e:
    print(f"❌ Une erreur générale s'est produite : {e}")
