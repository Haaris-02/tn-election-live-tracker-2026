import os
import django
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By 

# MUKKIYAM: Unga django project peru
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') 
django.setup()

from core.models import Constituency

def clean_text_for_match(name):
    if not name: return ""
    name = name.lower()
    name = name.replace('(sc)', '').replace('(st)', '')
    return re.sub(r'[^a-z]', '', name)

def scrape_eci_results():
    url = "https://results.eci.gov.in/ResultAcGenMay2026/statewiseS221.htm" 
    
    edge_options = Options()
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)
    edge_options.add_argument("--ignore-certificate-errors") 
    
    try:
        print("--------------------------------------------------")
        print("🚀 Fetching Live Data (Fixing ADMK & AMMK Name Bugs)...")
        
        driver = webdriver.Edge(options=edge_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get(url)
        print("⏳ Waiting 10s for page to load...")
        time.sleep(10) 
        
        # Dropdown bypass
        try:
            driver.execute_script("""
                var select = document.querySelector('select');
                if(select) {
                    select.value = select.options[select.options.length - 1].value;
                    select.dispatchEvent(new Event('change'));
                }
            """)
            time.sleep(5) 
        except:
            pass

        all_table_rows = []
        current_page = 1 
        
        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            all_table_rows.extend(soup.find_all('tr'))
            
            next_page_num = current_page + 1
            try:
                next_page_link = driver.find_element(By.XPATH, f"//a[normalize-space()='{next_page_num}']")
                driver.execute_script("arguments[0].click();", next_page_link)
                time.sleep(3) 
                current_page = next_page_num
            except Exception as e:
                break 
        
        driver.quit() 
        
        # --- PUDHU FIX: Katchi perugalai update pannitom ---
        party_map = {
            "All India Anna Dravida Munnetra": "ADMK", # ADMK first la irukkaum!
            "Dravida Munnetra Kazhagam": "DMK",
            "Tamilaga Vettri Kazhagam": "TVK",
            "Indian National Congress": "INC",
            "Bharatiya Janata Party": "BJP",
            "Naam Tamilar Katchi": "NTK",
            "Pattali Makkal Katchi": "PMK",
            "Desiya Murpokku Dravida": "DMDK",
            "Indian Union Muslim League": "IUML",
            "Communist Party of India (Marxist)": "CPIM",
            "Communist Party of India": "CPI",
            "Viduthalai Chiruthaigal Katchi": "VCK",
            "Amma Makkal Munnetra": "AMMK" # Spelling thappa irunthalum ithu kandupudichidum
        }

        updated_count = 0
        all_db_seats = list(Constituency.objects.all())

        manual_map = {
            "drradhakrishnannagar": "rknagar",
            "chepaukthiruvallikeni": "chepauk",
            "udagamandalam": "ooty",
            "kanniyakumari": "kanyakumari"
        }

        processed_seats = set()

        for row in all_table_rows:
            cols = row.find_all('td')
            
            if len(cols) >= 9: 
                try:
                    constituency_name = cols[0].text.strip()
                    raw_party = cols[3].text.strip() 
                    status = cols[-1].text.strip() 

                    skip_words = ["Kazhagam", "Party", "Congress", "Katchi", "League"]
                    if any(word in constituency_name for word in skip_words):
                        continue 

                    cleaned_eci_name = clean_text_for_match(constituency_name)
                    
                    if cleaned_eci_name in processed_seats:
                        continue

                    leading_party = raw_party 
                    
                    # --- PUDHU FIX: Periya perai first thedu (Length Sort) ---
                    # Ippo ADMK vai first thedum, aprom thaan DMK vai thedum!
                    for full_name in sorted(party_map.keys(), key=len, reverse=True):
                        if full_name in raw_party:
                            leading_party = party_map[full_name]
                            break

                    if cleaned_eci_name in manual_map:
                        cleaned_eci_name = manual_map[cleaned_eci_name]

                    matched_c = None
                    for db_seat in all_db_seats:
                        if clean_text_for_match(db_seat.name) == cleaned_eci_name:
                            matched_c = db_seat
                            break
                    
                    if matched_c:
                        matched_c.live_leading_party = leading_party
                        matched_c.live_status = status
                        
                        if "declared" in status.lower() or "won" in status.lower():
                            matched_c.live_status = "Result Declared - Won"
                            
                        matched_c.save()
                        processed_seats.add(cleaned_eci_name)
                        updated_count += 1

                except Exception as e:
                    pass
        
        print(f"\nTotal constituencies updated: {updated_count} out of 234")
        print("--------------------------------------------------")

    except Exception as e:
        print(f"❌ Scraping Error: {e}")
        try:
            driver.quit() 
        except:
            pass

if __name__ == '__main__':
    while True:
        scrape_eci_results()
        print("Waiting 5 minutes for next update...\n")
        time.sleep(300)