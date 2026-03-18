import os
import json
import requests
from datetime import datetime

import os

if os.environ.get('GITHUB_ACTIONS'):
    chemin_fichier = "status.json"
else:
    dossier_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_fichier = os.path.join(dossier_actuel, "status.json")

print(f"--- DEBUG ---")
print(f"Le fichier sera créé ici : {chemin_fichier}")

def fetch_steam_data():
    url = "https://api.steampowered.com/ISteamApps/GetSDRConfig/v1/?appid=730"
    
    try:
        print("Connexion à Steam...")
        response = requests.get(url, timeout=10)
        data = response.json()
        
        status_summary = {
            "last_update": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "regions": {}
        }

        if "pops" in data:

            for i, (region_id, region_info) in enumerate(data["pops"].items()):
                status_summary["regions"][region_id] = "Online"
                if i >= 10: break
            

            with open(chemin_fichier, "w") as f:
                json.dump(status_summary, f, indent=4)
            
            print("SUCCÈS : Le fichier status.json est apparu !")
        else:
            print("ERREUR : 'pops' non trouvé dans le JSON de Steam.")

    except Exception as e:
        print(f"ERREUR TECHNIQUE : {e}")

fetch_steam_data()
