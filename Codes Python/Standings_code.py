import requests
import time
import csv
import os

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

### Fonctions

# Récupération des résultats d'une course 
def course(lien):
    liste_course = []
    url = lien
    reponse = requests.get(url, headers=headers)
    if reponse.status_code == 200:
        data = reponse.json()
        for course in data['MRData']["RaceTable"]['Races']:
            dico_course = {}
            dico_course['sSeason'] = course['season']
            dico_course['gpID'] = course['raceName']
            for result in course['Results']:
                dico_pilote = {}
                dico_pilote.update(dico_course)
                dico_pilote['driverID'] = result['Driver']['givenName'] + ' ' + result['Driver']['familyName']
                dico_pilote['sPos'] = result['position']
                dico_pilote['sPoints'] = result['points']
                dico_pilote['sGrid'] = result['grid']
                dico_pilote['sLaps'] = result['laps']
                if result['laps'] == '0':
                    dico_pilote['sInc'] = 'DNS'
                if result['status'] != 'Finished':
                    if result['status'] == 'Retired':
                        dico_pilote['sInc'] = "DNF"
                    elif result['status'] == 'Disqualified':
                        dico_pilote['sInc'] = "DQ" 
                    elif "+" in result['status']:
                        dico_pilote['sInc'] = 'RAS'
                    else : 
                        dico_pilote['sInc'] = result['status']
                elif result['status'] == 'Finished':
                    dico_pilote['sInc'] = 'RAS'
                liste_course.append(dico_pilote)
    return liste_course


def creer_csv(i, liste_complete):
    fichier_existe = os.path.exists(f'standings_{i}.csv') and os.path.getsize(f'standings_{i}.csv') > 0
    colonnes = liste_complete[0].keys() 
    with open(f'standings_{i}.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=colonnes)
        if not fichier_existe:
            writer.writeheader()
        writer.writerows(liste_complete)
        

### Utilisation

# Création d'un csv par année
for i in range(1950, 2027):
    liste_complete = []
    for j in range(1, 25):      # j est le numéro du round de la saison i, le maximum étant 24
        url = f"http://api.jolpi.ca/ergast/f1/{i}/{j}/results?limit=100"
        liste_une_course = course(url)
        for dico in liste_une_course:
            liste_complete.append(dico)
        time.sleep(5)
    creer_csv(i, liste_complete)
print('Les fichiers sont chargés')


## CONSEIL SI CA BLOQUE (trop de demandes API): 
# Relancer le code par quinzaine d'années pour alléger les requêtes
# 1950, 1966
# 1966, 1981
# 1981, 1996
# 1996, 2011
# 2011, 2027
        


