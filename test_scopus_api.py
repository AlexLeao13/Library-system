from pybliometrics.scopus import AuthorSearch, init
import os

# ✅ Ensure Pybliometrics is initialized
print("🔧 Initializing Pybliometrics...")
init()

# ✅ Check if the configuration file is detected
config_path = os.path.abspath(r"C:\Users\alima\.config\pybliometrics.cfg")
if os.path.exists(config_path):
    print(f"✔️ Configuration file detected at: {config_path}")
else:
    print("❌ Configuration file not found! Please initialize Pybliometrics.")

# 🔍 **Step 1: Try searching for an author**
query = "AUTHLAST(Selten) AND AUTHFIRST(Reinhard)"  # Example author search
try:
    search = AuthorSearch(query, refresh=True)  # 🔹 Try forcing a refresh
    print(f"✔️ Author search successful. Results found: {search.get_results_size()}")
except Exception as e:
    print(f"❌ Error during AuthorSearch: {e}")

# 🔍 **Step 2: Test fetching author details**
try:
    author_id = "35726950800"  # Example Scopus author ID
    author = AuthorSearch(f"AU-ID({author_id})", refresh=True)

    # 🔍 Affichage du debug
    print(f"🔍 Debug: author.authors = {author.authors}")

    # ✅ Accès aux attributs avec le point `.`
    first_author = author.authors[0]  # C'est un objet Author, pas un dictionnaire
    print(f"✔️ Retrieved author: {first_author.givenname} {first_author.surname}")
except Exception as e:
    print(f"❌ Error retrieving author data: {e}")

