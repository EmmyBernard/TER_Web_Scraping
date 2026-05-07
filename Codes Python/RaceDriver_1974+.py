import csv
import os
from datetime import datetime
import re
from pprint import pprint


# os.getcwd()
# BIEN VERIFIER L'EMPLACEMENT DANS LE WORKSPACE


#************************************************************************************************************************************************************
#Pour des questions de modélisations, on exclus les années de 1950 à 1973 inclus, car les numéro étaient fixé selon l'ordre d'inscription à un Grand Prix 
# ************************************************************************************************************************************************************




#liste de dictionnaire sans doublons à partir du fichier RaceDriver_infos_supplémentaires.csv
lst_sans_double = []
with open("RaceDriver_infos_supplémentaires.csv", "r", encoding='utf-8') as f: 
    reader = csv.DictReader(f)

    #parcours ligne par ligne 
    for ligne in reader : 

        #éviter les lignes vides
        if int(ligne["season"]) >= 1974 and ligne["pilote"] and ligne["ecurie"]  :
            

            #Dans StatsF1, le nom du chassis est souvent le nom de l'écurie retenue dans la table TEAM
            #Quand le nom du chassis est présent dans celui de l'écurie on ne garde que le nom du chassis afin de faire le lien avec la table TEAM
            if ligne["chassis"].strip().lower() in ligne["ecurie"].strip().lower() :
                 ligne["ecurie"] = ligne["chassis"]
            
            #Si une écurie est privée, alors on lui attribue une écurie NULL
            if ligne["ecurie"].strip() == "Privé" :
                 ligne["ecurie"] = None 




#**********************
# CHOIX DE MODÉLISATION : mettre moteur et pneu dans RaceDriver
#**********************


#le dictionnaire contient les informations complètes avant la jointure

            dic = {"#seasonID" : ligne["season"],
                "rDriverNb" : ligne["num"],
                "#driverID" : ligne["pilote"],
                "#teamID" : ligne["ecurie"],
                "rTyres" : ligne["pneu"],
                "rMotor" : ligne["moteur"]}
            
            #évite les doublons
            if dic not in lst_sans_double: 
                lst_sans_double.append(dic)

        
# écriture du fichier final sans les associations         
with open("RaceDriver_sans_jointure.csv", "w", encoding='utf-8') as f_final : 
        writer = csv.DictWriter(f_final, fieldnames=["#teamID", "#driverID", "#seasonID", "rDriverNb", "rTyres", "rMotor"])
        writer.writeheader()
        writer.writerows(lst_sans_double)


# un prochain script devrait faire les associations (RaceDriver_Driver_Team_jointure.py)