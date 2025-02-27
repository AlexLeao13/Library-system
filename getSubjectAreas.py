from pybliometrics.scopus import AuthorRetrieval

from pybliometrics.scopus.author_retrieval import AuthorRetrieval



def get_subject_areas(author_id):
    """
    Récupère les subject areas et leurs scholarly output pour un chercheur donné via son Scopus ID.
    """
    try:
        # Récupération des informations de l'auteur
        author = AuthorRetrieval(author_id)
        
        # Vérification si l'auteur a des domaines associés
        if not author.subject_areas:
            print("Aucun subject area trouvé pour cet auteur.")
            return
        
        # Extraction et formatage des données
        subject_areas = []
        for area, output in zip(author.subject_areas, author.citation_count):
            subject_areas.append({
                "Subject Area": area,
                "Scholarly Output": output
            })
        
        # Affichage du résultat
        print("\nSubject Areas et Scholarly Output pour l'auteur ID:", author_id)
        for entry in subject_areas:
            print(f"- {entry['Subject Area']}: {entry['Scholarly Output']} publications")

    except Exception as e:
        print("Erreur lors de la récupération des données :", str(e))

# Demande de l'ID à l'utilisateur
author_id = int(input("Entrez l'ID Scopus de l'auteur : "))
get_subject_areas(author_id)