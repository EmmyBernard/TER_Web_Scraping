import csv
import re


## Fonction


def verifier_csv(nom_fichier):
    lignes_erreurs = []

    with open(nom_fichier, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        n = 1
        for ligne in reader:  

            n += 1 

            for i in reader.fieldnames:
                if '[' in ligne[i] : 
                    lignes_erreurs.append((n, ligne[i]))


    # Affichage des résultats
    if lignes_erreurs:
        print(f"{len(lignes_erreurs)} lignes problématiques trouvées :")
        for num, contenu in lignes_erreurs:
            print(f"Ligne {num} : {contenu}")
    else:
        print("Aucune erreur de format détectée.")


### Programme principal


fichier_entree = 'Circuit_sans_jointure_pas_nettoye.csv'
fichier_sortie = 'Circuit_final.csv'
fichier_pilotes = 'Driver_final.csv'




pattern = re.compile(r'\((.*?)\)')      # pour enlever de la colonne version les dates
pattern_dates_GP_plage_centre = re.compile(r'^(.*?)(Grand Prix Circuit)\s\((\d{4})\–(\w+)\)(.*?)$') # pour les plages de dates qui se trouvent entre plusieurs chaines de caractere
pattern_dates_GP_seule = re.compile(r'^(.*?)(Grand Prix Circuit)\s\((\d{4})\)')                     # pour les dates année unique
pattern_dates_GP_multi = re.compile(r'^(.*?)(Grand Prix Circuit)\s\((.*?)(,|and)(.*?)\)')           # pour les dates ou il y a plusieurs années qui ne se suivent pas
pattern_dates_GP_plage_fin = re.compile(r'^(.*?)(Grand Prix Circuit)\s(.*?)\((\d{4})\–(\w+)\)')     # pour les plages de dates seules
    
pattern_date_seule = re.compile(r'^(.*?)\s\((\d{4})\)')                         # pour les dates uniques
pattern_date_plage_fin = re.compile(r'^(.*?)\((\d{4})\–(\w+)\)')                # pour les plages de dates seules
pattern_date_plage_centre = re.compile(r'^(.*?)\s\((\d{4})\–(\w+)\)(.*?)$')     # pour les plages de dates au milieu du texte
pattern_date_multi = re.compile(r'^(.*?)\s\((.*?)(,|and)(.*?)\)')               # pour les dates ou il y a plusieurs années qui ne se suivent pas


pattern_lon = re.compile(r'(\d)\.(\d+)\s(mi)')      # pour les longueurs qui sont en miles


with open(fichier_entree, 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        # On ajoute la nouvelle colonne pour les dates et l'identifiant circuit
        nouveaux_champs = reader.fieldnames + ['cDates'] + ['circuitID'] + ['Error']

        id = 0

        with open(fichier_sortie, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=nouveaux_champs)
            writer.writeheader()

            for ligne in reader:

                id += 1
                ligne['circuitID'] = id     # On implémente l'identifiant

                nom_trouve = False
                date_trouve = True

                # Jointure avec la table pilote
                with open(fichier_pilotes, 'r', encoding='utf-8') as fich:
                    reader2 = csv.DictReader(fich)

                    for l in reader2:

                        nom_complet = l['dFirstName'] + ' '+ l['dLastName']
                        if nom_complet == ligne['cDrivRec'] :
                                ligne['cDrivRec'] = l['driverID']
                                nom_trouve = True
                        elif ligne['cDrivRec'] == 'NULL':
                                nom_trouve = True


                # Longueurs incorrectes converties en km
                longueur = ligne["cLength"]
                match = pattern_lon.search(longueur)

                if match:
                    miles = match.group(1) + match.group(2)
                    miles = int(miles)/1000
                    distance_km = round(miles*1.60923, 3)
                    ligne['cLength'] = f'{distance_km} km'


                # Extraction des dates de la colonne cVersion et remplissage de la colonne cDates
                version_texte = ligne['cVersion']
                # Les circuits qui ont des records
                match1 = pattern_dates_GP_plage_centre.fullmatch(version_texte)
                match2 = pattern_dates_GP_seule.search(version_texte)
                match3 = pattern_dates_GP_multi.match(version_texte)
                match4 = pattern_dates_GP_plage_fin.match(version_texte)

                # Les circuits qui n'ont pas de records
                match5 = pattern_date_plage_centre.fullmatch(version_texte)
                match6 = pattern_date_seule.search(version_texte)
                match7 = pattern_date_multi.match(version_texte)
                match8 = pattern_date_plage_fin.match(version_texte)

                if match1 : 
                    ligne['cDates'] = f'{match1.group(3)}-{match1.group(4)}'
                    ligne['cVersion'] = pattern.sub('', version_texte).strip() 
                    

                elif match2:
                    ligne['cDates'] = match2.group(3)
                    ligne['cVersion'] = pattern.sub('', version_texte).strip()
                    

                elif match3 :
                    new_ligne = ligne.copy()
                    new_ligne['cDates'] = f'{match3.group(5)}'
                    writer.writerow(new_ligne)
                    ligne['cDates'] = f'{match3.group(3)}'
                    ligne['cVersion'] = pattern.sub('', version_texte).strip()
                                     

                elif match4 :
                    ligne['cDates'] = f'{match4.group(4)}-{match4.group(5)}'
                    ligne['cVersion'] = pattern.sub('', version_texte).strip()


                elif match5:
                    ligne['cDates'] = f'{match5.group(2)}-{match5.group(3)}'
                    ligne['cVersion'] = pattern.sub('', version_texte).strip()
                

                elif match6:
                    ligne['cDates'] = match6.group(2)
                    ligne['cVersion'] = pattern.sub('', version_texte).strip()


                elif match7:
                    new_ligne = ligne.copy()
                    new_ligne['cDates'] = f'{match7.group(4)}'
                    writer.writerow(new_ligne)
                    ligne['cDates'] = f'{match7.group(2)}'
                    ligne['cVersion'] = pattern.sub('', version_texte).strip()

                
                elif match8:
                    ligne['cDates'] = f'{match8.group(2)}-{match8.group(3)}'
                    ligne['cVersion'] = pattern.sub('', version_texte).strip()
                    

                else:
                    ligne['cDates'] = ""
                    date_trouve = False
                    # On ne retire pas les dates de la colonne cVersion puisque dans ce cas particulier il faudra aller les recopier à la main

                ligne['cDates'] = re.sub(r'present', '2026', ligne['cDates'], flags=re.IGNORECASE)  # Remplacement de 'present' par 2026

                # Remplissage de la colonne Error
                if not date_trouve and not nom_trouve:
                    ligne['Error'] = 'Date_Pilote_Introuvables'
                elif date_trouve and not nom_trouve:
                    ligne['Error'] = 'Pilote_Introuvable'
                elif not date_trouve and nom_trouve:
                    ligne['Error'] = 'Date_Incompatible'

                    
                writer.writerow(ligne)

# Vérification du csv pour les crochets de Wikipédia à retirer a la main
verifier_csv(fichier_sortie)
