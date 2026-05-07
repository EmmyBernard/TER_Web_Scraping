import csv 
import os 

os.getcwd()
os.chdir("/Users/emmybernard/Library/Mobile Documents/com~apple~CloudDocs/MIASHS/L3MIASHS/S6/TER/CODE_season")

with open("Season_infos_supplémentaires.csv", "r", encoding = "utf-8") as f: 
    reader = csv.DictReader(f)
    with open("Season_final.csv", "w", encoding="utf-8") as fich: 
        writer = csv.DictWriter(fich, fieldnames=["seasonID", "seTires", "seWorldChamp", "seConstChamp", "seFixedNb"])
        writer.writeheader()

        for row in reader: 
            dic_propre = {"seasonID" : row["id"],
                          "seTires" : row["seTires"],
                          "seWorldChamp" : row["Champion"],
                          "seConstChamp" : row["Champion_constructeur"],
                          "seFixedNb" : row["seNbFixed"]}
            writer.writerow(dic_propre)

