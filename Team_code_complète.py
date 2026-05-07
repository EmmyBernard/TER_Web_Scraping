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

jj = {
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

unique_periods = {}
all_links = []

try:
    # 1. COLLECTE STATSF1
    for lettre in "abcdefghijklmnopqrstuvwxyz":
        print(f"Indexation StatsF1 : {lettre.upper()}")
        driver.get(f"https://www.statsf1.com/fr/constructeurs-{lettre}.aspx")
        try:
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_CPH_Main_GV_Constructeur")))
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) < 3: continue
                link = cells[0].find_element(By.TAG_NAME, "a")
                all_links.append({
                    "nom_base": link.text.strip(),
                    "url_stats": link.get_attribute("href"),
                    "pays": cells[1].find_element(By.TAG_NAME, "img").get_attribute("alt") if cells[1].find_elements(By.TAG_NAME, "img") else "N/A",
                    "cellule_annees": cells[2].text.strip()
                })
        except: continue

    # 2. ANALYSE FILIATIONS
    print("\nAnalyse des filiations...")
    for item in all_links:
        driver.get(item['url_stats'])
        try:
            blocs = driver.find_elements(By.XPATH, "//*[contains(text(), 'Filiation :')]/..")
            if blocs:
                text_f = blocs[0].text.split("Team Principal")[0].replace("Filiation :", "").strip()
                segments = [s.strip('• ').strip() for s in text_f.split('➜') if s.strip()]
                last_uid = None
                for seg in segments:
                    nom_seg = re.search(r'^[^(\n]+', seg).group(0).strip()
                    raw_date = re.search(r'\((.*?)\)', seg).group(1).strip() if "(" in seg else item['cellule_annees']
                    ans = re.findall(r'\d{4}', raw_date)
                    ts = ans[0] if ans else "NULL"
                    te = "NULL" if "-" in raw_date and raw_date.strip().endswith("-") else (ans[1] if len(ans) > 1 else ts)
                    
                    uid = f"{nom_seg} ({raw_date})"
                    if uid not in unique_periods:
                        unique_periods[uid] = {"nom": nom_seg, "tstart": ts, "tend": te, "pays": item['pays'], "parent_uid": last_uid}
                    last_uid = uid
            else:
                raw_date = item['cellule_annees']
                ans = re.findall(r'\d{4}', raw_date)
                ts = ans[0] if ans else "NULL"
                te = "NULL" if "-" in raw_date and raw_date.strip().endswith("-") else (ans[-1] if len(ans) > 1 else ts)
                uid = f"{item['nom_base']} ({raw_date})"
                if uid not in unique_periods:
                    unique_periods[uid] = {"nom": item['nom_base'], "tstart": ts, "tend": te, "pays": item['pays'], "parent_uid": None}
        except: continue

    # 3. SCRAPING WIKIPEDIA
    print("\nScraping Wikipedia...")
    sorted_keys = sorted(unique_periods.keys(), key=lambda x: x.lower())
    uid_to_id = {key: i for i, key in enumerate(sorted_keys, 1)}
    final_data = []
    infobox_cache = {}

    for key in sorted_keys:
        row = unique_periods[key]
        nom_stats = row['nom']
        mot, pneu = "NULL", "NULL"
        page_cible = None

        if nom_stats in jj:
            valeur_jj = jj[nom_stats]
            page_cible = valeur_jj.replace(" ", "_") if valeur_jj != "NULL" else None

        if page_cible:
            if page_cible not in infobox_cache:
                
                c_mot, c_pneu = "NULL", "NULL"
                try:
                    res_i = requests.get(f"https://fr.wikipedia.org/wiki/{page_cible}", headers=headers, timeout=5)
                    if res_i.status_code == 200:
                        soup_i = BeautifulSoup(res_i.text, 'html.parser')
                        ib = soup_i.find('div', class_='infobox_v3') or soup_i.find('table', class_='infobox')
                        if ib:
                            for tr_ib in ib.find_all('tr'):
                                th = tr_ib.find('th')
                                td = tr_ib.find('td')
                                if th and td:
                                    lbl = th.get_text(strip=True).lower()
                                    val = td.get_text(" ", strip=True)
                                    if "moteur" in lbl: 
                                        
                                        raw_val = val.split()[0].replace(",", "").strip()
                                        c_mot = raw_val.split("-")[0]
                                    elif "pneu" in lbl: 
                                        c_pneu = val.split()[0].replace(",", "").strip()
                    infobox_cache[page_cible] = (c_mot, c_pneu)
                except:
                    infobox_cache[page_cible] = ("NULL", "NULL")
            
     
            mot, pneu = infobox_cache[page_cible]

        final_data.append({
            'teamID': uid_to_id[key],
            'tName': nom_stats,
            'tCountry': row['pays'],
            'tstart': row['tstart'],
            'tend': row['tend'],
            'tMotor': mot,
            'tTyres': pneu,
            'twas': uid_to_id.get(row['parent_uid'], "NULL") if row['parent_uid'] else "NULL"
        })
        

    # 4. DOC CSV
    with open('Team_complète.csv', 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['teamID', 'tName', 'tCountry', 'tstart', 'tend', 'tMotor', 'tTyres', 'twas']
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(final_data)

finally:
    driver.quit()
    print("\n Fichier généré ")