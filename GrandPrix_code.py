import requests 
from bs4 import BeautifulSoup
from datetime import datetime
import re
import csv
import time


ma_lst_dico = [] # liste de dictionnaire mis en place pour faciliter l'écriture du fichier csv 
id = 1 #initialisation de l'identifiant unique auto-incrémenté 

for year in range(1950, 2027): #Boucle sur les années pour ne pas depasser le nombre de requètes avec l'API 

    url = f"https://api.jolpi.ca/ergast/f1/{year}/races?limit=100"
    headers = {"User-Agent":"Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200 : 
        data = response.json()
        #  => récupération du premier Grand Prix de 1950 pour analyser la structure
        # print(data["MRData"]["RaceTable"]["Races"][1]) 
        # {'season': '1950', 'round': '2', 'url': 'https://en.wikipedia.org/wiki/1950_Monaco_Grand_Prix'
        # , 'raceName': 'Monaco Grand Prix', 'Circuit': {'circuitId': 'monaco', 'url': 'https://en.wikipedia.org/wiki/Circuit_de_Monaco'
        # , 'circuitName': 'Circuit de Monaco', 'Location': {'lat': '43.7347', 'long': '7.42056', 'locality': 'Monte Carlo'
        # , 'country': 'Monaco'}}, 'date': '1950-05-21'}

        
        for gp in data["MRData"]["RaceTable"]["Races"]: #Boucle qui atteind chaque grand prix d'une année un à un :
 
            season = gp['season']
            round = gp["round"]
            url_pour_nb_tours = gp["url"] #lien vers page wikipedia 
            name_gp = gp["raceName"]
            name_circuit = gp["Circuit"]["circuitName"]
            date = gp["date"]
            dt = datetime.strptime(date, "%Y-%m-%d")
            
            # récupération du nombre de tour sur la page wikipedia: 
            response2 = requests.get(url_pour_nb_tours, headers=headers)
            if response2.status_code == 200 : 
                soup = BeautifulSoup(response2.text, 'html.parser')

                try : #structure qui permet d'éviter les erreurs comme pour les grands prixs de 2026 qui n'ont pas encore leur page wikipedia dédiée, donc l'infobox était None 
                    infobox = soup.find('table', class_='infobox infobox-table vevent') or soup.find('table', class_='infobox') or soup.find('div', class_='infobox_v3')

                    for ligne in infobox.find_all('tr'):
                        if "Distance" in ligne.get_text(strip=True): #Sélectionne la ligne pour laquelle le titre est "Distance"
                            reponse = ligne.find('td')
                            if reponse :
                                if "laps" in reponse.get_text(strip=True): #Sélectionne l'information qui contient "laps", soit le nombre de tour
                                    laps = reponse.get_text(strip=True)
                                    laps_ = re.findall(r"^\d{1,5}", laps)[0] #utilisation de l'expression régulière pour ne garder que le nombre correspondant au tour 
                            
                except AttributeError : 
                    laps_ = None 

            #Ajout des informations dans un dictionnaire directement dans la liste
            ma_lst_dico.append({"gName":name_gp, 
                                "gpID":id,
                                "NomCircuit":name_circuit,
                                "gDate":dt,
                                "gLaps": laps_, #pour ne garder que le nombre 
                                "gRank":round,
                                "url_GP":url_pour_nb_tours})
            id += 1 #incrémentation de l'identifiant 

    # time.sleep(2) #temps de pause pour permettre l'enchaînement des requêtes 
    print(f"année {year} chargée")

# print(ma_lst_dico)
with open("GrandPrix_infos_supplémentaires.csv", "w", encoding="utf-8") as f: 
    writer = csv.DictWriter(f, fieldnames=["gName", "gpID", "NomCircuit", "gDate", "gLaps", "gRank", "url_GP"])
    writer.writeheader()
    writer.writerows(ma_lst_dico)


