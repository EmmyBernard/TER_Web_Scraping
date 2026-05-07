import requests 
from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime
import re
import csv 



#Fonction qui récupère le nom du champion de la saison sur le site englais fournis par l'API
def Recup_url_season(url, year): #pour url de type  "https://en.wikipedia.org/wiki/1950_Formula_One_season" récupéré par l'API
    if int(year) == 2026 :  #exclusion de 2026 car on ne connait pas le champion
        return None
    headers = {"User-Agent":"Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200 : 
        soup = BeautifulSoup(response.text, 'html.parser')
        tableau = soup.find('div', class_="motorsport-season-nav-subheader")
        Champion = tableau.find_all('a')[1].get_text(strip=True)
        
    return Champion

#TEST 
# Recup_url_season("https://en.wikipedia.org/wiki/1950_Formula_One_season", 1950)

#Fonction qui récupère diverses informations pour la saison à partir du site wikipedia français. 
def Recup_site_fr(year):
    url = f"https://fr.wikipedia.org/wiki/Championnat_du_monde_de_Formule_1_{year}" #url uniforme pour toutes les saisons 
    headers = {"User-Agent":"Mozilla/5.0"}
    response = requests.get(url, headers=headers)


    if response.status_code == 200 : 
        soup = BeautifulSoup(response.text, 'html.parser')
        infobox = soup.find('table', class_='infobox infobox-table vevent') or soup.find('table', class_='infobox') or soup.find('div', class_='infobox_v3')
        tableaux = infobox.find_all('table')

        #Récupération, selon les années, dans le premier tableau de l'infobox
        # Nb de manches, Nb paticipants et  Nb équipes : 
        Nb_participants = None 
        Nb_equipes = None 
        Nb_manche = None 
        for ligne in tableaux[0].find_all('tr'): 
            if "Nombre de manches" in ligne.get_text(strip=True) or "Épreuves" in ligne.get_text(strip=True) : #erreur en 2011 si on ne rajoute pas cette condition
                reponse = ligne.find('td').get_text(strip=True)
                Nb_manche = re.findall(r"^\d+", reponse)[0] #renvoie une liste de un élément indexé à 0 
                
            if "Participants" in ligne.get_text(strip=True) :
                Nb_participants = re.findall(r"^(\d+)(?:.*)" , ligne.find('td').get_text(strip=True))[0] #Liste de 1 élément 

                try : #cette information n'est pas toujours précisée mais elle se trouve sur la même ligne que le nombre de participants 
                    Nb_equipes = re.findall(r"(\d{1,2})\s*équipes" , ligne.find('td').get_text(strip=True))[0] #Liste de 1 élément 
                except IndexError : #Signifie que l'information ne figure pas dans l'infobox
                    Nb_equipes = None

            
        # Récupération, selon les années, dans le deuxième tableau de l'infobox
        # Le champion de la saison ainsi que le constructeur champion (à partir de 1958)
        # On ignore l'année 2026, pour laquelle on ne connait pas ces informations 
        Champion_driver = None
        Champion_constructor = None
        if int(year) < 2026 :
            for ligne in tableaux[1].find_all('tr'):
                if "Champion pilote" in ligne.get_text(strip=True): #Information deja récupérée par la fonction précédente
                    Champion_driver = ligne.find('td').get_text(strip=True)
            
                if "Champion constructeur" in ligne.get_text(strip=True) : #Information à partir de 1958
                    Champion_constructor = ligne.find('td').get_text(strip=True)
            
    return Nb_manche, Champion_driver, Champion_constructor, url, Nb_participants, Nb_equipes



#################################### PROGRAMME PRINCIPAL ######################################################

# récupération des années et liste des url 
url = f"https://api.jolpi.ca/ergast/f1/seasons?limit=100"
headers = {"User-Agent":"Mozilla/5.0"}
response = requests.get(url, headers=headers)

if response.status_code == 200 : 
    data = response.json()
    # print(data["MRData"]["SeasonTable"]["Seasons"][1]) # Renvoie le dico de la premère année 

    lst = []
    for season_dic in data["MRData"]["SeasonTable"]["Seasons"] : #parcours des saisons par année 
        year = season_dic["season"]
        url_en = season_dic["url"]
        champion_Site_en = Recup_url_season(url_en, year)
        Nb_GP, champion_site_fr, champion_constructeur_fr, url_fr, Nb_participants, Nb_equipes = Recup_site_fr(year)

        year = int(year) #afin de pouvoir réaliser les comparaisons

        #Ajout manuel de l'attribut SeNbFixed, Numéro fixe à vie pour un pilote qui est mis en place à partir de 2014 inclu
        if year >= 2014 :  
            seNbFixed = True
        else : 
            seNbFixed = False

        #Ajout manuel des manufacturiers de pneu lorsqu'ils sont communs à toutes les écuries 
        seTires = None #pour les années où il y a plusieurs manufacturiers possibles : aller voir la table team 
        if year in range(1961, 1964):
            seTires = "Dunlop"
        elif year in range(1987, 1989) or year in range(1992, 1997):
            seTires = "Goodyear"
        elif year in range(1999, 2001) or year in range(2007, 2011):
            seTires = "Bridgestone"
        elif year >= 2011 : 
            seTires = "Pirelli"

        #Ajout dans un dictionnaire 
        dic_rendu_season = {"id" : year,
                            "url_en" : url_en,
                            "url_fr" : url_fr,
                            "Champion" : champion_Site_en,
                            # "Champ_fr" : champion_site_fr, Ce sont les mêmes après vérification
                            "Nb_GP" : Nb_GP,
                            "Champion_constructeur" : champion_constructeur_fr, #None si non reseigné, apparait à partir de 1950
                            "Nb_pilotes" : Nb_participants, #None si non renseigné sur site fr 
                            "Nb_team" : Nb_equipes, #None si non renseigné sur site fr
                            "seNbFixed" : seNbFixed, #Booléen : True à partir de 2014 car nombre fixe à vie 
                            "seTires" : seTires } #None si plusieurs manufacturiers sur une même saison
        print(f'année {year} OK') 
        lst.append(dic_rendu_season)


    with open("Season_infos_supplémentaires.csv","w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "url_en","url_fr", "Champion", "Nb_GP", "Champion_constructeur", "Nb_pilotes", "Nb_team", "seNbFixed", "seTires"])
        writer.writeheader()
        writer.writerows(lst)

