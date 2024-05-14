import os
import json
import shutil

# Pokus o importování gitpython
try:
    import git
except ImportError as ie:
    stah = input("Update client potřebuje knihovnu gitpython. Přejete si ji stáhnout? (A/n) ")
    
    if stah.lower() == "n":
        os.system("python gui.py")
    else:
        os.system("pip install gitpython")
        os.system(f"python res.py upd.py {os.getpid()} restart")

# Začátek
os.system("cls" if os.name == "nt" else "clear")
print("Update client v. 0.9\n======================\n")
print("Inicializace...")
url = "https://github.com/CreatorOfBiontium/strava"

try:
    print("[i] Měním cwd na aktuální složku")
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    print("[i] Vytváření složky 'update'")
    
    try:
        os.makedirs("update")
    except:
        try:
            os.system("rmdir /s update" if os.name == "nt" else "rm -r update")
            os.makedirs("update")
        except:
            pass
        
    print("[i] stahuji GitHub repozitář")
    repo = git.Repo.clone_from(url, "update")
    
    print("[i] Kontrola aktualizací")
    with open("update/vi/verze.txt", "r", encoding="utf-8") as verze:
        radky = verze.readlines()
        
    with open("data/verze.txt", "r", encoding="utf-8") as verzeL:
        verzeLzs = verzeL.read()
        
    if radky[-1] == verzeLzs:
        print("[i] Máte nejnovější verzi")
        
        
        print("Startuji gui.py...")
        exit()
        
    else:
        print("[i] Instaluji aktualizace...")
        print("\t> kopíruji:   gui.py   res.py   upd.py")
        
        shutil.copy2(f"update/verze/{radky[-1]}/gui.py", "gui.py")
        shutil.copy2(f"update/verze/{radky[-1]}/res.py", "res.py")
        
        try:
            shutil.copy2(f"update/verze/{radky[-1]}/upd.py", "upd.py")
        except:
            print("\033[91m" + "Soubor upd.py nelze aktualizovat, pokračuji v aktualizaci ostatních souborů..." + "\033[0m")
        
        with open("data/config.json", "r", encoding="utf-8") as configFile:
            slovnik = json.load(configFile)
            
        souborNastaveni = slovnik["all"]["settingsFile"]
        
        print(F"\t> aktualizuji:   data/config.json   {souborNastaveni}")
        
        with open(f"update/verze/{radky[-1]}/data/config.json", "r", encoding="utf-8") as configFileTc:
            ncf = json.load(configFileTc)
        
        with open("data/config.json", "r+", encoding="utf-8") as configFile:
            cf = json.load(configFile)
            
            cf.update(ncf)
            
            jsonDone = json.dumps(cf, indent=4)
            configFile.seek(0)
            configFile.write(jsonDone)
            configFile.truncate()
            

        with open(f"update/verze/{radky[-1]}/{souborNastaveni}", "r", encoding="utf-8") as configFileTc:
            ncf2 = json.load(configFileTc)
        
        with open(f"{souborNastaveni}", "r+", encoding="utf-8") as settingsFile:
            cf2 = json.load(settingsFile)
            
            cf2.update(ncf2)
            
            jsonDone = json.dumps(cf2, indent=4)
            settingsFile.seek(0)
            settingsFile.write(jsonDone)
            settingsFile.truncate()
        
        os.system("rmdir /s update" if os.name == "nt" else "rm -r update")
        
        print("[i] Aktualizace byla úspěšná!")
        os.system("cls" if os.name == "nt" else "clear")
        exit()

except Exception as excp:
    print("\033[91m" + f"Chyba: {excp}" + "\033[0m")
    
# Na konec řekne že nastala chyba, protože program neodešel kdy měl
print("[!] Nastala chyba. Program nelze aktualizovat.")
print("[i] Odstraňuji složku update")
os.system("rmdir /s update" if os.name == "nt" else "rm -r update")
input("Zavřete entrem ")
exit()