import csv
from datetime import datetime
import re


### Fonctions

# Vérification du nombre de GP par année
def verif_nombre_gp(i):
    fich_csv = f"standings_{i}.csv"

    f_season = 'Season_infos_supplémentaires.csv'

    with open(fich_csv, 'r', encoding='utf-8') as f_standings:
        reader = csv.DictReader(f_standings)

        liste_noms = []
        nb_gp = 0

        for ligne in reader:
            if (ligne['sSeason'], ligne["gpID"] ) not in liste_noms:
                liste_noms.append((ligne['sSeason'], ligne['gpID']))

        with open(f_season, 'r', encoding='utf-8') as f_verif : 
            reader1 = csv.DictReader(f_verif)

            for ligne in reader1:
                if ligne['id'] == str(i):
                    nb_gp = int(ligne['Nb_GP'])

    return len(liste_noms) == nb_gp


# Ajout de chaque incidents des grands prix dans un set
def ajouter_dans_set(fichier_entree):
    with open(fichier_entree, 'r', encoding='utf-8') as fich_original :
        reader = csv.DictReader(fich_original)

        s = set()

        for ligne in reader:
            incident = ligne['sInc']
            s.add(incident)
    return s




### Programme principal

fichier_pilotes = 'Driver_final.csv'
fichier_grand_prix = 'GrandPrix_final.csv'
annees = [a for a in range(1950, 2027)]
annee_en_cours = 2026

incidents = set()
for i in annees:
    if verif_nombre_gp(i):
        incidents = incidents.union(ajouter_dans_set(f'standings_{i}.csv'))   

    

print(incidents) # Utilisé pour la requête IA


dic_incidents = {}

# --- Catégorie 1 : Problèmes Techniques (Internes/Systèmes) ---
problemes_techniques = [
    'Alternator', 'Battery', 'Clutch', 'Cooling system', 'Crankshaft', 
    'CV joint', 'Differential', 'Distributor', 'Driveshaft', 'Drivetrain', 
    'Electrical', 'Electronics', 'Engine', 'Engine fire', 'Engine misfire', 
    'ERS', 'Exhaust', 'Fuel leak', 'Fuel pipe', 'Fuel pressure', 'Fuel pump', 
    'Fuel system', 'Gearbox', 'Halfshaft', 'Hydraulics', 'Ignition', 
    'Injection', 'Launch control', 'Magneto', 'Mechanical', 'Oil leak', 
    'Oil line', 'Oil pipe', 'Oil pump', 'Oil pressure', 'Overheating', 
    'Pneumatics', 'Power loss', 'Power Unit', 'Radiator', 'Spark plugs', 
    'Supercharger', 'Technical', 'Throttle', 'Transmission', 'Turbo', 
    'Water leak', 'Water pipe', 'Water pressure', 'Water pump'
]

# --- Catégorie 2 : Problèmes Extérieurs (Châssis/Aéro/Liaison au sol) ---
problemes_exterieurs = [
    'Axle', 'Brake duct', 'Brakes', 'Broken wing', 'Chassis', 'Damage', 
    'Debris', 'Front wing', 'Handling', 'Heat shield fire', 'Rear wing', 
    'Steering', 'Suspension', 'Track rod', 'Tyre', 'Tyre puncture', 
    'Puncture', 'Undertray', 'Vibrations', 'Wheel', 'Wheel bearing', 
    'Wheel nut', 'Wheel rim'
]

# --- Catégorie 3 : Pilote (Santé/Sécurité) ---
problemes_pilote = [
    'Driver Seat', 'Seat', 'Driver unwell', 'Illness', 'Eye injury', 
    'Fatal accident', 'Injured', 'Injury', 'Physical', 'Safety', 
    'Safety belt', 'Safety concerns'
]

# --- Catégorie 4 : Accidents et Sorties ---
accidents = [
    'Accident', 'Collision', 'Collision damage', 'Fire', 'Spun off', 'Stalled'
]

# --- Catégorie 5 : Stratégie et Gestion ---
strategie_gestion = [
    'Fuel', 'Fuel rig', 'Not restarted', 'Out of fuel', 'Refuelling', 'Withdrew'
]

# --- Éléments exclus (Status / Sanctions) ---
# DNF, DNS, Did not start, DQ, RAS, NULL, Excluded, Underweight, Lapped, Not classified


for inc in incidents:
    if inc in problemes_techniques :
      dic_incidents[inc] = 'Technical'
    elif inc in problemes_exterieurs :
      dic_incidents[inc] = 'Car related'
    elif inc in problemes_pilote : 
      dic_incidents[inc] = 'Driver related'
    elif inc in strategie_gestion : 
      dic_incidents[inc] = 'Strategy'
    elif inc in accidents : 
      dic_incidents[inc] = 'Accident'
   


colonnes = ['sSeason','gpID','driverID','sPos','sPoints','sGrid','sLaps','sInc', 'Error']



with open("Standings_final.csv", 'a', newline='', encoding='utf-8') as fich_complet:
    writer = csv.DictWriter(fich_complet, fieldnames=colonnes)
    writer.writeheader()

    for i in annees:
        if verif_nombre_gp(i) or i == annee_en_cours:
            with open(f"standings_{i}.csv", 'r', encoding='utf-8') as fichier_annee:
                reader = csv.DictReader(fichier_annee)         

                for ligne in reader : 

                    nom_trouve = False
                    gp_trouve = False


                    inc_course = ligne['sInc']

                    for cle, valeur in dic_incidents.items():
                        if inc_course == cle :
                            ligne['sInc'] = valeur

                    if inc_course.lower() == 'did not start':
                            ligne['sInc'] = 'DNS'
                    elif inc_course.lower() == 'lapped':
                            ligne['sInc'] = 'RAS'
                    elif inc_course.lower() == 'not classified':
                            ligne['sInc'] = 'NC'
                    elif inc_course.lower() == 'underweight' or inc_course.lower() =='excluded':
                            ligne['sInc'] = 'DQ'


                    with open(fichier_pilotes, 'r', encoding='utf-8') as fich:
                        reader2 = csv.DictReader(fich)

                        for l in reader2:

                            nom_complet = l['dFirstName'] + ' '+ l['dLastName']
                            if nom_complet == ligne['driverID'] :
                                ligne['driverID'] = l['driverID']
                                nom_trouve = True

                    with open(fichier_grand_prix, 'r', encoding='utf-8') as fich:
                        reader3 = csv.DictReader(fich)

                        for l in reader3:
                            date_csv = datetime.strptime(l['gDate'], "%Y-%m-%d %H:%M:%S")
                            date = date_csv.year
                            if ligne['sSeason'] == str(date):
                                if ligne['gpID'] == l['gName']:
                                    ligne['gpID'] = l['gpID']
                                    gp_trouve = True
                    

                    if not gp_trouve and not nom_trouve :
                        ligne['Error'] = 'GP_Pilote_Introuvables'
                    elif gp_trouve and not nom_trouve:
                        ligne['Error'] = 'Pilote_Introuvable'
                    elif not gp_trouve and nom_trouve:
                        ligne['Error'] = 'GP_Introuvable'
                
                    
                    writer.writerow(ligne)

        else:
            print(f"Le fichier de l'année {i} est incomplet")
        
    print('Fichier chargé')
            





 