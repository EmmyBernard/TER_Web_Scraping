import requests
import time
from bs4 import BeautifulSoup
import json
import re
import csv


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
un_circuit = {}


### Fonctions


def temps_en_secondes(temps_str):
    try:
        if ":" in temps_str:
            minutes, secondes = temps_str.split(":")
            return round(int(minutes) * 60 + float(secondes), 3)
        else:
            return round(float(temps_str), 3)
    except:
        return None # En cas de format de texte imprévu


def recup_infobox(lien):   
    url= lien
    reponse = requests.get(url, headers=headers)
    if reponse.status_code == 200:
        soup = BeautifulSoup(reponse.text, 'html.parser')
    else:
        raise ValueError
    
    liste_versions = []
    infobox = soup.find('table',class_ = "infobox vcard" )

    if infobox:
            derniere_date = " "
            for ligne in infobox.find_all('tr'):
                titre = ligne.find('th')
                reponse = ligne.find('td')
                if titre and not reponse:       # Cas 1 : on trouve une date donc un <th> sans <td>
                        annee_grand_prix = {}
                        derniere_date = titre.get_text(strip=True)
                        annee_grand_prix['cVersion'] = derniere_date
                elif reponse and titre :        # Cas 2 : on trouve une donnée donc un <th> ET un <td>
                    categorie = titre.get_text(strip=True)
                    if categorie == 'Length':
                        donnee = reponse.get_text(" ", strip=True).split('(')[0].strip()
                        annee_grand_prix["cLength"] = donnee
                    elif categorie == 'Race lap record':
                        texte_complet = reponse.get_text(" ", strip=True).replace('\u2013', '-')
                        # On ne traite que si "F1" est présent
                        if "F1" in texte_complet:
                        # On découpe l'information récupérée
                            parties = texte_complet.split('(', 1)
                            temps_raw = parties[0].strip()

                            annee_grand_prix["cLapRec"] = temps_en_secondes(temps_raw)
                            if len(parties) > 1:
                                contenu_parenthese = parties[1].replace(')', '')

                                match_annee = re.search(r'(\d{4})', contenu_parenthese)
                                if match_annee:
                                    annee_grand_prix["cYearRec"] = match_annee.group(1)

                                infos_split = contenu_parenthese.split(',')
                                if len(infos_split) >0:
                                    pilote = infos_split[0].strip()
                                    annee_grand_prix["cDrivRec"] = pilote
                                    liste_versions.append(annee_grand_prix)
                            
                            else:
                                # Si le format est spécial mais que c'est de la F1, on garde tout
                                annee_grand_prix["cYearRec"] = texte_complet
                                liste_versions.append(annee_grand_prix)

                        else :  # Si ce n'est pas un record de F1
                            annee_grand_prix['cYearRec'] = 'NULL'
                            annee_grand_prix['cDrivRec'] = 'NULL'
                            annee_grand_prix['cLapRec'] = 'NULL'
                            liste_versions.append(annee_grand_prix)

    return liste_versions



def recup_api(lien):
    url = f"https://api.jolpi.ca/ergast/f1/circuits?limit=100"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    reponse = requests.get(url, headers=headers)
    if reponse.status_code == 200:
        data = reponse.json()
        for circuit in data['MRData']['CircuitTable']['Circuits']:
            if circuit['url'] == lien :
                un_circuit = {}
                un_circuit['cName'] = circuit['circuitName']
                un_circuit['cCity'] = circuit['Location']['locality']
                un_circuit['cCountry'] = circuit['Location']['country']
    else:
        un_circuit = {'NULL'}
        
    return un_circuit
    

### Programme principal

# Création de ma liste de liens pour chaque circuit
liste_lien = []
url = f"https://api.jolpi.ca/ergast/f1/circuits?limit=100"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
reponse = requests.get(url, headers=headers)
if reponse.status_code == 200:
    data = reponse.json()
    for circuit in data['MRData']['CircuitTable']['Circuits']:
        liste_lien.append(circuit['url'])


tous_les_circuits = []
for lien in liste_lien:
    try : 
        dico = recup_api(lien)
        liste = recup_infobox(lien)
        if len(liste) >= 2 :
                for dic in liste:
                    dico_init = dico.copy()
                    dico_init.update(dic)
                    tous_les_circuits.append(dico_init)
        else:
            dic = liste[0]
            dico.update(dic)
            tous_les_circuits.append(dico)
        time.sleep(3)
    except:
        None

# Création du json
with open('Circuits.json', 'x') as fich:
    fich.write(json.dumps(tous_les_circuits, indent=4, ensure_ascii=False))


# Création du csv
with open('Circuits.json', 'r') as f:
    donnees = json.load(f)

# On récupère les noms des colonnes à partir des clés du premier dictionnaire (et on verifie que la liste n'est pas vide)
if donnees:
    colonnes = donnees[0].keys()

    with open('Circuit_sans_jointure_pas_nettoye.csv', 'w', newline='', encoding='utf-8') as f_csv:
        writer = csv.DictWriter(f_csv, fieldnames=colonnes)       
        # ecrire le nom des colonnes
        writer.writeheader()
        # ecrire toutes les lignes d'un coup
        writer.writerows(donnees)




