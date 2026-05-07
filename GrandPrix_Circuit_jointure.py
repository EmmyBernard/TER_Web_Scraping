import csv
import os
from datetime import datetime
import re

os.getcwd()
os.chdir( "/Users/emmybernard/Library/Mobile Documents/com~apple~CloudDocs/MIASHS/L3MIASHS/S6/TER/CODE-GrandsPrix")

#rappel format GP 
# {"gpID" : row["gpID"],
# "gName" : row["gName"], 
# "circuitID#" : None, 
# "gDate" : row['gDate'], 
# "gLaps" : row['gLaps'], 
# "gRank" : row['gRank']} 

#clés circuit 
# cName,cCity,
# cCountry,cVersion,
# cLength,cLapRec,
# cYearRec,cDrivRec,
# cDates,circuitID

#Liste de dictionnaire des circuits
with open("Circuit_final.csv", "r", encoding="utf-8") as fich:
    # On transforme le reader en une vraie liste de dictionnaires
    liste_circuits = list(csv.DictReader(fich))

with open("GrandPrix_infos_supplémentaires.csv", "r", encoding="utf-8") as f_gp : 
    reader_GP = csv.DictReader(f_gp)
    print(reader_GP.fieldnames)

    with open("GrandPrix_final.csv", "w", encoding='utf-8') as f_final:
        writer = csv.DictWriter(f_final, fieldnames=['gpID', 'gName', 'circuitID#', 'gDate', 'gLaps', 'gRank', 'error'])
        writer.writeheader()
    
            
        for gp in reader_GP:

            dic_propre = {"gpID" : gp["gpID"],
                          "gName" : gp["gName"], 
                          "circuitID#" : gp["NomCircuit"], 
                          "gDate" : gp['gDate'], 
                          "gLaps" : gp['gLaps'], 
                          "gRank" : gp['gRank'],
                          "error" : None} 

            NOM_Trouve = False
            TOTAL_Trouve = False


            #infos nécéssaire de la table gp pour faire le lien 
            gDate = datetime.strptime(gp["gDate"], "%Y-%m-%d %H:%M:%S")
            annee_gp = int(gDate.year) #récupération de l'année seulement 
            Nom_circuitID = str(gp["NomCircuit"]).lower().strip()
            

            for circuit in liste_circuits:
                nom_circuit = str(circuit["cName"].lower().strip())
                circuitID = int(circuit["circuitID"])
                
                condition_periode = re.findall(r'\d{4}(-|–)\d{4}',circuit["cDates"]) #vrai si liste non vide 
                condition_date = re.findall(r'^\s*\d{4}\s*$',circuit["cDates"]) #vrai si liste non vide 

                if nom_circuit == Nom_circuitID : #Recherche d'une correspondance de nom
                    NOM_Trouve = True

                    if condition_periode : 
                        annee_deb = int(re.findall(r'(\d{4})(?:-|–)\d{4}',circuit["cDates"])[0])
                        annee_fin = int(re.findall(r'\d{4}(?:-|–)(\d{4})',circuit["cDates"])[0])

                        if annee_gp in range(annee_deb,annee_fin+1):
                            dic_propre["circuitID#"] = circuitID
                            print(f"{nom_circuit} de {annee_gp} correspondance Nom et années ")
                            TOTAL_Trouve = True
                            break
                    
                    if condition_date : 
                        annee = int(condition_date[0])
                        if annee == annee_gp :
                            dic_propre["circuitID#"] = circuitID
                            print(f"{nom_circuit} de {annee_gp} correspondance Nom et année ")
                            TOTAL_Trouve = True
                            break

            if TOTAL_Trouve : 
                dic_propre["error"] = None
            
            elif NOM_Trouve : 
                dic_propre["error"] = "Dates_Circuit"
            
            else : 
                dic_propre["error"] = "Nom_Introuvable"
            
            writer.writerow(dic_propre)                





    