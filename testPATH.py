

r"C:\Users\alima\.config\pybliometrics.cfg"


#file_path = r"C:\Users\alima\.config\text.txt"
file_path = r"C:\Users\alima\.config\pybliometrics.cfg"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

print("Conteúdo do arquivo:\n", content)