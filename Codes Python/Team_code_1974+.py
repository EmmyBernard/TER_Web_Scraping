import csv
import time
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)
headers = {"User-Agent": "Mozilla/5.0"}

dictionnaire_noms_ecuries = {
"A-T-S":"Automobili Turismo e Sport",
"Adams":"NULL",
"AFM" :"Alex von Falkenhausen",
"AGS":"Automobiles Gonfaronnaises Sportives",
"Alfa Romeo":"Alfa Romeo (Formule 1)",
"Alfa Special":"NULL",
"AlphaTauri":"NULL",
"Alpine":"NULL",
"Alta":"Alta Car and Engineering",
"Amon":"NULL",
"Andrea Moda":"Andrea Moda Formula",
"Apollon":"Apollon Racing",
"Arrows":"Arrows",
"Arzani Volpini":"NULL",
"Aston":"WS Aston",
"Aston Marten":"Aston Martin F1 Team",
"ATS":"Auto Technisches Spezialzubehör",
"Audi":"NULL",
"BAR":"British American Racing",
"Bardazon":"NULL",
"Bellasi":"Bellasi",
"Benetton":"Benetton Formula",
"Berta":"NULL",
"BMW":"NULL",
"BMW Sauber":"BMW Sauber F1 Team",
"Boro":"Boro (Formule 1)",
"Brabham":"Brabham Racing Organisation",
"Brawn GP":"Brawn GP Formula One Team",
"BRM":"British Racing Motors",
"Bromme":"NULL",
"BRP":"British Racing Partnership",
"Bugatti":"Bugatti",
"Cadillac":"NULL",
"Cantarano":"NULL",
"Caterham":"Caterham F1 Team",
"Christensen":"NULL",
"Christy":"NULL",
"Cisitalia":"NULL",
"Clemons":"NULL",
"Coloni":"Coloni",
"Connaught":"Connaught Engineering",
"Connew":"Connew Racing team",
"Cooper":"Cooper Car Company",
"Copersucar":"Fittipaldi Automotive",
"Cornis":"NULL",
"Cosworth":"NULL",
"Dallara":"Dallara",
"De Tomaso":"De Tomaso",
"Deidt":"NULL",
"Del Roy":"NULL",
"Dunn":"NULL",
"Eagle":"Eagle (Formule 1)",
"Eifelland March":"Eifelland Racing",
"Ekström":"NULL",
"EL":"NULL",
"Elder":"NULL",
"Emeryson":"Emeryson",
"EMW":"Eisenacher Motorenwerk",
"ENB":"Equipe Nationale Belge",
"Ensign":"Ensign",
"Epperly":"NULL",
"ERA":"English Racing Automobile",
"Eurobrun":"Eurobrun Racing",
"Ewing":"NULL",
"Ferguson":"Massey Ferguson",
"Ferrari":"Scuderia Ferrari",
"Fittipaldi":"Fittipaldi Automotive",
"Fondmental":"Fondmental",
"Footwork":"Footwork racing",
"Force India":"Force India",
"Forti":"Forti Corse",
"Frazer Nash":"Frazer Nash",
"Fry":"NULL",
"Gdula":"NULL",
"Gerhardt":"NULL",
"Gilby":"Gilby Engineering",
"Gordini":"Gordini",
"Haas":"Haas F1 Team",
"Hall":"NULL",
"Hesketh":"Hesketh Racing",
"Hill":"Embrassy-Hill",
"Hillegass":"NULL",
"Honda":"Honda Racing F1 Team ",
"HRT":"HRT Formula One Team",
"HWM":"Hersham and Walton Motors",
"JBW":"JBW",
"Jaguar":"Jaguar Racing",
"Johnson":"NULL",
"Jordan":"Jordan Grand Prix",
"Kauhsen":"NULL",
"Kick Sauber":"Sauber",
"Klenk":"Klenk",
"Koehnle":"NULL",
"Kojima":"Kojima Engineering",
"Kupiec":"NULL",
"Kurtis Kraft":"Kurtis Kraft",
"Kuzma":"NULL",
"Lamborghini":"NULL",
"Lancia":"NULL",
"Langley":"NULL",
"Larousse":"Larousse",
"LDS":"LDS (Formule 1)",
"LEC":"LEC Refrigeration Racing",
"Lesovsky":"NULL",
"Leyton House":"NULL",
"Life":"Life racing Engines",
"Ligier":"Ligier",
"Lola":"Haas Lola",
"Lotus":"Lotus F1 Team",
"Lyncar":"Lyncar",
"Maki":"NULL",
"Manor":"Manor Racing",
"March":"March Engineering",
"Marchese":"NULL",
"Martini":"Automobiles Martini",
"Marussia":"Marussia F1 Team",
"Maserati":"Officine Alfieri Maserati",
"Maserati Milano":"NULL",
"Matra":"Matra Sports",
"MBM":"Monteverdi",
"McGuire":"McGuire (Formule 1)",
"McLaren":"MacLaren Racing",
"Mercedes":"Mercedes Grand Prix",
"Merzario":"Team Merzario",
"Meskowski":"NULL",
"Meyer":"NULL",
"Midland":"Midland F1 Racing",
"Miller":"NULL",
"Minardi":"Scuderia Minardi",
"Monteverdi":"Monteverdi (automobile)",
"Moore":"NULL",
"MSM":"NULL",
"Nichels":"NULL",
"Olson":"NULL",
"Onyx":"Onyx Grand Prix",
"OSCA":"O.S.C.A",
"Osella":"Osella",
"Pacific":"Pacific racing",
"Pankratz":"NULL",
"Parnelli":"Vel's Parnelli Jones Racing",
"Pawl":"NULL",
"Penske":"Penske racing",
"Phillips":"NULL",
"Politoys":"NULL",
"Porsche":"Porsche Team",
"Prost":"Prost Grand Prix",
"R Miller":"NULL",
"Racing Bulls":"NULL",
"Racing Point":"Racing Point F1 Team",
"Rae":"NULL",
"RAM":"RAM Racing",
"RAM March":"RAM March",
"Rassey":"NULL",
"RB":"NULL",
"Realpha":"NULL",
"Rebaque":"Team Rebaque",
"Red Bull":"Red Bull Racing",
"Renault":"NULL",
"Rial":"Rial Racing",
"Rounds Rocket":"NULL",
"Sauber":"Sauber",
"Scarab":"Scarab-Reventlow Automobiles",
"Schroeder":"NULL",
"Scirocco":"Scirocco-Powell",
"Scopa":"NULL",
"Shadow":"Shadow Racing Cars",
"Shannon":"Shannon racings Cars",
"Sherman":"NULL",
"Shilala":"NULL",
"Silnes":"NULL",
"Simca Gordini":"Gordini",
"Simtek":"Simtek",
"Snowberger":"NULL",
"Spirit":"Spirit Racing",
"Spyker":"Spyker F1 Team",
"Stebro":"Stebro",
"Stevens":"NULL",
"Stewart":"Stewart Grand Prix",
"Super Aguri":"Super Aguri Formula F1 Team",
"Surtees":"Surtees Racing Organisation",
"Sutton":"NULL",
"SVA":"NULL",
"Szalai":"NULL",
"Talbot Lago":"Talbot",
"Talbot-Darracq":"NULL",
"Tec Mec":"NULL",
"Tecno":"Tecno",
"Templeton":"NULL",
"Theodore":"Theodore Racing",
"Token":"Token racing",
"Toleman":"Toleman",
"Toro Rosso":"NULL",
"Toyota":"Toyota F1 Team",
"Trevis":"NULL",
"Trojan":"Trojan-Tauranac Racing",
"Trussardi":"NULL",
"Turner":"NULL",
"Tyrrell":"Tyrrell Racing",
"Vanwall":"Vanwall",
"Venturi":"Venturi Automobiles",
"Veritas":"Veritas (entreprise)",
"Virgin":"Virgin Racing",
"Voelker":"NULL",
"Watson":"NULL",
"Watts":"NULL",
"Weidel":"NULL",
"Wetteroth":"NULL",
"Williams":"Williams F1 Team",
"Wolf":"Walter Wolf Racing",
"Zakspeed":"Zakspeed",
}


