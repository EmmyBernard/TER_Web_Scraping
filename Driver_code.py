import requests
from bs4 import BeautifulSoup
import csv
import time
import re

url_pilotes = "https://fr.wikipedia.org/wiki/Liste_des_pilotes_de_Formule_1"
headers = {"User-Agent": "Mozilla/5.0"}
# Dictionnaire des mois et la correspondance en chiffre
mois = {
    'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04',
    'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08',
    'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'
}

# Liste des femmes avec url
femmes_noms = ["Maria Teresa de Filippis", "Lella Lombardi", "Divina Galica", "Desiré Wilson", "Giovanna Amati"]
urls_femmes_forcees = [
    "/wiki/Maria_Teresa_de_Filippis",
    "/wiki/Lella_Lombardi",
    "/wiki/Divina_Galica",
    "/wiki/Desir%C3%A9_Wilson",
    "/wiki/Giovanna_Amati"
]

# Dictionnaire des pilotes avec des noms composés
noms_composes = {
    "Andrea Kimi Antonelli": ("Andrea Kimi", "Antonelli"),
    "John Campbell Jones": ("John", "Campbell Jones"),
    "Hermano da Silva Ramos": ("Hermano", "da Silva Ramos"),
    "Mário de Araújo Cabral": ("Mário", "de Araújo Cabral"),
    "Maria Teresa De Filippis": ("Maria Teresa", "De Filippis"),
    "Juan Manuel Fangio": ("Juan Manuel", "Fangio"),
    "Oscar Alfredo Gálvez": ("Oscar Alfredo", "Gálvez"),
    "Francisco Godia Sales": ("Francisco", "Godia Sales"),
    "Carel Godin de Beaufort": ("Carel", "Godin de Beaufort"),
    "José Froilán González": ("José Froilán", "González"),
    "Miguel Ángel Guerra": ("Miguel Ángel", "Guerra"),
    "José Carlos Pace": ("José Carlos", "Pace"),
    "Nelson Angelo Piquet": ("Nelson Angelo", "Piquet"),
    "Alberto Rodriguez Larreta": ("Alberto", "Rodriguez Larreta"),
    "Pedro Rodríguez de la Vega": ("Pedro", "Rodríguez de la Vega"),
    "Carlos Sainz Jr": ("Carlos", "Sainz Jr"),
    "Adolfo Schwelm Cruz": ("Adolfo", "Schwelm Cruz"),
    "Archie Scott Brown": ("Archie", "Scott Brown")
}

mapping_nationalites= {
    # Amériques
    'américaine': 'États-Unis', 'américain': 'États-Unis', 'états-unis': 'États-Unis',
    'canadienne': 'Canada', 'canadien': 'Canada',
    'argentine': 'Argentine', 'argentin': 'Argentine',
    'brésilienne': 'Brésil', 'brésilien': 'Brésil', 'brésilen': 'Brésil', 'bresilien': 'Brésil', 'brésil': 'Brésil',
    'mexicaine': 'Mexique', 'mexicain': 'Mexique',
    'vénézuélienne': 'Venezuela', 'vénézuélien': 'Venezuela',
    'colombienne': 'Colombie', 'colombien': 'Colombie',
    'uruguayenne': 'Uruguay', 'uruguayen': 'Uruguay',
    'chilien': 'Chili',

    # Europe
    'française': 'France', 'français': 'France', 'france': 'France',
    'britannique': 'Royaume-Uni', 'royaume-uni': 'Royaume-Uni', 'anglaise': 'Royaume-Uni', 'anglais': 'Royaume-Uni', 'écossaise': 'Royaume-Uni', 'nord-irlandais': 'Royaume-Uni',
    'allemande': 'Allemagne', 'allemand': 'Allemagne', 'allemagne': 'Allemagne', 'ouest-allemand': 'Allemagne', 'est-allemand': 'Allemagne',
    'italienne': 'Italie', 'italien': 'Italie', 'italie': 'Italie',
    'espagnole': 'Espagne', 'espagnol': 'Espagne',
    'belge': 'Belgique', 'belgique': 'Belgique',
    'suisse': 'Suisse',
    'monégasque': 'Monaco',
    'néerlandaise': 'Pays-Bas', 'néerlandais': 'Pays-Bas', 'pays-bas': 'Pays-Bas',
    'autrichienne': 'Autriche', 'autrichien': 'Autriche', 'autriche': 'Autriche',
    'finlandaise': 'Finlande', 'finlandais': 'Finlande', 'finlande': 'Finlande',
    'suédoise': 'Suède', 'suédois': 'Suède', 'suède': 'Suède',
    'danois': 'Danemark',
    'portugais': 'Portugal',
    'hongrois': 'Hongrie',
    'russe': 'Russie', 'russie': 'Russie',
    'polonaise': 'Pologne',
    'tchèque': 'République Tchèque',
    'liechtensteinois': 'Liechtenstein',

    # Océanie & Asie
    'australienne': 'Australie', 'australien': 'Australie',
    'néo-zélandaise': 'Nouvelle-Zélande', 'néo-zélandais': 'Nouvelle-Zélande',
    'japonaise': 'Japon', 'japonais': 'Japon', 'japon': 'Japon',
    'thaïlandaise': 'Thaïlande', 'siam': 'Thaïlande',
    'chinoise': 'Chine',
    'indienne': 'Inde', 'indien': 'Inde',
    'indonésien': 'Indonésie',
    'malaisienne': 'Malaisie',

    # Afrique
    'sud-africaine': 'Afrique du Sud', 'sud-africain': 'Afrique du Sud', 'afrique du sud': 'Afrique du Sud',
    'rhodésienne': 'Zimbabwe', 'rhodésien': 'Zimbabwe',
    'algérienne': 'Algérie',
    'maurice': 'Île Maurice'
}
response = requests.get(url_pilotes, headers=headers)

