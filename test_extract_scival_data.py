from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pandas as pd
import os

# 📌 CONFIGURATION SELENIUM
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Ouvrir Chrome en plein écran
options.add_argument("--disable-blink-features=AutomationControlled")  # Contourner la détection de bot
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 🔥 Démarrer le navigateur
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)  # Augmenter le temps d'attente

# 📌 Aller sur SciVal
scival_url = "https://www.scival.com/"
driver.get(scival_url)

# ⏳ Attendre que la page charge complètement
time.sleep(10)

# 📌 Vérifier si on est bien connecté
try:
    login_button = driver.find_element(By.XPATH, "//button[contains(text(),'Sign in')]")
    print("❌ Vous n'êtes pas connecté. Veuillez vous connecter manuellement et relancer le script.")
    driver.quit()
    exit()
except:
    print("✅ Connexion détectée. Continuation du script...")

# 📌 Attendre un peu pour éviter la détection du bot
time.sleep(random.randint(5, 10))

# 📌 Vérifier si on est bloqué sur la page d’accueil de SciVal (capture d’écran)
if "landing" in driver.current_url:
    print("⚠️ SciVal a détecté un accès automatisé. Essaye de te connecter manuellement et relance le script.")
    driver.quit()
    exit()

# 📌 Simuler un mouvement de souris et un scroll pour éviter la détection du bot
driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
time.sleep(random.uniform(2, 5))
driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
time.sleep(random.uniform(2, 5))

# 📌 Aller sur "Entity List" (avec un sélecteur plus précis)
try:
    entity_list_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@title, 'Entity list')]")))
    entity_list_button.click()
    print("✅ Accès à la 'Entity List'.")
except Exception as e:
    print(f"❌ ERREUR : Impossible de trouver 'Entity List'. Vérifiez la page SciVal. \n{e}")
    driver.quit()
    exit()

# 📌 Continuer avec la recherche de l'auteur...