tous_les_liens_statsf1 = []
periodes_equipes_uniques = {}

try:
   
    for lettre in "abcdefghijklmnopqrstuvwxyz":
        print(f"Lettre : {lettre.upper()}")
        driver.get(f"https://www.statsf1.com/fr/constructeurs-{lettre}.aspx")
        try:
            tableau = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ctl00_CPH_Main_GV_Constructeur"))
            )
            lignes = tableau.find_elements(By.CSS_SELECTOR, "tbody tr")
            for ligne in lignes:
                cellules = ligne.find_elements(By.TAG_NAME, "td")
                if len(cellules) < 3: continue
                lien = cellules[0].find_element(By.TAG_NAME, "a")
                tous_les_liens_statsf1.append({
                    "nom_base": lien.text.strip(),
                    "url_stats": lien.get_attribute("href"),
                    "pays": cellules[1].find_element(By.TAG_NAME, "img").get_attribute("alt") if cellules[1].find_elements(By.TAG_NAME, "img") else "N/A",
                    "annees_brutes": cellules[2].text.strip()
                })
        except: continue

   
    
    for item in tous_les_liens_statsf1:
        driver.get(item['url_stats'])
        try:
            blocs = driver.find_elements(By.XPATH, "//*[contains(text(), 'Filiation :')]/..")
            if blocs:
                texte_f = blocs[0].text.split("Team Principal")[0].replace("Filiation :", "").strip()
                segments = [s.strip('• ').strip() for s in texte_f.split('➜') if s.strip()]
                dernier_id_parent = None
                for seg in segments:
                    nom_seg = re.search(r'^[^(\n]+', seg).group(0).strip()
                    dates_seg = re.search(r'\((.*?)\)', seg).group(1).strip() if "(" in seg else item['annees_brutes']
                    
                    ans = re.findall(r'\d{4}', dates_seg)
                    debut = ans[0] if ans else "NULL"
                    fin = "NULL" if "-" in dates_seg and dates_seg.strip().endswith("-") else (ans[1] if len(ans) > 1 else debut)
                    
                    uid = f"{nom_seg} ({dates_seg})"
                    if uid not in periodes_equipes_uniques:
                        periodes_equipes_uniques[uid] = {"nom": nom_seg, "debut": debut, "fin": fin, "pays": item['pays'], "parent_uid": dernier_id_parent}
                    dernier_id_parent = uid
            else:
                ans = re.findall(r'\d{4}', item['annees_brutes'])
                debut = ans[0] if ans else "NULL"
                fin = "NULL" if "-" in item['annees_brutes'] and item['annees_brutes'].strip().endswith("-") else (ans[-1] if len(ans) > 1 else debut)
                uid = f"{item['nom_base']} ({item['annees_brutes']})"
                if uid not in periodes_equipes_uniques:
                    periodes_equipes_uniques[uid] = {"nom": item['nom_base'], "debut": debut, "fin": fin, "pays": item['pays'], "parent_uid": None}
        except: continue

    
   
    cles_triees = sorted(periodes_equipes_uniques.keys(), key=lambda x: x.lower())
    
    id_numerique_complet = {cle: i for i, cle in enumerate(cles_triees, 1)}
    
    donnees_finales = []

    for cle in cles_triees:
        equipe = periodes_equipes_uniques[cle]
        
        
        try:
            annee_debut_entier = int(equipe['debut'])
        except (ValueError, TypeError):
            annee_debut_entier = 0 
            
        
        if annee_debut_entier < 1974 and annee_debut_entier != 0:
            continue
        

        
        donnees_finales.append({
            'teamID': id_numerique_complet[cle],
            'tName': equipe['nom'],
            'tCountry': equipe['pays'],
            'tstart': equipe['debut'],
            'tend': equipe['fin'],
            'twas': id_numerique_complet.get(equipe['parent_uid'], "NULL") if equipe['parent_uid'] else "NULL"
        })

    # 4. EXPORT CSV
    with open('Team_1974+.csv', 'w', newline='', encoding='utf-8-sig') as f:
        champs = ['teamID', 'tName', 'tCountry', 'tstart', 'tend', 'twas']
        ecrivain = csv.DictWriter(f, fieldnames=champs, delimiter=';')
        ecrivain.writeheader()
        ecrivain.writerows(donnees_finales)

finally:
    driver.quit()
    print("\nTerminé")