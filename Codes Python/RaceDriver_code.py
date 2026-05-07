from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time 
from pprint import pprint
import csv 
import re

# os.getcwd()
# BIEN VERIFIER L'EMPLACEMENT DANS LE WORKSPACE


# Configuration pour laisser le navigateur ouvert
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Objectif : faire une liste de dictionnaire avec 
# Numéro, Nom, Année et Écurie pour chaque grand prix de 1950 à 2026

# Lancement du driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

#initialisation d'une liste de dictionnaire vide
lst_dico = []
 
try : 
    url_principale = "https://www.statsf1.com/fr/1950/grande-bretagne/engages.aspx"
    driver.get(url_principale)
    time.sleep(1) #temps nécéssaire pour que le navigateur ouvre la page 
    while url_principale : 
        entete = driver.find_element(By.XPATH, '//*[@id="header"]/div[3]/div/div[2]/h2/a').text
        year = re.findall(r'\d{4}', entete)[0] #trouve l'année
        gp = re.findall(r'(.*)\d{4}', entete)[0] #et le pays du GP 

        tableau = driver.find_element(By.ID, "ctl00_CPH_Main_GV_Stats") #on accéde au tableau par son identifiant 
        lignes = tableau.find_elements(By.TAG_NAME, "tr") #récupèration d'une liste dans laquelle chaque ligne est un dictionnaire 

        for ligne in lignes[1:]: #evite la ligne d'entête
            cellules = ligne.find_elements(By.TAG_NAME, "td") #atteinte de chaque cellule de la ligne 
        
            #tableau toujours du même format tel que : 
            num = cellules[0].text
            pilote = cellules[1].text
            ecurie = cellules[2].text
            chassis = cellules[3].text
            moteur = cellules[5].text
            pneu = cellules[7].text

            # print(f"season : {year}, num : {num}, pilote : {pilote}, ecurie : {ecurie},chassis : {chassis}, moteur : {moteur}, pneu : {pneu} ")
            
            lst_dico.append({"url" : url_principale,
                            "season" : year,
                            "num" : num,
                            "pilote" : pilote, 
                            "ecurie" : ecurie,
                            "chassis" : chassis,
                            "moteur" : moteur,
                            "pneu" : pneu,
                            "nom_gp" : gp})
        
        print(f"ok pour le lien : {url_principale}") #test pour qu'en cas d'erreur on puisse accéder directement à la page qui provoque un bug
        url_a_visiter = driver.find_element(By.ID, "ctl00_HL_NavigRight") #atteinte de la ligne ou se trouve le lien de la page suivante 
        url_principale = url_a_visiter.get_attribute("href") #récupération du lien seulement 
        driver.get(url_principale)
        time.sleep(0.5) #temps pour charger la page 



except : 
    pass

# quitter la page ouverte à la fin de l'execution 
finally : 
    driver.quit()


#écriture du fichier csv avec beaucoup d'informations
with open("RaceDriver_infos_supplémentaires.csv", "w", encoding="utf-8") as f : 
    writer = csv.DictWriter(f, fieldnames=["url",
                            "season",
                            "num",
                            "pilote", 
                            "ecurie",
                            "chassis",
                            "moteur",
                            "pneu",
                            "nom_gp"])
    writer.writeheader() #écriture des entêtes 
    writer.writerows(lst_dico)

# un prochain script trie les lignes pour écrire un fichier csv plus propre (RaceDriver_1974+.py)