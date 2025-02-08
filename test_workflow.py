import sys
import os
import json
import pandas as pd
from pybliometrics.scopus.author_retrieval import AuthorRetrieval
from pybliometrics.scopus.scopus_search import ScopusSearch
from pybliometrics.scopus.abstract_retrieval import AbstractRetrieval

# ✅ Configuration de Scopus
os.environ["PYBLIOMETRICS_CONFIG"] = r"C:\\Users\\alima\\.config\\pybliometrics.cfg"

# ✅ Dictionnaire des principaux Subject Areas (ASJC Codes)
ASJC_MAPPING = {
    10: "Multidisciplinary",
    11: "Agricultural and Biological Sciences",
    12: "Arts and Humanities",
    13: "Biochemistry",
    14: "Business",
    15: "Chemical Engineering",
    16: "Chemistry",
    17: "Computer Science",
    18: "Decision Sciences",
    19: "Earth and Planetary Sciences",
    20: "Economics",
    21: "Energy",
    22: "Engineering",
    23: "Environmental Science",
    24: "Immunology and Microbiology",
    25: "Materials Science",
    26: "Mathematics",
    27: "Medicine",
    28: "Neuroscience",
    29: "Nursing",
    30: "Pharmacology",
    31: "Physics and Astronomy",
    32: "Psychology",
    33: "Social Sciences",
    34: "Veterinary",
    35: "Dentistry",
    36: "Health Professions"
}

def fetch_primary_author_documents(author_id, filter_subject=None):
    """ Récupère uniquement les documents où l'auteur est premier auteur et les classe par Subject Areas. """
    print(f"🔍 Récupération des documents où l'auteur {author_id} est premier auteur...")

    try:
        author = AuthorRetrieval(author_id)
        indexed_name = author.indexed_name.lower().strip()
        last_name = indexed_name.split()[0]  # Extraction du nom de famille uniquement (Melhado)

        print(f"✅ Données récupérées avec succès depuis Scopus")
        print(f"📌 Indexed Name détecté par Scopus : '{indexed_name}'")
        print(f"📌 Nom de famille utilisé pour la comparaison : '{last_name}'")

    except Exception as e:
        print(json.dumps({"error": f"Erreur lors de la récupération des données Scopus : {str(e)}"}, indent=4))
        return

    try:
        query = f'AU-ID({author_id})'  # Rechercher tous les documents de l'auteur
        search = ScopusSearch(query)
        docs_df = pd.DataFrame(search.results)

        if docs_df.empty:
            raise AttributeError("Aucun document trouvé pour cet auteur.")

        # ✅ Vérification : Affichage des 5 premières valeurs de `author_names`
        print("\n📌 Vérification : Exemple de noms d'auteurs extraits de Scopus")
        print(docs_df[['eid', 'author_names']].head())

        # Vérifier si 'author_names' existe dans les colonnes
        if 'author_names' not in docs_df.columns:
            raise KeyError("La colonne 'author_names' n'existe pas dans les données récupérées.")

        # ✅ Identifier les documents où l'auteur est en première position
        def is_first_author(authors_list):
            authors = [name.strip().lower() for name in str(authors_list).split(";")]
            return last_name in authors[0]  # Vérifier si le nom de famille est dans le premier auteur

        primary_author_docs = docs_df[docs_df['author_names'].apply(is_first_author)]
        total_primary_author_documents = primary_author_docs.shape[0]

        print(f"📌 Nombre total de documents où l'auteur est premier auteur : {total_primary_author_documents}")

        # ✅ Extraire les Subject Areas depuis chaque document
        scholarly_output_data = {}
        for _, row in primary_author_docs.iterrows():
            eid = row['eid']
            try:
                abstract = AbstractRetrieval(eid, view="FULL")  # 🔥 Utilisation de la vue complète

                # ✅ Vérifier si `subject_areas` est disponible
                if abstract.subject_areas:
                    for sa in abstract.subject_areas:
                        if sa.code in ASJC_MAPPING:
                            subject_name = ASJC_MAPPING[sa.code]
                            scholarly_output_data[subject_name] = scholarly_output_data.get(subject_name, 0) + 1
                else:
                    print(f"⚠️ Aucune donnée de Subject Areas pour le document {eid}")

            except Exception as e:
                print(f"⚠️ Erreur lors de l'extraction des Subject Areas pour le document {eid}: {str(e)}")

        # ✅ Filtrer par Subject Area spécifique si demandé
        if filter_subject:
            scholarly_output_data = {filter_subject: scholarly_output_data.get(filter_subject, 0)}

        print("📌 Résultats des Scholarly Outputs par Subject Area")

    except Exception as e:
        print(json.dumps({"error": f"Erreur lors de la récupération des documents : {str(e)}"}, indent=4))
        return

    # ✅ Affichage des données transformées en JSON
    print(json.dumps({
        "total_primary_author_documents": total_primary_author_documents,
        "scholarly_outputs": scholarly_output_data
    }, indent=4, ensure_ascii=False))

def main():
    author_id = input("Entrez l'ID de l'auteur Scopus : ").strip()

    # ✅ Afficher tous les Subject Areas disponibles
    print("\n📌 Liste des Subject Areas disponibles :")
    for key, value in ASJC_MAPPING.items():
        print(f"{value}")

    filter_choice = input("\n👉 Entrez un Subject Area pour filtrer (ou laissez vide pour voir tous les résultats) : ").strip()

    # Exécuter avec ou sans filtre
    fetch_primary_author_documents(author_id, filter_subject=filter_choice if filter_choice else None)

if __name__ == "__main__":
    main()  # 🔥 Exécuter uniquement avec Scopus