if response.status_code == 200:
    print("ok, ça fonctionne")
    soup = BeautifulSoup(response.text, 'html.parser')
    pilotes = []

    for li in soup.find_all('li'):
        if ":" in li.text:
            for a in li.find_all('a'):
                href = a.get("href", "")
                if href.startswith("/wiki/") and not href.startswith("/wiki/Fichier:"):
                    pilotes.append(href)
                    break

    for url_f in urls_femmes_forcees:
        if url_f not in pilotes:
            pilotes.append(url_f)
# Création du fichier csv
with open('pilotes_f1.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
    colonnes = ["driverID", "dFirstName", "dLastName", "dBirthdate", "dDeathdate", "dCountry", "dGender"]
    writer = csv.DictWriter(fichier_csv, fieldnames=colonnes)
    writer.writeheader()
# Initialisation de l'identifiant, on commence à 1
    driverID = 1
    url_infox = "https://fr.wikipedia.org"
    particules = {'de', 'des', 'du', 'van', 'von', 'der', 'da', 'di', 'la', 'le', 'del'} # dictionnaire avec différents mot de liaison pour les noms composés

    # Mapping des catégories de l'infobox aux noms de colonnes CSV
    # AJOUT DES VARIANTES "Naissance" et "Décès" pour les anciens pilotes
    category_to_column = {
        "Date de naissance": "dBirthdate",
        "Naissance": "dBirthdate",
        "Date de décès": "dDeathdate",
        "Décès": "dDeathdate",
        "Nationalité": "dCountry",
    }

    for pilote in pilotes:
        url_total = url_infox + f"{pilote}" # Création de l'url final

        response = requests.get(url_total, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            infos_du_pilote = {champ: "Null" for champ in colonnes}

            infos_du_pilote["driverID"] = driverID


            infobox = soup.find('div', class_='infobox_v3') or soup.find('table', class_='infobox')

            if infobox:
                entete = infobox.find('div', class_='entete')
                nom_complet = entete.get_text(strip=True) if entete else soup.find('h1').get_text(strip=True)
                nom_complet = nom_complet.replace("Sir ", "")

                # Initialisation du genre
                if any(femme.lower() in nom_complet.lower() for femme in femmes_noms):
                    infos_du_pilote["dGender"] = "F"
                else:
                    infos_du_pilote["dGender"] = "H"

                # On sépare le nom complet en deux, le prénom et le nom
                if nom_complet in noms_composes:
                    infos_du_pilote["dFirstName"], infos_du_pilote["dLastName"] = noms_composes[nom_complet]
                else:
                    parties = nom_complet.split()
                    if len(parties) >= 2:
                        infos_du_pilote["dFirstName"] = parties[0]
                        nom_famille_parts = [parties[-1]]
                        i = len(parties) - 2
                        while i > 0:
                            if parties[i].lower() in particules:
                                nom_famille_parts.insert(0, parties[i])
                                i -= 1
                            else:
                                break
                        infos_du_pilote["dLastName"] = " ".join(nom_famille_parts)
                    else:
                        infos_du_pilote["dFirstName"] = nom_complet
                        infos_du_pilote["dLastName"] = ""

                # La on fait un parcours pour récupérer les infos dans l'infobox
                for ligne in infobox.find_all('tr'):
                    titre = ligne.find('th')
                    reponse_td = ligne.find('td')
                    if titre and reponse_td:
                        categorie = titre.get_text(strip=True)
                        # On tilise le mapping pour trouver le nom de colonne CSV correspondant
                        if categorie in category_to_column:
                            csv_column_name = category_to_column[categorie]
                            # NETTOYAGE : remplacement des espaces insécables (\xa0) par des espaces normaux
                            info = reponse_td.get_text(" ", strip=True).replace('\xa0', ' ')
                            info = re.sub(r'\[.*?\]', '', info) # Enlève les éléments dans des []
                            info = re.sub(r'\(.*?\)', '', info).strip() # Enlève les éléments dans des ()

                        # réglage pb de nationalité 
                            if csv_column_name == "dCountry":
                                info_low = info.lower() 
                                pays_trouve = "Null"
                                for variante, pays_propre in mapping_nationalites.items():
                                    if variante in info_low:
                                        pays_trouve = pays_propre
                                        break
                                info = pays_trouve if pays_trouve != "Null" else info.capitalize()

                            # Modification des dates pour avoir le résultat YYYY-MM-DD
                            if csv_column_name in ["dBirthdate", "dDeathdate"]:
                                # NETTOYAGE : suppression de "1er" ou "1 er"
                                texte_date = info.lower().replace('1 er', '1').replace('1er', '1')
                                # REGEX : assouplissement pour capturer la date n'importe où dans la cellule
                                date_match = re.search(r'(\d{1,2})\s+([a-z\u00e0-\u00ff]+)\s+(\d{4})', texte_date)

                                if date_match:
                                    jour = date_match.group(1).zfill(2)
                                    nom_mois = date_match.group(2)
                                    annee = date_match.group(3)
                                    chiffre_mois = mois.get(nom_mois)

                                    if chiffre_mois:
                                        info = f"{annee}-{chiffre_mois}-{jour}"

                            infos_du_pilote[csv_column_name] = info


                writer.writerow(infos_du_pilote)
                driverID += 1
                print(f"Ajouté : {infos_du_pilote['dFirstName']} {infos_du_pilote['dLastName']}")
                time.sleep(0.1)

print("Traitement terminé, tout est propre !")