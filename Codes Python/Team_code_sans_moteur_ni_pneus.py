import csv
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)

unique_periods = {}
all_links = []

try:
   
    for lettre in "abcdefghijklmnopqrstuvwxyz":
        print(f"Indexation StatsF1 : {lettre.upper()}")
        driver.get(f"https://www.statsf1.com/fr/constructeurs-{lettre}.aspx")
        try:
            table = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "ctl00_CPH_Main_GV_Constructeur")))
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
                    nom_match = re.search(r'^[^(\n]+', seg)
                    nom_seg = nom_match.group(0).strip() if nom_match else "Inconnu"
                    
                    raw_date = re.search(r'\((.*?)\)', seg).group(1).strip() if "(" in seg else item['cellule_annees']
                    ans = re.findall(r'\d{4}', raw_date)
                    ts = ans[0] if ans else "NULL"
                    te = "NULL" if "-" in raw_date and raw_date.strip().endswith("-") else (ans[-1] if len(ans) > 0 else ts)
                    
                    uid = f"{nom_seg} ({raw_date})"
                    if uid not in unique_periods:
                        unique_periods[uid] = {"nom": nom_seg, "tstart": ts, "tend": te, "pays": item['pays'], "parent_uid": last_uid}
                    last_uid = uid
            else:
                raw_date = item['cellule_annees']
                ans = re.findall(r'\d{4}', raw_date)
                ts = ans[0] if ans else "NULL"
                te = "NULL" if "-" in raw_date and raw_date.strip().endswith("-") else (ans[-1] if len(ans) > 0 else ts)
                uid = f"{item['nom_base']} ({raw_date})"
                if uid not in unique_periods:
                    unique_periods[uid] = {"nom": item['nom_base'], "tstart": ts, "tend": te, "pays": item['pays'], "parent_uid": None}
        except: continue

  
    sorted_keys = sorted(unique_periods.keys(), key=lambda x: x.lower())
    uid_to_id = {key: i for i, key in enumerate(sorted_keys, 1)}
    final_data = []
    
    for key in sorted_keys:
        row = unique_periods[key]
        final_data.append({
            'teamID': uid_to_id[key],
            'tName': row['nom'],
            'tCountry': row['pays'],
            'tstart': row['tstart'],
            'tend': row['tend'],
            'twas': uid_to_id.get(row['parent_uid'], "NULL") if row['parent_uid'] else "NULL"
        })

    
    with open('Team_sans_moteur_ni_pneus.csv', 'w', newline='', encoding='utf-8-sig') as f:
       
        fieldnames = ['teamID', 'tName', 'tCountry', 'tstart', 'tend', 'twas']
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(final_data)

finally:
    driver.quit()
    print(f"\nTerminé ! Fichier généré avec {len(final_data)} lignes.")