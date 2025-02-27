import os
import requests
import configparser
import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from datetime import datetime
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.text import RichText
from openpyxl.drawing.text import ParagraphProperties, CharacterProperties
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# 📌 Charger la configuration API
CONFIG_PATH = os.path.expanduser("~/.config/pybliometrics.cfg")
def load_api_keys():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    try:
        return config['Authentication']['APIKey'], config['Authentication']['InstToken']
    except KeyError:
        raise ValueError("API Key ou Token Institutionnel introuvables.")

# 📌 Récupérer les publications par plage d'années
def get_publication_count(author_id, start_year, end_year, api_key, inst_token):
    url = "https://api.elsevier.com/content/search/scopus"
    headers = {"X-ELS-APIKey": api_key, "X-ELS-Insttoken": inst_token, "Accept": "application/json"}
    params = {"query": f"AU-ID({author_id}) AND PUBYEAR > {start_year-1} AND PUBYEAR < {end_year+1}", "count": "0"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Erreur API : {response.status_code} - {response.text}")
    return int(response.json()["search-results"]["opensearch:totalResults"])

# 📌 Récupérer les principales disciplines
def get_subject_areas(author_id, start_year, end_year, api_key, inst_token):
    url = "https://api.elsevier.com/content/search/scopus"
    headers = {"X-ELS-APIKey": api_key, "X-ELS-Insttoken": inst_token, "Accept": "application/json"}
    params = {"query": f"AU-ID({author_id}) AND PUBYEAR > {start_year-1} AND PUBYEAR < {end_year+1}", "facets": "subjarea", "count": "0"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Erreur API : {response.status_code} - {response.text}")

    data = response.json()
    subject_areas = data.get("search-results", {}).get("facet", {}).get("category", [])
    if not subject_areas:
        raise ValueError("Aucune catégorie trouvée.")

    df = pd.DataFrame(subject_areas)
    df.rename(columns={"label": "Subject Area", "hitCount": "Scholarly Output"}, inplace=True)
    df["Scholarly Output"] = df["Scholarly Output"].astype(int)
    return df.sort_values(by="Scholarly Output", ascending=False)

# 📌 Créer un fichier Excel avec le graphique
def create_excel_report(author_id, start_year, end_year, df, total_publications):
    now = datetime.now().strftime("%Y-%m-%d_%Hh%M")
    filename = f"{now}_Scopus_{author_id}.xlsx"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)

    wb = Workbook()
    ws = wb.active
    ws.title = "Subject Areas"

    # Ajouter les informations générales
    ws.append(["Data set", "Publications by Subject Area"])
    ws.append(["Entity", author_id])
    ws.append(["Year range", f"{start_year} to {end_year}"])
    ws.append(["Total publications", total_publications])
    ws.append([])

    # Ajouter les données principales
    ws.append(["Subject Area", "Scholarly Output", "Percentage"])
    df["Percentage"] = (df["Scholarly Output"] / total_publications) * 100
    for _, row in df.iterrows():
        ws.append([row["Subject Area"], row["Scholarly Output"], f"{row['Percentage']:.1f}%"])

    # Créer le graphique
    chart = BarChart()
    chart.type = "bar"
    chart.style = 10
    chart.y_axis.reverseOrder = True
    chart.y_axis.labelOffset = 0

    data_range = Reference(ws, min_col=2, min_row=7, max_row=6 + len(df))
    categories_range = Reference(ws, min_col=1, min_row=7, max_row=6 + len(df))

    chart.add_data(data_range, titles_from_data=False)
    chart.set_categories(categories_range)
    chart.legend = None

    chart.layout = Layout(manualLayout=ManualLayout(x=0.01, y=0.05, w=0.7, h=0.85))
    ws.add_chart(chart, "E10")

    wb.save(file_path)
    return file_path

# Interface Graphique (GUI)
class PrincDiscipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PrincDiscip - Rapport des principales disciplines")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Logo ETS
        self.logo = tk.PhotoImage(file="ets_logo.png")
        logo_label = tk.Label(root, image=self.logo, bg="#f0f0f0")
        logo_label.pack(pady=5)

        # Titre
        title = tk.Label(root, text="Bienvenue sur PrincDiscip, le logiciel qui vous permet de générer automatiquement le rapport des principales disciplines des auteurs.",
                         font=("Helvetica", 12, "bold"), wraplength=750, bg="#f0f0f0")
        title.pack(pady=5)

        # Champs de saisie
        self.create_label_entry("ID Scopus de l'auteur (en bleu)", "author_id")
        self.create_label_entry("Année de début (en bleu)", "start_year")
        self.create_label_entry("Année de fin (en bleu)", "end_year")

        # Bouton Générer
        self.generate_button = tk.Button(root, text="Générer le rapport", command=self.generate_report, bg="#1f77b4", fg="white", font=("Helvetica", 10, "bold"))
        self.generate_button.pack(pady=10)
    
        # Bouton Nouvelle recherche
        self.reset_button = tk.Button(root, text="Nouvelle recherche", command=self.reset_fields, bg="#28a745", fg="white", font=("Helvetica", 10, "bold"))
        self.reset_button.pack(pady=5)


        # Zone de sortie
        self.output_text = tk.Text(root, height=10, width=90, bg="white", fg="black", wrap="word")
        self.output_text.pack(pady=5)
        self.output_text.insert("1.0", "✅ Résultats des principales disciplines :\n")

    def create_label_entry(self, label_text, attribute):
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=2)
        label = tk.Label(frame, text=f"{label_text} :", font=("Helvetica", 10), bg="#f0f0f0")
        label.pack(side="left")
        entry = tk.Entry(frame, width=30)
        entry.pack(side="left", padx=10)
        setattr(self, attribute, entry)

    def generate_report(self):
        author_id = self.author_id.get()
        start_year = self.start_year.get()
        end_year = self.end_year.get()

        if not (author_id and start_year.isdigit() and end_year.isdigit()):
            messagebox.showerror("Erreur", "Veuillez entrer des informations valides.")
            return

        api_key, inst_token = load_api_keys()

        try:
            total_publications = get_publication_count(author_id, int(start_year), int(end_year), api_key, inst_token)
            df_subjects = get_subject_areas(author_id, int(start_year), int(end_year), api_key, inst_token)
            file_path = create_excel_report(author_id, int(start_year), int(end_year), df_subjects, total_publications)

            self.output_text.insert("end", f"\n✅ Rapport généré avec succès : {file_path}\n")
            
            # Afficher les résultats des principales disciplines
            self.output_text.insert("end", "\n📊 Résultats des principales disciplines :\n")
            self.output_text.insert("end", df_subjects.to_string(index=False) + "\n")


        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def reset_fields(self):
        """Réinitialiser les champs pour une nouvelle recherche."""
        self.author_id.delete(0, tk.END)
        self.start_year.delete(0, tk.END)
        self.end_year.delete(0, tk.END)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", "✅ Résultats des principales disciplines :\n")

    

if __name__ == "__main__":
    root = tk.Tk()
    app = PrincDiscipApp(root)
    root.mainloop()
