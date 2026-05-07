import csv
import os
from datetime import datetime
import re

# os.getcwd()
# BIEN VERIFIER L'EMPLACEMENT DANS LE WORKSPACE


#RaceDriver en liste 
with open("RaceDriver_sans_jointure.csv", "r", encoding="utf-8") as f : 
    # On transforme le reader en une vraie liste de dictionnaires
    liste_racedriver = list(csv.DictReader(f)) #au fur et à mesure on modifiera cette liste avec les identifiants nécessaires 
 

#Table pilote en liste 
with open("Driver_final.csv", "r", encoding="utf-8") as f_driver :
    liste_driver = list(csv.DictReader(f_driver))

#Table Team en liste : 
with open("Team_final.csv", "r", encoding="utf-8") as f_team :
    liste_team = list(csv.DictReader(f_team, delimiter=";"))
    
    


#******RAPPEL STRUCTURE*******
#Race Driver : #teamID,#driverID,#seasonID,rDriverNb,rTyres,rMotor
#Driver : driverID,dFirstName,dLastName,dBirthdate,dDeathdate,dCountry,dGender
#Team : teamID;tName;tCountry;tstart;tend;twas


with open("RaceDriver_final.csv", "w", encoding = "utf-8") as f_final : 
    writer = csv.DictWriter(f_final, fieldnames = ["#teamID","#driverID","#seasonID","rDriverNb","rTyres","rMotor", "error"])
    writer.writeheader()

    

    
    for RD in liste_racedriver : 
        # exemple du contenu d'une case DriverID dans RaceDriver avant la jointure : "Ronnie PETERSON" ou "Ryo HIRAKAWA *" (troisième pilote) ou avec la particule "de" ou prénom composé
        nom_complet_rd = RD["#driverID"].strip().lower() #Nom du pilote de la table RaceDriver
        nom_team_rd = RD["#teamID"].strip().lower()

        ID_DRIVER_RECUP = False 
        ID_TEAM_RECUP = False 

        #jointure avec DRIVER
        for driver in liste_driver:
            nom_d, prenom_d = driver['dLastName'].strip().lower(), driver['dFirstName'].strip().lower()
            driver_id = driver["driverID"]

            if nom_d in nom_complet_rd and prenom_d in nom_complet_rd : 
                ID_DRIVER_RECUP = True 
                RD["#driverID"] = driver_id
    
   

        #jointure avec TEAM
        for team in liste_team:
            nom_team = team["tName"].strip().lower()
            team_id = team["\ufeffteamID"]

            if nom_team == nom_team_rd : 
                ID_TEAM_RECUP = True 
                RD["#teamID"] = team_id


        

        #remplissage de la colonne error 
        if not ID_DRIVER_RECUP and  not ID_TEAM_RECUP : 
            RD["error"] = "DRIVER & TEAM"
        elif not ID_TEAM_RECUP :
            RD["error"] = "TEAM"
        elif not ID_DRIVER_RECUP :
            RD["error"] = "DRIVER"
        else : 
            RD["error"] = None 
            


        writer.writerow(RD)
                                
            


    


