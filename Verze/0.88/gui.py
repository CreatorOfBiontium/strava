try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter.font import Font
    import tkinter.messagebox as messagebox
    import datetime
    import os
    import threading
    import time
    import json
except ImportError as ie:
    with open("data/debug.txt", "a", encoding="utf-8") as debugFile:
        debugFile.write(f"\nError6: Could not import library - {ie} [{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]")

try:
    from cryptography.fernet import Fernet
except:
    with open("data/debug.txt", "a", encoding="utf-8") as debugFile:
        debugFile.write(f"\nError6: Could not import cryptography.fernet [{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]")

try:
    import requests
except:
    with open("data/debug.txt", "a", encoding="utf-8") as debugFile:
        debugFile.write(f"\nError6: Could not import requests [{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]")

#TODO: runCheck a kontrola při uložení nastavení

#cislo; A -> Alfa; a -> verze a; + -> nedokončená verze, rozšíření napsané verze, ale nedokončené; může být i třeba: 1.0Ba+
VERSION = "0.88"

#souobry potřebné (pak načtené z configu)
settingsFile = None
currentDataFile = None
config = {}
vlakno1bezi = False
vlakno2bezi = False
vlakno3bezi = True
vlakno4bezi = False
vlakno5bezi = False
after_loop1 = True
after_loop2 = True
waited = 0

#temp
restart_gui = False
brk_end_loop = False

problems = []
codeRunning = "ne"
threads = ["3"]
nesxtOrder = "--:--:--"

exit_event = threading.Event()

# Nastavení cwd na tuto složku - potřeba pro VS Code a asi i některé linux/unixy, protože to SAMI NEUDĚLŮAJÍ (udělají nebo nevím, jen přístup k souborům nefunguje)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

#inicializace z config.json
try:
    with open("data/config.json", "r", encoding="utf-8") as confSoubor:
        config = json.load(confSoubor)
        settingsFile = config["all"]["settingsFile"]
        currentDataFile = config["all"]["currentDataFile"]
        debugTF = config["all"]["debug"]
        showErrors = config["all"]["showErrors"]
        ShutOnClose = config["all"]["ShutOnClose"]
        bgc = config["all"]["bg"]
        threadsjson = config["all"]["threads"]
        allowRM = config["all"]["allowRM"]
        showErrorOnDebug = config["all"]["showErrorOnDebug"]
        
    with open("data/config.json", "r", encoding="utf-8") as confSoubor:
        config = json.load(confSoubor)
        
        setup = config["data"]["setup"]
        allOrders = config["data"]["allOrders"]
        lastOrder = config["data"]["lastOrder"]
        shutDownProperly = config["data"]["shutDownProperly"]
        showMode4Alert = config["data"]["showMode4Alert"]
        runCheck = config["data"]["runCheck"]
        showMode4Alert = config["data"]["showMode4Alert"]
        
except Exception as excp:
        with open("data/debug.txt", "a") as debugFile:
                debugFile.write(f"\nError1: Could not load config.json Exception {excp} [{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]")
        if "e1" not in problems:
            problems.append("e1")

#Tu bude základní inicializace z nastavení, jen část nastavení, zbytek si už bude brát kód sám později
try:
    with open(settingsFile, "r") as confSoubor:
        settings = json.load(confSoubor)
        updateOrderForIdk = settings["mainSettings"]["orderUpdateInterval"]
        infoUpdateInterval = settings["mainSettings"]["infoUpdateInterval"]
        useGPT = settings["mainSettings"]["useGPT"]
        ifNoGPT = settings["mainSettings"]["ifNoGPT"]

        
except Exception as excp:
        with open("data/debug.txt", "a") as debugFile:
                debugFile.write(f"\nError1: Could not load settings file Exception {excp} [{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]")
        if "e1" not in problems:
            problems.append("e1")

def exitPgTop(exitt):
    global vlakno1bezi, exit_event, thread1, vlakno2bezi, vlakno3bezi, vlakno4bezi, vlakno5bezi, problems, codeRunning
    
    vlakno1bezi = False
    vlakno2bezi = False
    vlakno3bezi = False
    vlakno4bezi = False
    vlakno5bezi = False
    problems = []
    codeRunning = "ne"
    
    with open(currentDataFile, "w") as currFile:
        currFile.write(f"problems: lastPRproblems: {' '.join(problems)}\nlastOrder: lastPRlastOrder: {lastOrder}\ncodeRunning: ne\nthreads: \nallOrders: \nnextOrderUpdate: 0")
        
    with open("data/config.json", "r+") as configFile:
        jsonData = json.load(configFile)
        jsonData["data"]["shutDownProperly"] = True
        jsonDone = json.dumps(jsonData, indent=4)
        configFile.seek(0)
        configFile.write(jsonDone)
        configFile.truncate()
    
    if exitt:
        exit()
    
#Start (zapsání do currentdataFile a další)
#List: problems-lastPRproblems:, runCheck

with open(currentDataFile, "w") as currFile:
    currFile.write(f"problems: \nlastOrder: \ncodeRunning: ano\nthreads: 3\nallOrders: \nnextOrderUpdate: 0")
    
# Vím, že jsem mohl to dát do třídy a bylo by to tak mnohem lepší, ale idk, takto sa to dá
if setup == True:
    root = tk.Tk()
    root.geometry("400x300")
    root.title("Setup")
    root.minsize(320, 300)
    root.maxsize(420, 400)
    
    lbl = tk.Label(root, text="Vítej! Zde začínají tvé první kroky. Pojďme si vše nastavit. (Jestli chcete vypnout setup, vypňete setup mód v data/config.json)\n", wraplength=320)
    lbl.pack()
    
    def cont():
        info = {}
        
        def cont2(encr, jmeno, heslo):
            # Uložení info do info
            info["uzivatel"] = jmeno
            info["pwd"] = heslo
            info["encryptPwd"] = encr
            
            for widget in root.winfo_children():
                if widget.winfo_class() != 'Menu':
                    widget.destroy()
                    
            gptlbl = tk.Label(root, text="Přejete si použít Chat GPT?\nChat GPT dokáže objednat oběd podle toho, co právy vy máte rádi. Nastavování je mírně složitější, proto tuto možnost doporučuji pouze pro ty co těmto věcem rozumí. Níže bude tutoriál jak na to.\n\n1. Přejděte na platform.openai.com/api-keys a vygenerujte si váš API klíč\n2. Začněte novou konverzaci, pozdravte a zkopírujte si id konverzace (.../u/idKonverzace)\n3. Informace vložte na příští stránce, GPT ještě nemá podporu, ale brzo by mohla přijít\n\nZatím jsem se k podpoře Chat GPT moc nedostal, ale pak ano, možná to celé předělám, takže info ani vyplňovat nemusíte, ale API klíč se hodit bude pořád.", wraplength=320)
            gptlbl.pack()
            
            def cont3():
                for widget in root.winfo_children():
                    if widget.winfo_class() != 'Menu':
                        widget.destroy()


                gptlbl2 = tk.Label(root, text="Níže zadejte vaše údaje. Po zadání by se mělo zobrazit tlačítko 'pokračovat'. Údaje vám v poli nezůstanou pokud přejdete zpět.\n\n", wraplength=320)
                gptlbl2.pack()
                        
                api_label = tk.Label(root, text="Api:")   
                api_label.pack(padx=(0, 10))
                api_entry = tk.Entry(root, show="*")
                api_entry.pack()

                cid_label = tk.Label(root, text="Id konverzace:")  
                cid_label.pack(padx=(0, 10))
                cid_entry = tk.Entry(root)
                cid_entry.pack()
                
                n_label = tk.Label(root, text="\n")
                n_label.pack()

                ct4_button = tk.Button(root, text="Přeskočit", command=lambda: cont4(True))
                ct4_button.pack()
                back2_button = tk.Button(root, text="Zpět", command=lambda: cont2(info["encryptPwd"], info["uzivatel"], info["pwd"]))
                back2_button.pack()
                
                def on_change():
                    print("a", api_entry.get(), cid_entry.get())
                    if api_entry.get() == "" and cid_entry.get() == "":
                        ct4_button.config(text="Přeskočit")
                        ct4_button.config(command=lambda: cont4(True))
                    else:
                        ct4_button.config(text="Pokračovat")
                        ct4_button.config(command=lambda: cont4(False))
                        
                cid_entry.bind("<<Modified>>", on_change)
                api_entry.bind("<<Modified>>", on_change)
                
                
                def cont4c():
                    for widget in root.winfo_children():
                        if widget.winfo_class() != 'Menu':
                            widget.destroy()

                    gptlbl = tk.Label(root, text="Na tomto stále pracujeme. Chat GPT stále namá podporu.", wraplength=320)
                    gptlbl.pack()
                    back3_button = tk.Button(root, text="Zpět", command=lambda: cont3())
                    back3_button.pack()
                        
                def cont4(skip):
                    def finish():
                        for widget in root.winfo_children():
                            if widget.winfo_class() != 'Menu':
                                widget.destroy()
                            
                        finito = tk.Label(root, text="\nPočkejte chvíli než vše dokončíme...", wraplength=320, font=("Arial", 12, "bold"))
                        finito.pack(pady=(0, 80))
                        
                        
                        # Zapisování
                        with open(settingsFile, "r+", encoding="utf-8") as settFile:
                            jsonData = json.load(settFile)
                            jsonData["mainSettings"]["uzivatel"] = info["uzivatel"]
                            jsonData["mainSettings"]["encryptPwd"] = info["encryptPwd"]

                            if info["encryptPwd"] == True:
                                keyy = Fernet.generate_key()

                                pwdd = Fernet(keyy).encrypt(info["pwd"].encode()).decode()
                                jsonData["mainSettings"]["pwd"] = pwdd

                                jsonData["mainSettings"]["key"] = keyy.decode()

                            else:
                                jsonData["mainSettings"]["pwd"] = info["pwd"]


                            jsonData["mainSettings"]["loginEveryDays"] = 5
                            jsonData["mainSettings"]["orderUpdateInterval"] = 21600
                            jsonData["mainSettings"]["useGPT"] = False
                            jsonData["mainSettings"]["ifNoGPT"] = 2
                            jsonData["mainSettings"]["infoUpdateInterval"] = 1

                            jsonDone = json.dumps(jsonData, indent=4)
                            settFile.seek(0)
                            settFile.write(jsonDone)
                            settFile.truncate()
                            
                            
                        with open("data/config.json", "r+", encoding="utf-8") as settFile:
                            jsonData = json.load(settFile)
                            jsonData["data"]["setup"] = False

                            jsonDone = json.dumps(jsonData, indent=4)
                            settFile.seek(0)
                            settFile.write(jsonDone)
                            settFile.truncate()
                            
                            
                        finito.config(text="Vše hotovo!")
                        os.system(f"python res.py gui.py {os.getpid()} restart")


                    for widget in root.winfo_children():
                        if widget.winfo_class() != 'Menu':
                            widget.destroy()
                            
                    if skip == True:
                        fin = tk.Label(root, text="Prozatím vše hotovo! Vše potřené si jde nastavit v nastavení aplikce.\nDěkuji za spolupráci.\n\n", wraplength=320)
                        fin.pack()
                        back3_button = tk.Button(root, text="Dokončit", command=finish)
                        back3_button.pack()
                        back4_button = tk.Button(root, text="Zpět", command=lambda: cont3())
                        back4_button.pack()
                    else:
                        cont4c()


            ct3_button = tk.Button(root, text="Pokračovat", command=cont3)
            ct3_button.pack()
            back2_button = tk.Button(root, text="Zpět", command=cont)
            back2_button.pack()
        
        
        for widget in root.winfo_children():
            if widget.winfo_class() != 'Menu':
                widget.destroy()
                
        
        lbl = tk.Label(root, text="Začňeme zadáním tvých přihlašovacích údajů na stravu.\n", wraplength=320)
        lbl.pack()

        # Jméno (entry)
        name_label = tk.Label(root, text="Jméno:")
        name_label.pack(padx=(0, 10))
        name_entry = tk.Entry(root)
        name_entry.pack()

        # Heslo (entry)
        password_label = tk.Label(root, text="Heslo:")
        password_label.pack(padx=(0, 10))
        password_entry = tk.Entry(root, show="*")
        password_entry.pack()

        # Encryptovat heslo do souboru (Dropdown ano/ne)
        encrypt_label = tk.Label(root, text="Encryptovat heslo do souboru:")
        encrypt_label.pack(padx=(0, 10))
        encrypt_options = ["Ano", "ne"]

        encrypt_dropdown_var = tk.StringVar(value=encrypt_options[1])

        encrypt_dropdown = tk.OptionMenu(root, encrypt_dropdown_var, *encrypt_options)
        encrypt_dropdown.pack()
        
        lbl = tk.Label(root, text="\n Tento kód používá údaje pouze k objednávání objedů, jestli se vám to ale i tak nezdá, můžete heslo do souboru encryptovat a zaručit tím větší bezpečí, protože venkovní aplikace to budou mít težší zjistit.\n", wraplength=320)
        lbl.pack()
        
        
        lg_button = tk.Button(root, text="Pokračovat", command=lambda: cont2(encrypt_dropdown_var.get(), name_entry.get(), password_entry.get()))
        lg_button.pack()
        
    def back():
        for widget in root.winfo_children():
            if widget.winfo_class() != 'Menu':
                widget.destroy()
                
        sbv = tk.Label(root, text="Setup bude zanedlouho vypnut a při příštím zapnutí budete přesměrování do hlavního okna.", wraplength=320)
        sbv.pack()
    
        with open("data/config.json", "r+") as configFile:
            jsonData = json.load(configFile)
            jsonData["data"]["setup"] = False
            jsonDone = json.dumps(jsonData, indent=4)
            configFile.seek(0)
            configFile.write(jsonDone)
            configFile.truncate()
            
        os.system(f"python res.py gui.py {os.getpid()} restart")
    
    
    lg_button = tk.Button(root, text="Jdeme do toho!", command=cont)
    lg_button.pack()
    
    backkk_button = tk.Button(root, text="Odejít a vypnout setup", command=back)
    backkk_button.pack()
    
    root.mainloop()
    exit()

if shutDownProperly != True:
    messagebox.showwarning("Program nebyl vypnut dobře", "Program nebyl vypnut jak měl být, je možné že jste přišli o nějaká data. Program bude restartován.")
    exitPgTop(False)
    os.system(f"python res.py gui.py {os.getpid()} pshdwn")

def writeToDebug(data):
        global showErrors
        
        if debugTF != False:
            with open("data/debug.txt", "a") as debugFile:
                debugFile.write(f"\n{data} [{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]")
            if showErrorOnDebug:
                messagebox.showinfo("Error", f"\nNastala chyba [{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}] (Error: {data})")
        else:
            try:
                if showErrors:
                    messagebox.showinfo("Error", f"\nTried writing to debug.txt while debug = False [{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}] (Error: {data})")
            except:
                pass

def runCheckFunc():
    print("runCheck ještě není podporováno, ale brzo bude")

if runCheck:
    runCheckFunc()

def changeToPrehled():
    global label, after_loop1, casDoNextOrder, restartV1, stav, casDoNextUpdate, beziciVlakna, problemy, celkemObjednavek, posledniObjednavka

    custom_font = Font(family="Arial", size=35, weight="bold")
    
    aktualizacePrvku = 10000
    casDoNextOrder = 0
    casDoNextUpdate = "--:--:--"
    stav = ""
    posledniObjednavka = ""
    problemy = ""
    celkemObjednavek = 0
    beziciVlakna = ""
    
    after_loop1 = True

    try:
        with open(settingsFile, "r", encoding="utf-8") as soubor:
            aktualizacePrvku = int(json.load(soubor)["mainSettings"]["infoUpdateInterval"]) * 1000
        with open(settingsFile, "r", encoding="utf-8") as soubor:
            casDoNextOrder = int(json.load(soubor)["mainSettings"]["orderUpdateInterval"])
    except Exception as excp:
        writeToDebug(f"Error3: Could not get infoUpdateInterval from from {settingsFile} while updating window. Exception: {excp}")
        if "e3/1" not in problems:
            problems.append("e3/1")
        
        
    def updateLabelsPrehled():
        global label, casDoNextOrder, label0, label1, label2, label3, label4, label5, restartV1
        
        if after_loop1:
            try:
                #loadne data z currentData.txt
                with open(currentDataFile, "r", encoding="utf-8") as curDfile:
                    obsah = curDfile.read()

                radky = obsah.split("\n")
                for radek in radky:
                    if radek.startswith("problems: "):
                        problemy = radek.replace("problems: ", "")
                    elif radek.startswith("lastOrder: "):
                        posledniObjednavka = radek.replace("lastOrder: ", "")
                    elif radek.startswith("codeRunning: "):
                        stav = radek.replace("codeRunning: ", "")
                    elif radek.startswith("threads: "):
                        beziciVlakna = radek.replace("threads: ", "")
                    elif radek.startswith("allOrders: "):
                        celkemObjednavek = radek.replace("allOrders: ", "")
                    elif radek.startswith("nextOrderUpdate: "):
                        casDoNextUpdate = int(radek.replace("nextOrderUpdate: ", ""))

                        casDoNextUpdate = casDoNextOrder - casDoNextUpdate

                        hodiny = casDoNextUpdate // 3600
                        zbyle_sekundy = casDoNextUpdate % 3600
                        minuty = zbyle_sekundy // 60
                        sekundy = zbyle_sekundy % 60


                        casDoNextUpdate = f"{hodiny}:{minuty:02}:{sekundy:02}"


                for widget in root.winfo_children():
                    if widget.winfo_class() != 'Menu':
                        widget.destroy()

                label = tk.Label(root, text=f"{casDoNextUpdate}", font=custom_font, anchor="center", justify="center")
                label.configure(background=bgc)
                label.pack()
                

                label0 = tk.Label(root, text="", font=custom_font)
                label0.configure(background=bgc)
                label0.pack()

                label1 = tk.Label(root, text=f"Hlavní smyčka kódu běží: {stav}")
                label1.configure(background=bgc)
                label1.pack()

                label2 = tk.Label(root, text=f"Poslední obědnávka: {posledniObjednavka}", wraplength=320)
                label2.configure(background=bgc)
                label2.pack()

                label4 = tk.Label(root, text=f"Celkem objednávek: {celkemObjednavek}")
                label4.configure(background=bgc)
                label4.pack()        

                label3 = tk.Label(root, text=f"Problémy: {problemy}")
                label3.configure(background=bgc)
                label3.pack()

                label5 = tk.Label(root, text=f"Běžící vlákna: {beziciVlakna}")
                label5.configure(background=bgc)
                label5.pack()

                label.bind("<Button-1>", restartV1)

                if "e5" in problems:
                    problems.remove("e5")

            except Exception as excp:
                if excp != "name 'restartV1' is not defined":
                    writeToDebug(f"Error5: Error occurred while loading Přehled. Exception: {excp}")
                    if "e5" not in problems:
                        problems.append("e5")
                    
    updateLabelsPrehled()
    
    def update():
        global label, casDoNextOrder, label0, label1, label2, label3, label4, label5
        
        if after_loop1:
            try:
                #loadne data z currentData.txt
                with open(currentDataFile, "r", encoding="utf-8") as curDfile:
                    obsah = curDfile.read()

                radky = obsah.split("\n")
                for radek in radky:
                    if radek.startswith("problems: "):
                        problemy = radek.replace("problems: ", "")
                    elif radek.startswith("lastOrder: "):
                        posledniObjednavka = radek.replace("lastOrder: ", "")
                    elif radek.startswith("codeRunning: "):
                        stav = radek.replace("codeRunning: ", "")
                    elif radek.startswith("threads: "):
                        beziciVlakna = radek.replace("threads: ", "")
                    elif radek.startswith("allOrders: "):
                        celkemObjednavek = radek.replace("allOrders: ", "")
                    elif radek.startswith("nextOrderUpdate: "):
                        casDoNextUpdate = int(radek.replace("nextOrderUpdate: ", ""))

                        casDoNextUpdate = casDoNextOrder - casDoNextUpdate

                        hodiny = casDoNextUpdate // 3600
                        zbyle_sekundy = casDoNextUpdate % 3600
                        minuty = zbyle_sekundy // 60
                        sekundy = zbyle_sekundy % 60

                        casDoNextUpdate = f"{hodiny}:{minuty:02}:{sekundy:02}"

                label.configure(text=casDoNextUpdate)

                label1.configure(text=f"Hlavní smyčka kódu běží: {stav}")

                label2.configure(text=f"Poslední obědnávka: {posledniObjednavka}")

                label4.configure(text=f"Celkem objednávek: {celkemObjednavek}")  

                label3.configure(text=f"Problémy: {problemy}")

                label5.configure(text=f"Běžící vlákna: {beziciVlakna}")

                if after_loop1:
                    root.after(aktualizacePrvku, update)

                if "e5" in problems:
                    problems.remove("e5")

            except Exception as excp:
                writeToDebug(f"Error5: Error occurred while updating Přehled. Exception: {excp}")
                if "e5" not in problems:
                    problems.append("e5")
                
    update()


def changeToCgpt():
    global after_loop1, bgc
    
    after_loop1 = False

    
    # Zavření aktuálního okna
    for widget in root.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def save_settings():
        global favfav, nfavnfav, api, cid, favs, nfavs, trained
        
        try:
            with open(settingsFile, "r+") as settingsFileIDK:
                settinsPref = json.load(settingsFileIDK)

                favfav = settinsPref["GPTSetings"]["fav-fav"]
                nfavnfav = settinsPref["GPTSetings"]["nfav-nfav"]
                api = settinsPref["GPTSetings"]["apiKey"]
                cid = settinsPref["GPTSetings"]["chatId"]
                trained = settinsPref["GPTSetings"]["trained"]
                trainFile = settinsPref["GPTSetings"]["trainFile"]
                
                jsonDone = json.dumps(settinsPref, indent=4)
                settingsFileIDK.seek(0)
                settingsFileIDK.write(jsonDone)
                settingsFileIDK.truncate()
            
            with open(trainFile, "r+", encoding="utf-8") as trainFilee:
                obsah = trainFilee.read()
                casti = obsah.split("\n\n")
                zacatek = casti[0]

                rad = "mám rád:\n- " + favs_entry.get().replace(", ", "\n- ")
                nerad = "nemám rád:\n- " + nfavs_entry.get().replace(", ", "\n- ")
                favfav = favfav_dropdown_var.get()
                nfavnfav = nfavnfav_dropdown_var.get()
                vybirej = f"Pokud:\noblíbené-oblíbené: vybírej {favfav}\nneoblíbené-neoblíbené: vybírej {nfavnfav}"
                konec = casti[4]
                

                trainFilee.seek(0)
                trainFilee.write(f"{zacatek}\n\n{rad}\n\n{nerad}\n\n{vybirej}\n\n{konec}")
                trainFilee.truncate()


        except Exception as excp:
            writeToDebug(f"Error8/2: Error while saving settings (GPT): {excp}")
        
    def startSettings():
        global favfav, nfavnfav, api, cid, favs, nfavs, trained, trainFile
        
        try:
            with open(settingsFile, "r", encoding="utf-8") as settingsFileIDK:
                settinsPref = json.load(settingsFileIDK)

                favfav = settinsPref["GPTSetings"]["fav-fav"]
                nfavnfav = settinsPref["GPTSetings"]["nfav-nfav"]
                api = settinsPref["GPTSetings"]["apiKey"]
                cid = settinsPref["GPTSetings"]["chatId"]
                trained = settinsPref["GPTSetings"]["trained"]
                trainFile = settinsPref["GPTSetings"]["trainFile"]
            
            with open(trainFile, "r", encoding="utf-8") as trainFilee:
                obsah = trainFilee.read()
                casti = obsah.split("\n\n")
                zacatek = casti[0]
                rad = casti[1]
                nerad = casti[2]
                vybirej = casti[3]
                konec = casti[4]
                
                favs = rad.replace("mám rád:", "").replace("\n- ", ", ").replace(", ", "", 1).replace("\n", "")
                nfavs = nerad.replace("nemám rád:", "").replace("\n- ", ", ").replace(", ", "", 1).replace("\n", "")
                choose = vybirej.split("\n")[1].replace("oblíbené-oblíbené: vybírej ", "") + "-" + vybirej.split("\n")[2].replace("neoblíbené-neoblíbené: vybírej ", "")
                
                

        except Exception as excp:
            writeToDebug(f"Error occurred while loading settings from {settingsFile} while startSettings (GPT). Exception: {excp}")
                
        if trained != True:
            messagebox.showwarning("GPT neví co má dělat", "Chat GPT nebylo vytrénováno pomocí tohoto kódu, doporučujeme abyste kliknuli na tlačítko vytrénovat a dále pokračovali.")
                
                
    def train():
        global trainFile
        
        def openn():
            def save_file(obsah):
                with open(trainFile, "w", encoding="utf-8") as trainFilee:
                    trainFilee.write(obsah)
            
            def loadTE():
                editor_window = tk.Toplevel(root)
                editor_window.title(f"Úprava {trainFile}")

                editor_window.bind("<Control-s>", lambda event: save_file(text_editor.get("1.0", "end-1c")))

                # Vytvoření nového textového pole
                text_editor = tk.Text(editor_window, wrap="word", height=20, width=80)
                text_editor.pack(pady=10, fill=tk.BOTH, expand=True)

                # Tlačítko pro uložení
                button_save = ttk.Button(editor_window, text="Uložit", command=lambda: save_file(text_editor.get("1.0", "end-1c")))
                button_save.pack(side=tk.LEFT, padx=5)

                with open(trainFile, "r", encoding="utf-8") as trainFilee:
                    obsah = trainFilee.read()

                text_editor.delete("1.0", tk.END)  # Smazat stávající obsah editoru
                text_editor.insert(tk.END, obsah)  # Vložit obsah souboru do editoru
                
            loadTE()
        
        def train():
            messagebox.showwarning("Funkce není podporována", "Funkce ještě není dostupná.")
        
        toplevel_train = tk.Toplevel()
        toplevel_train.title("Vytrénovat")
        toplevel_train.geometry("200x120")
        
        not_label = tk.Label(toplevel_train, text="")
        not_label.pack()
        
        open_button = tk.Button(toplevel_train, text=f"Otevřít {trainFile}", command=openn)
        open_button.pack()
        
        train_button = tk.Button(toplevel_train, text="Trénovat", command=train)
        train_button.pack()
        
        train_label = tk.Label(toplevel_train, text="\nVše je připraveno pro trénink")
        train_label.pack()
        

    def cancel():
        global favfav, favfav_dropdown_var, nfavnfav, nfavnfav_dropdown_var
        
        startSettings()
        
        api_entry.delete(0, tk.END)
        api_entry.insert(0, api)  # Základní hodnota
        
        cid_entry.delete(0, tk.END)
        cid_entry.insert(0, cid)
        
        favs_entry.delete(0, tk.END)
        favs_entry.insert(0, favs)
        
        nfavs_entry.delete(0, tk.END)
        nfavs_entry.insert(0, nfavs)
        
        if favfav == 1:
            favfav_dropdown_var = tk.StringVar(value=favfav_options[0])
        else:
            favfav_dropdown_var = tk.StringVar(value=favfav_options[1])
            
        if nfavnfav == 1:
            nfavnfav_dropdown_var = tk.StringVar(value=nfavnfavoptions[0])
        else:
            nfavnfav_dropdown_var = tk.StringVar(value=nfavnfavoptions[1])
        
    startSettings()

    # Vytvoření skrolovatelného frame
    canvas = tk.Canvas(root, borderwidth=0, background=bgc, highlightthickness=0)
    frame = tk.Frame(canvas, background=bgc)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    def on_focus_out(event):
        root.focus_set()
        
    frame.bind('<Button-1>', on_focus_out)

    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="top", fill="both", expand=True)
    canvas.create_window((4, 4), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
    frame.bind("<Enter>", lambda event: root.bind_all("<MouseWheel>", on_mousewheel))
    frame.bind("<Leave>", lambda event: root.unbind_all("<MouseWheel>"))

    bgc = "white"

    api_label = tk.Label(frame, text="Api:")
    api_label.configure(bg=bgc)    
    api_label.pack(padx=(0, 10))
    api_entry = tk.Entry(frame, show="*")
    api_entry.pack()
    api_entry.delete(0, tk.END)
    api_entry.insert(0, api)  # Základní hodnota

    cid_label = tk.Label(frame, text="Id konverzace:")
    cid_label.configure(bg=bgc)    
    cid_label.pack(padx=(0, 10))
    cid_entry = tk.Entry(frame)
    cid_entry.pack()
    cid_entry.delete(0, tk.END)
    cid_entry.insert(0, cid)  # Základní hodnota

    favfav_label = tk.Label(frame, text="\n\nOblíbené-oblíbené jídlo:")
    favfav_label.configure(bg=bgc)
    favfav_label.pack(padx=(0, 10))
    favfav_options = [1, 2]
    
    favfav_dropdown_var = tk.StringVar()
    
    if favfav == 1:
        favfav_dropdown_var = tk.StringVar(value=favfav_options[0])
    else:
        favfav_dropdown_var = tk.StringVar(value=favfav_options[1])
        
    favfav_dropdown = tk.OptionMenu(frame, favfav_dropdown_var, *favfav_options)
    favfav_dropdown.pack()

    nfavnfavlabel = tk.Label(frame, text="Neoblíbené-neoblíbené jídlo:")
    nfavnfavlabel.configure(bg=bgc)
    nfavnfavlabel.pack(padx=(0, 10))
    nfavnfavoptions = [1, 2]
    
    nfavnfav_dropdown_var = tk.StringVar()
    
    if nfavnfav == 1:
        nfavnfav_dropdown_var = tk.StringVar(value=nfavnfavoptions[0])
    else:
        nfavnfav_dropdown_var = tk.StringVar(value=nfavnfavoptions[1])
    
    nfavnfav_dropdown = tk.OptionMenu(frame, nfavnfav_dropdown_var, *nfavnfavoptions)
    nfavnfav_dropdown.pack()

    favs_label = tk.Label(frame, text="\n\nMám rád jídla:")
    favs_label.configure(bg=bgc)
    favs_label.pack(padx=(0, 10))
    favs_entry = tk.Entry(frame)
    favs_entry.pack()
    favs_entry.delete(0, tk.END)
    favs_entry.insert(0, favs)  # Základní hodnota

    # Soubor nastavení (entry)
    nfavs_label = tk.Label(frame, text="Nemám rád jídla:")
    nfavs_label.configure(bg=bgc)
    nfavs_label.pack(padx=(0, 10))
    nfavs_entry = tk.Entry(frame)
    nfavs_entry.pack()
    nfavs_entry.delete(0, tk.END)
    nfavs_entry.insert(0, nfavs)  # Základní hodnota
    
    n_label = tk.Label(frame, text="\n")
    n_label.configure(bg=bgc)
    n_label.pack(padx=(0, 10))
    
    i_label = tk.Label(frame, text="*GPT si vytrénujte podle potřeby, ale klidně můžete použít můj built-in kód. Více info v info.md. (pokud chcete vypnou toto oznámení, nastavte trained na True v souboru nastavení)\n", wraplength=310)
    i_label.configure(bg=bgc)
    i_label.pack(padx=(0, 10))


    # Tlačítka Zrušit a Uložit (tlačítko - oboje budou zarovnaná napravo)
    save_button = tk.Button(frame, text="Vytrénovat", command=train)
    save_button.pack(side="left", pady=5, padx=5)
    
    save_button = tk.Button(frame, text="Uložit", command=save_settings)
    save_button.pack(side="right", pady=5, padx=5)
    
    cancel_button = tk.Button(frame, text="Zrušit", command=cancel)
    cancel_button.pack(side="right", pady=5, padx=5)


def changeToNastaveni():
    global after_loop1, bgc, infoUpdateInterval, updateOrderForIdk, settingsFile, useGPT, ifNoGPT, aktualizacePrvku
    
    after_loop1 = False
    
    # Zavření aktuálního okna
    for widget in root.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()


    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def save_settings():
        global checkOnSave, infoUpdateInterval, updateOrderForIdk, settingsFile, useGPT, ifNoGPT, aktualizacePrvku
        
        odpovedd = messagebox.askyesno("Uložení nastavení", "Chcete uložené změny uprlatnit už teď? (Může přijít ke problémům v kódu - změny se uloží do konfiguračního souboru nastavení, ale při přijmutí se změny nastaví v běžícím kódu, při chybě můžete restartovat potřebná vlákna)")
        
        try:
            # Funkce pro uložení nastavení
            name_value = name_entry.get()
            password_value = password_entry.get()
            
            encrypt_value = encrypt_dropdown_var.get()
            encrypt_value1 = encrypt_value
            
            if encrypt_value == "Ano":
                encrypt_value1 = True
            elif encrypt_value == "ne":
                encrypt_value1 = False
            else:
                writeToDebug(f"Error9/1: encrypt_value is not set to 'Ano' or 'ne'")
            
            login_days_value = login_days_entry.get()
            check_every_value = check_every_entry.get()
            
            # Vytvoříme druhou kopii kvůli kódu později
            use_gpt_value = use_gpt_dropdown_var.get()
            use_gpt_value1 = use_gpt_value
            
            if use_gpt_value == "Ano":
                use_gpt_value1 = True
            elif use_gpt_value == "ne":
                use_gpt_value1 = False
            else:
                writeToDebug(f"Error9/2: use_gpt_value is not set to 'Ano' or 'ne'")
            
            lunch_option_value = lunch_option_dropdown_var.get()
            update_interval_value = update_interval_entry.get()
            settings_file_value = settings_file_entry.get()

            if checkOnSave:
                print("Kontrola nastavení ještě není podporována, ale brzo bude!")
                # Tady to zkontroluje: přihlašování údaje ok/ne, klíč a kódování a jestli soubor nastavení je ok.
                chybaset = "Žádná chyba!"
                canContinue = True
                
            if canContinue:
                if encrypt_value1 != True:
                        odpoved = messagebox.askyesno("Upozornění", "Upozornění, heslo není enkryptované a je vystaveno vetšímu riziku, chcete takto pokrečovat? (ne = encryptování)")
                        if odpoved == False:
                            encrypt_value1 = True
                            encrypt_dropdown_var.set(encrypt_options[0])
                            
                
                with open(settingsFile, "r+", encoding="utf-8") as settFile:
                    jsonData = json.load(settFile)
                    jsonData["mainSettings"]["uzivatel"] = name_value
                    jsonData["mainSettings"]["encryptPwd"] = encrypt_value1

                    if encrypt_value1 == True:
                        keyy = Fernet.generate_key()

                        pwdd = Fernet(keyy).encrypt(password_value.encode()).decode()
                        jsonData["mainSettings"]["pwd"] = pwdd

                        jsonData["mainSettings"]["key"] = keyy.decode()

                    else:
                        jsonData["mainSettings"]["pwd"] = password_value


                    jsonData["mainSettings"]["loginEveryDays"] = int(login_days_value)
                    jsonData["mainSettings"]["orderUpdateInterval"] = int(check_every_value)
                    jsonData["mainSettings"]["useGPT"] = use_gpt_value1
                    jsonData["mainSettings"]["ifNoGPT"] = int(lunch_option_value)
                    jsonData["mainSettings"]["infoUpdateInterval"] = int(update_interval_value)

                    jsonDone = json.dumps(jsonData, indent=4)
                    settFile.seek(0)
                    settFile.write(jsonDone)
                    settFile.truncate()

                with open("data/config.json", "r+", encoding="utf-8") as configFile:
                    jsonData = json.load(configFile)
                    jsonData["data"]["settingsFile"] = settings_file_value

                    jsonDone = json.dumps(jsonData, indent=4)
                    configFile.seek(0)
                    configFile.write(jsonDone)
                    configFile.truncate()

                if odpovedd:
                    updateOrderForIdk = int(check_every_value)
                    infoUpdateInterval = int(update_interval_value)
                    aktualizacePrvku = int(update_interval_value)
                    settingsFile = settings_file_value
                    useGPT = use_gpt_value1
                    ifNoGPT = int(lunch_option_value)
                    
            else:
                messagebox.showwarning("Pozor!", f"V nastavení došlo k chybě {chybaset}")
                
        except Exception as excp:
            writeToDebug(f"Error8/1: Error while saving settings: {excp}")
        
        
    settingsFile1 = settingsFile
        
    def startSettings():
        global loginEveryDays, orderUpdateInterval, useGPT, uzivatel, ifNoGPT, pwd, infoUpdateInterval, settingsFile1, encryptPwd, checkOnSave
        
        # Načte do proměn hodnoty z souboru nastavení
        
        try:
            with open(settingsFile, "r", encoding="utf-8") as settingsFileIDK:
                settinsPref = json.load(settingsFileIDK)

                checkOnSave =  settinsPref["mainSettings"]["checkOnSave"]
                    
                loginEveryDays = settinsPref["mainSettings"]["loginEveryDays"]
                orderUpdateInterval = settinsPref["mainSettings"]["orderUpdateInterval"]
                useGPT = settinsPref["mainSettings"]["useGPT"]
                uzivatel = settinsPref["mainSettings"]["uzivatel"]
                ifNoGPT = settinsPref["mainSettings"]["ifNoGPT"]
                pwd = settinsPref["mainSettings"]["pwd"]
                infoUpdateInterval = settinsPref["mainSettings"]["infoUpdateInterval"]
                encryptPwd = settinsPref["mainSettings"]["encryptPwd"]

                if settinsPref["mainSettings"]["encryptPwd"] == True:
                    key = settinsPref["mainSettings"]["key"]
                    pwd2 = Fernet(key.encode()).decrypt(pwd.encode()).decode() #.encrypt(message.encode)
                    pwd = pwd2
                    
            with open("data/config.json", "r", encoding="utf-8") as configFile:
                jsonData = json.load(configFile)
                settingsFile1 = jsonData["all"]["settingsFile"]
                    
        except Exception as excp:
            writeToDebug(f"Error7/1: Error occurred while loading settings from {settingsFile} while startSettings. Exception: {excp}")
                

    def cancel():
        
        startSettings()
        
        login_days_entry.delete(0, tk.END)
        login_days_entry.insert(0, loginEveryDays)
        
        password_entry.delete(0, tk.END)
        password_entry.insert(0, pwd)  # Základní hodnota
        
        login_days_entry.delete(0, tk.END)
        login_days_entry.insert(0, loginEveryDays)
        
        check_every_entry.delete(0, tk.END)
        check_every_entry.insert(0, orderUpdateInterval)
        
        update_interval_entry.delete(0, tk.END)
        update_interval_entry.insert(0, infoUpdateInterval)
        
        settings_file_entry.delete(0, tk.END)
        settings_file_entry.insert(0, settingsFile1)
        
        if encryptPwd == True:
            encrypt_dropdown_var.set(encrypt_options[0])
        else:
            encrypt_dropdown_var.set(encrypt_options[1])
            
        if useGPT == True:
            use_gpt_dropdown_var.set(use_gpt_options[0])
        else:
            use_gpt_dropdown_var.set(use_gpt_options[1])
        
    startSettings()

    # Vytvoření skrolovatelného frame
    canvas = tk.Canvas(root, borderwidth=0, background=bgc, highlightthickness=0)
    frame = tk.Frame(canvas, background=bgc)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    def on_focus_out(event):
        root.focus_set()
        
    frame.bind('<Button-1>', on_focus_out)

    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="top", fill="both", expand=True)
    canvas.create_window((4, 4), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
    frame.bind("<Enter>", lambda event: root.bind_all("<MouseWheel>", on_mousewheel))
    frame.bind("<Leave>", lambda event: root.unbind_all("<MouseWheel>"))

    # Váš obsah frame
    bgc = "white"

    # Jméno (entry)
    name_label = tk.Label(frame, text="Jméno:")
    name_label.configure(bg=bgc)    
    name_label.pack(padx=(0, 10))
    name_entry = tk.Entry(frame)
    name_entry.pack()
    name_entry.delete(0, tk.END)
    name_entry.insert(0, uzivatel)  # Základní hodnota

    # Heslo (entry)
    password_label = tk.Label(frame, text="Heslo:")
    password_label.configure(bg=bgc)    
    password_label.pack(padx=(0, 10))
    password_entry = tk.Entry(frame, show="*")
    password_entry.pack()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, pwd)  # Základní hodnota

    # Encryptovat heslo do souboru (Dropdown ano/ne)
    encrypt_label = tk.Label(frame, text="Encryptovat heslo do souboru:")
    encrypt_label.configure(bg=bgc)
    encrypt_label.pack(padx=(0, 10))
    encrypt_options = ["Ano", "ne"]
    
    encrypt_dropdown_var = tk.StringVar()
    
    if encryptPwd == True:
        encrypt_dropdown_var = tk.StringVar(value=encrypt_options[0])
    else:
        encrypt_dropdown_var = tk.StringVar(value=encrypt_options[1])
        
    encrypt_dropdown = tk.OptionMenu(frame, encrypt_dropdown_var, *encrypt_options)
    encrypt_dropdown.pack()

    # Přihláši každých dnů (entry)
    login_days_label = tk.Label(frame, text="\n\n\nPřihlášení každých dnů:")
    login_days_label.configure(bg=bgc)
    login_days_label.pack(padx=(0, 10))
    login_days_entry = tk.Entry(frame)
    login_days_entry.pack()
    login_days_entry.delete(0, tk.END)
    login_days_entry.insert(0, loginEveryDays)  # Základní hodnota

    # Checknou pokaždé (entry)
    check_every_label = tk.Label(frame, text="Checknout pokaždé:")
    check_every_label.configure(bg=bgc)
    check_every_label.pack(padx=(0, 10))
    check_every_entry = tk.Entry(frame)
    check_every_entry.pack()
    check_every_entry.delete(0, tk.END)
    check_every_entry.insert(0, orderUpdateInterval)  # Základní hodnota

    # Použít GPT (Dropdown ano/ne)
    use_gpt_label = tk.Label(frame, text="\n\n\nPoužít GPT:")
    use_gpt_label.configure(bg=bgc)
    use_gpt_label.pack(padx=(0, 10))
    use_gpt_options = ["Ano", "ne"]
    
    use_gpt_dropdown_var = tk.StringVar()
    
    if useGPT == True:
        use_gpt_dropdown_var = tk.StringVar(value=use_gpt_options[0])
    else:
        use_gpt_dropdown_var = tk.StringVar(value=use_gpt_options[1])
    
    use_gpt_dropdown = tk.OptionMenu(frame, use_gpt_dropdown_var, *use_gpt_options)
    use_gpt_dropdown.pack()

    # Když GPT není dostupné vybrat na oběd možnost (Dropdown 1/2)
    lunch_option_label = tk.Label(frame, text="Když chat GPT není dostupné, vybrat na oběd možnost:", wraplength=310)
    lunch_option_label.configure(bg=bgc)
    lunch_option_label.pack(padx=(0, 10))
    lunch_options = ["1", "2"]
    lunch_option_dropdown_var = tk.StringVar()
    
    if ifNoGPT == 1:
        lunch_option_dropdown_var = tk.StringVar(value=lunch_options[0])
    else:
        lunch_option_dropdown_var = tk.StringVar(value=lunch_options[1])
    
    lunch_option_dropdown = tk.OptionMenu(frame, lunch_option_dropdown_var, *lunch_options)
    lunch_option_dropdown.pack()

    # Interval updatu Přehledu (entry)
    update_interval_label = tk.Label(frame, text="\n\n\nInterval updatu Přehledu:")
    update_interval_label.configure(bg=bgc)
    update_interval_label.pack(padx=(0, 10))
    update_interval_entry = tk.Entry(frame)
    update_interval_entry.pack()
    update_interval_entry.delete(0, tk.END)
    update_interval_entry.insert(0, infoUpdateInterval)  # Základní hodnota

    # Soubor nastavení (entry)
    settings_file_label = tk.Label(frame, text="Soubor nastavení:")
    settings_file_label.configure(bg=bgc)
    settings_file_label.pack(padx=(0, 10))
    settings_file_entry = tk.Entry(frame)
    settings_file_entry.pack()
    settings_file_entry.delete(0, tk.END)
    settings_file_entry.insert(0, settingsFile1)  # Základní hodnota
    
    n_label = tk.Label(frame, text="\n")
    n_label.configure(bg=bgc)
    n_label.pack(padx=(0, 10))

    # Tlačítka Zrušit a Uložit (tlačítko - oboje budou zarovnaná napravo)
    save_button = tk.Button(frame, text="Uložit", command=save_settings)
    save_button.pack(side="right", pady=5, padx=5)
    
    cancel_button = tk.Button(frame, text="Zrušit", command=cancel)
    cancel_button.pack(side="right", pady=5, padx=5)



def changeToRm():
    global after_loop1, waited, vlakno1bezi, after_loop2, uh, thread5
    
    
    if allowRM:
        
        after_loop1 = False

        # Zavření aktuálního okna
        for widget in root.winfo_children():
            if widget.winfo_class() != 'Menu':
                widget.destroy()

        def sv():
            global waited, vlakno1bezi, after_loop2, threads

            def t1():
                global waited, threads

                toplevel_vlakno1 = tk.Toplevel()
                toplevel_vlakno1.title("Vlákno 1")

                def stop():
                    global vlakno1bezi, threads

                    if "1" in threads:
                        threads.remove("1")

                    exit_event.set()
                    thread1.join()
                    vlakno1bezi = False

                def start():
                    global waited, vlakno1bezi, threads

                    if "1" not in threads:
                        threads.append("1")

                    exit_event.clear()
                    waited = 0
                    vlakno1bezi = True
                    thread1 = threading.Thread(target=vlakno1)
                    thread1.start()

                t1Start_button = tk.Button(toplevel_vlakno1, text="Zastavit", command=stop)
                t1Start_button.pack(pady=5)

                t1Stop_button = tk.Button(toplevel_vlakno1, text="Sputit", command=start)
                t1Stop_button.pack(pady=5)



            def t2():
                global vlakno2bezi, threads

                toplevel_vlakno2 = tk.Toplevel()
                toplevel_vlakno2.title("Vlákno 2")

                def stop():
                    global vlakno2bezi, threads

                    if "2" in threads:
                        threads.remove("2")

                    thread2.join()
                    vlakno2bezi = False

                def start():
                    global waited, vlakno2bezi, threads

                    if "2" not in threads:
                        threads.append("2")

                    vlakno2bezi = True
                    thread2 = threading.Thread(target=vlakno2)
                    thread2.start()

                t2Start_button = tk.Button(toplevel_vlakno2, text="Zastavit", command=stop)
                t2Start_button.pack(pady=5)

                t2Stop_button = tk.Button(toplevel_vlakno2, text="Sputit", command=start)
                t2Stop_button.pack(pady=5)


            def t3():
                global threads

                toplevel_vlakno3 = tk.Toplevel()
                toplevel_vlakno3.title("Vlákno 3")

                def stop():
                    global threads

                    if "3" in threads:
                        threads.remove("3")  
                    exit()

                def start():
                    pass
                
                t3Start_button = tk.Button(toplevel_vlakno3, text="Zastavit", command=stop)
                t3Start_button.pack(pady=5)

                t3Stop_button = tk.Button(toplevel_vlakno3, text="Sputit", command=start)
                t3Stop_button.pack(pady=5)


            def t4():
                global after_loop2, threads

                

                toplevel_vlakno4 = tk.Toplevel()
                toplevel_vlakno4.title("Vlákno 4")

                def stop():
                    global vlakno4bezi, after_loop2, threads
                    
                    if "4" in threads:
                        threads.remove("4")
                        
                    after_loop2 = False

                    thread4.join()
                    vlakno4bezi = False

                def start():
                    global waited, vlakno4bezi, after_loop2, threads

                    if "4" not in threads:
                        threads.append("4")

                    after_loop2 = True

                    vlakno4bezi = True
                    thread4 = threading.Thread(target=vlakno4)
                    thread4.start()

                t4Start_button = tk.Button(toplevel_vlakno4, text="Zastavit", command=stop)
                t4Start_button.pack(pady=5)

                t4Stop_button = tk.Button(toplevel_vlakno4, text="Sputit", command=start)
                t4Stop_button.pack(pady=5)



            def t5():
                global vlakno5bezi, threads

                toplevel_vlakno5 = tk.Toplevel()
                toplevel_vlakno5.title("Vlákno 5")

                def stop():
                    global vlakno5bezi, threads

                    if "5" in threads:
                        threads.remove("5")

                    thread5.join()
                    vlakno5bezi = False

                def start():
                    global waited, vlakno5bezi, threads

                    if "5" not in threads:
                        threads.append("5")

                    vlakno5bezi = True
                    thread5 = threading.Thread(target=vlakno5)
                    thread5.start()

                t5Start_button = tk.Button(toplevel_vlakno5, text="Zastavit", command=stop)
                t5Start_button.pack(pady=5)

                t5Stop_button = tk.Button(toplevel_vlakno5, text="Sputit", command=start)
                t5Stop_button.pack(pady=5)


            toplevel_vlaken = tk.Toplevel()
            toplevel_vlaken.title("Spravovat vlákna")

            thread1_button = tk.Button(toplevel_vlaken, text="Vlákno 1", command=t1)
            thread1_button.pack(pady=5)

            thread2_button = tk.Button(toplevel_vlaken, text="Vlákno 2", command=t2)
            thread2_button.pack(pady=5)

            thread3_button = tk.Button(toplevel_vlaken, text="Vlákno 3", command=t3)
            thread3_button.pack(pady=5)

            thread4_button = tk.Button(toplevel_vlaken, text="Vlákno 4", command=t4)
            thread4_button.pack(pady=5)

            thread5_button = tk.Button(toplevel_vlaken, text="Vlákno 5", command=t5)
            thread5_button.pack(pady=5)

        def csf():
            def save_file(obsah, file):
                with open(file, "w", encoding="utf-8") as trainFilee:
                    trainFilee.write(obsah)
            
            def loadTE(file):
                editor_window = tk.Toplevel(root)
                editor_window.title(f"Úprava {file}")

                editor_window.bind("<Control-s>", lambda event: save_file(text_editor.get("1.0", "end-1c"), file))

                # Vytvoření nového textového pole
                text_editor = tk.Text(editor_window, wrap="word", height=20, width=80)
                text_editor.pack(pady=10, fill=tk.BOTH, expand=True)

                # Tlačítko pro uložení
                button_save = ttk.Button(editor_window, text="Uložit", command=lambda: save_file(text_editor.get("1.0", "end-1c"), file))
                button_save.pack(side=tk.LEFT, padx=5)

                with open(file, "r", encoding="utf-8") as trainFilee:
                    obsah = trainFilee.read()

                text_editor.delete("1.0", tk.END)  # Smazat stávající obsah editoru
                text_editor.insert(tk.END, obsah)  # Vložit obsah souboru do editoru
                
            loadTE(settingsFile)
            loadTE("data/config.json")
            
        
        def lpp():
            pass
    

        threads_button = tk.Button(root, text="Spravovat vlákna", command=sv)
        threads_button.pack(pady=5)

        files_button = tk.Button(root, text=f"Soubory config.json a {settingsFile}", command=csf)
        files_button.pack(pady=5)

        threads_button = tk.Button(root, text="Nastavení proměn programu", command=lpp)
        threads_button.pack(pady=5)
        
        #cmd_button = tk.Button(root, text="CMD mód", command=ecmdmHand)
        #cmd_button.pack(pady=5)

        def start():
            if showMode4Alert:
                messagebox.showwarning("Varování!", "Při špatném zacházení může dojít ke: strátě dat, crashnutí programu, či dalším nečekaným hrozbám.")

        start()
        
    else:
        messagebox.showerror("Chyba", "Funkce není povolena")
    

def exitPg():
    global vlakno1bezi, exit_event, thread1, vlakno2bezi, vlakno3bezi, vlakno4bezi, vlakno5bezi, problems, bgc, codeRunning, allOrders, lastOrder, exit_event

    for widget in root.winfo_children():
        widget.destroy()
        
    labelIDK = tk.Label(root, text="Zavírám...")
    labelIDK.config(bg=bgc)
    labelIDK.pack()
        
    root.minsize(200, 50)
    root.geometry("200x50")
    
    exit_event.set()
    vlakno1bezi = False
    vlakno2bezi = False
    vlakno3bezi = False
    vlakno4bezi = False
    vlakno5bezi = False
    problems = []
    codeRunning = "ne"
    
    with open(currentDataFile, "w", encoding="utf-8") as currFile:
        currFile.write(f"problems: lastPRproblems: {' '.join(problems)}\nlastOrder: lastPRlastOrder: {lastOrder}\ncodeRunning: ne\nthreads: \nallOrders: \nnextOrderUpdate: 0")
        
    with open("data/config.json", "r+", encoding="utf-8") as configFile:
        jsonData = json.load(configFile)
        jsonData["data"]["shutDownProperly"] = True
        jsonData["data"]["allOrders"] = allOrders
        jsonData["data"]["lastOrder"] = lastOrder
        jsonDone = json.dumps(jsonData, indent=4)
        configFile.seek(0)
        configFile.write(jsonDone)
        configFile.truncate()
    
    exit_event.set()
    thread1.join()
    exit_event.clear()
    
    def finn():
        exit()
    
    root.after(500, finn)
    
def exitPg2(exitt):
    global vlakno1bezi, exit_event, thread1, vlakno2bezi, vlakno3bezi, vlakno4bezi, vlakno5bezi, problems, bgc, codeRunning, allOrders, lastOrder, exit_event

    exit_event.set()
    vlakno1bezi = False
    vlakno2bezi = False
    vlakno3bezi = False
    vlakno4bezi = False
    vlakno5bezi = False
    problems = []
    codeRunning = "ne"
    
    with open(currentDataFile, "w", encoding="utf-8") as currFile:
        currFile.write(f"problems: lastPRproblems: {' '.join(problems)}\nlastOrder: lastPRlastOrder: {lastOrder}\ncodeRunning: ne\nthreads: \nallOrders: \nnextOrderUpdate: 0")
    
    with open("data/config.json", "r+", encoding="utf-8") as configFile:
        jsonData = json.load(configFile)
        jsonData["data"]["shutDownProperly"] = True
        jsonData["data"]["allOrders"] = allOrders
        jsonData["data"]["lastOrder"] = lastOrder
        jsonDone = json.dumps(jsonData, indent=4)
        configFile.seek(0)
        configFile.write(jsonDone)
        configFile.truncate()
    
    exit_event.set()
    thread1.join()
    exit_event.clear()
    
    if exitt:
        if thread5:
            thread5.join()
        exit()


        
def end_all_threads(exittt):
    global vlakno1bezi, vlakno2bezi, vlakno3bezi, vlakno4bezi, vlakno5bezi, after_loop1, after_loop2
    
    after_loop1 = False
    exit_event.set()
    thread1.join()
    vlakno1bezi = False 
    thread2.join()
    vlakno2bezi = False
    vlakno3bezi = False
    after_loop2 = False
    thread4.join()
    vlakno4bezi = False
    
    if exittt:
        exit()
    
def ev5(threadd):
    threadd.join()
    
def vlakno5():
    global thread5, threads, thread1, restart_gui, brk_end_loop, uh, vlakno5bezi

    try:
        if "5" not in threads:
            threads.append("5")

        def uh(clea):
            global thread5, threads, thread1, restart_gui, brk_end_loop, vlakno5bezi
            
            if clea:
                os.system("cls" if os.name == "nt" else "clear")
            endI = input("Zmáčkni enter pro obnovu okna (jinak exit/res) ")

            if endI.lower() == "exit" or endI.lower() == "escape" or endI.lower() == "odejit" or endI.lower() == "zrusit":
                brk_end_loop = True
                vlakno5bezi = False
                exitPg2(True)
            elif endI.lower() == "res" or endI.lower() == "obnovit":
                os.system("cls" if os.name == "nt" else "clear")
                exitPg2(False)
                vlakno5bezi = False
                brk_end_loop = True
                os.system(f"python res.py gui.py {os.getpid()} restart")

            elif endI.lower() == "cmd":
                    print("CMD mód není od verze 0.87 podporován")
                    os.system("cls" if os.name == "nt" else "clear")
                    time.sleep(3)
                    
        uh(True)
                
        os.system("cls" if os.name == "nt" else "clear")

        restart_gui = True
        vlakno5bezi = False

        if "e4" in problems:
            problems.remove("e4")
            

    except Exception as excp:
        writeToDebug(f"Error4: Error occurred while starting thread5. Exception: {excp}")
        if "e4" not in problems:
            problems.append("e4")

    
def vlakno4():
    global currentDataFile, threads, waited
    
    if "4" not in threads:
        threads.append("4")
    
    try:
        with open(settingsFile, "r", encoding="utf-8") as soubor:
            aktualizacePrvku = int(json.load(soubor)["mainSettings"]["infoUpdateInterval"]) * 1000
            
        with open(currentDataFile, "w", encoding="utf-8") as currFile:
            currFile.write(f"problems: {' '.join(problems)}\nlastOrder: {lastOrder}\ncodeRunning: {codeRunning}\nthreads: {' '.join(threads)}\nallOrders: {allOrders}\nnextOrderUpdate: {waited}")
            
        if "e3/2" in problems:
            problems.remove("e3/2")
            
    except Exception as excp:
        writeToDebug(f"Error3: Could not get infoUpdateInterval from from {settingsFile} while updating currentData.txt. Exception: {excp}")
        problems.append("e3/2")
    
    if after_loop2:
        root.after(aktualizacePrvku, vlakno4)

    
def vlakno2():
    global label, thread1, vlakno1bezi, restartV1, showErrors, waited, infoUpdateInterval

    
    if "2" not in threads:
        threads.append("2")
    
    def restartV1(event):
        global thread1, vlakno1bezi, showErrors, waited
        
        if vlakno1bezi:
            exit_event.set()
            vlakno1bezi = False
            thread1.join()
            
            def finish():
                global vlakno1bezi, exit_event, thread1, waited
                
                waited = 0
                
                vlakno1bezi = True
                exit_event.clear()
    
                thread1 = threading.Thread(target=vlakno1)
                
                if 1 in threadsjson:
                    waited = 0
                    
                    thread1.start()
                
            root.after(10, finish)
            
            if "w1/1" in problems:
                problems.remove("w1/1")
        else:
            if showErrors:
                messagebox.showerror("Pozor!", "Při pokusu restartovat vlákno 1 (přeskočit čekání) došlo k záchytu potenciálního problému. Vlákno 1 neběží, takže funkce pro přihlášení obědu neběží. Warning1")
            if "w1/1" not in problems:
                problems.append("w1/1")
            
    def bind():
        if label:
            if label.winfo_exists():
                label.bind("<Button-1>", restartV1)
                
    bind()


def vlakno1():
    global vlakno1bezi, thread2, waited, posledniObjednavka, celkemObjednavek, lastOrder, allOrders
    
    vlakno1bezi = True
    
    try:
        with open(settingsFile, "r", encoding="utf-8") as soubor:
            orderUpdateInterval = int(json.load(soubor)["mainSettings"]["orderUpdateInterval"]) * 1000
    except Exception as excp:
        writeToDebug(f"Error3: Could not get infoUpdateInterval from from {settingsFile} while updating window. Exception: {excp}")
        if "e3/1" not in problems:
            problems.append("e3/3")

    def insidewrapper():
        global waited, posledniObjednavka, celkemObjednavek, lastOrder, allOrders
    
        print("Upozornění: kód je stále ve vývoji a proto se zatím přihlašuje při každém obědnání")
        waited = 0
    
        with open(settingsFile, "r", encoding="utf-8") as settFile:
            nastaveni = json.load(settFile)
            cislo_jidelny = nastaveni["mainSettings"]["cislo_jidelny"]
            jmeno = nastaveni["mainSettings"]["uzivatel"]
            if nastaveni["mainSettings"]["encryptPwd"] == True:
                    pwd = nastaveni["mainSettings"]["pwd"]
                    key = nastaveni["mainSettings"]["key"]
                    pwd = Fernet(key.encode()).decrypt(pwd.encode()).decode()
                    heslo = pwd
            else:
                heslo = nastaveni["mainSettings"]["pwd"]
        
        if jmeno != "" and heslo != "":
            data = {"cislo": cislo_jidelny, "jmeno":jmeno, "heslo":heslo, "zustatPrihlasen":False, "lang":"CZ"}
    
            json_data = json.dumps(data)
    
            # Odeslání HTTP požadavku
            odpoved = requests.post('https://app.strava.cz/api/login', data=json_data, headers={'Content-Type': 'text/plain'})
    
    
            odpoved_slovnik = json.loads(odpoved.text)
    
            try:
                sid = odpoved_slovnik["sid"]
                jmeno = odpoved_slovnik["jmeno"]
                cislo = odpoved_slovnik["uzivatel"]["cislo"]
                s5url = odpoved_slovnik["s5url"]
                url = s5url
            except Exception as excp:
                writeToDebug(f"Error10: Error occured while trying to order lunch. Exception: {excp}")
                return
    
            # Níže jsou stálé
            konto = 0
            podminka = ""
            ignoreCert = "true"
            resetTables = False
    
            data = {'dataString': f'{sid}&{s5url}&{cislo}&true&true'}
    
            json_data = json.dumps(data)
    
            # Odeslání HTTP požadavku
            odpoved = requests.post('https://app.strava.cz/api/coder', data=json_data, headers={'Content-Type': 'text/plain'})
    
            data = {'cislo': cislo, "sid":sid, "s5url":s5url, "konto":konto, "podminka":podminka, "ignoreCert":ignoreCert, "resetTables":resetTables, "lang":"CZ"}
        
            json_data = json.dumps(data)
        
            # Odeslání HTTP znovu požadavku
            odpoved = requests.post('https://app.strava.cz/api/objednavky', data=json_data, headers={'Content-Type': 'text/plain'})
            odpoved_json = json.loads(odpoved.text)
            
            if ifNoGPT == 1:
                veta = int(odpoved_json[str(list(odpoved_json.keys())[-1])][1]["veta"])
            else:
                veta = int(odpoved_json[str(list(odpoved_json.keys())[-1])][1]["veta"]) + 1
                
    
            print(f"Na oběd bude výbrána možnost: {ifNoGPT}, protože Chat GPT ještě není podporováno")
            
            if ifNoGPT == 1:
                lo = odpoved_json[str(list(odpoved_json.keys())[-1])][1]["nazev"]
            else:
                lo = odpoved_json[str(list(odpoved_json.keys())[-1])][2]["nazev"]
            
            
            if lo != lastOrder:
                posledniObjednavka = lo
                lastOrder = lo
                celkemObjednavek = int(celkemObjednavek) + 1
                allOrders = int(allOrders) + 1
    
            data = {'cislo': cislo, "sid":sid, "url":url, "veta":str(veta), "pocet":1, "ignoreCert":ignoreCert, "lang":"CZ"}
    
            json_data = json.dumps(data)
    
            # Odeslání HTTP zase požadavku
            odpoved = requests.post('https://app.strava.cz/api/pridejJidloS5', data=json_data, headers={'Content-Type': 'text/plain'})
            
    
            data = {'cislo': cislo, "sid":sid, "url":url, "xml":None, "pocet":1, "ignoreCert":ignoreCert, "lang":"CZ"}
    
            json_data = json.dumps(data)
    
            # Odeslání HTTP požadavku
            odpoved = requests.post('https://app.strava.cz/api/saveOrders', data=json_data, headers={'Content-Type': 'text/plain'})
            
    
            for i in range(orderUpdateInterval):
                if not exit_event.is_set():
                    time.sleep(1)
                    waited = waited + 1
                    
            if not exit_event.is_set():      
                insidewrapper()

    
    insidewrapper()
    

    vlakno1bezi = False

    
def closeGUI():
    global vlakno3bezi, vlakno5bezi, vlakno1bezi, vlakno2bezi, vlakno3bezi, vlakno4bezi, after_loop1, thread5, codeRunning, thread1, thread2, thread4
    
    codeRunning = "no"
        
    vlakno3bezi = False
    vlakno5bezi = True
    vlakno1bezi = True
    vlakno2bezi = False
    vlakno4bezi = False
    after_loop1 = False
    
    #vypnutí všech vláken kromě: 1 a 5
    if vlakno4bezi:
        thread4.join()
        
    if vlakno2bezi:
        thread2.join()
        
    if "2" in threads:
        threads.remove("2")
        
    if "3" in threads:
        threads.remove("3")
        
    if "4" in threads:
        threads.remove("4")
    
    
    if ShutOnClose:
        exitPg()
    else:
        thread5 = threading.Thread(target=vlakno5)
        if 5 in threadsjson:
            thread5.start()        
        
        root.after(500, root.destroy)


def startGUI():    
    global root, menu, after_loop1, codeRunning, thread5, thread1, thread2, thread4, bgc, restart_gui, brk_end_loop
    
    after_loop1 = True
    codeRunning = "ano"
    
    with open("data/config.json", "r+", encoding="utf-8") as configFile:
        jsonData = json.load(configFile)
        jsonData["data"]["shutDownProperly"] = False
        jsonDone = json.dumps(jsonData, indent=4)
        configFile.seek(0)
        configFile.write(jsonDone)
        configFile.truncate()
    
    
    if "3" not in threads:
        threads.append("3")
        
    if not vlakno1bezi:
        if "1" not in threads:
            threads.append("1")
        
        thread1 = threading.Thread(target=vlakno1)
        if 1 in threadsjson:
            thread1.start()
    else:
        if "1" not in threads:
            threads.append("1")
    
        
    if "5" in threads:
        threads.remove("5")
        
    if 1 in threadsjson:
        if "w2/1" in problems:
            problems.remove("w1/1")
    else:
        if showErrors:
            messagebox.showerror("Pozor!", "Vlákno 1 je zakázáno funkce pro přihlášení jídel nebude fungovat a kód se může na nečekaných místech robít, hrozí stráta dat.")
        if "w2/1" not in problems:
            problems.append("w2/1")

    if 2 in threadsjson:
        if "w2/2" in problems:
            problems.remove("w2/2")
    else:
        if showErrors:
            messagebox.showerror("Pozor!", "Vlákno 2 je zakázáno funkce pro obnovu časunebude fungovat a kód se může na nečekaných místech robít, hrozí stráta dat.")
        if "w2/2" not in problems:
            problems.append("w2/2")
            
    if 3 in threadsjson:
        if "w2/3" in problems:
            problems.remove("w2/3")
    else:
        if showErrors:
            messagebox.showerror("Pozor!", "Vlákno 3 je zakázáno kód nebude fungovat.")
        if "w2/3" not in problems:
            problems.append("w2/3")
            
    if 4 in threadsjson:
        if "w2/4" in problems:
            problems.remove("w2/4")
    else:
        if showErrors:
            messagebox.showerror("Pozor!", "Vlákno 4 je zakázáno funkce zapisování aktuálních dat nebude fungovat a kód se může na nečekaných místech robít, hrozí stráta dat.")
        if "w2/4" not in problems:
            problems.append("w2/4")
            
    if 5 in threadsjson:
        if "w2/5" in problems:
            problems.remove("w2/5")
    else:
        if showErrors:
            messagebox.showerror("Pozor!", "Vlákno 5 je zakázáno funkce po zavření okna nebude fungovat a kód se automaticky po zavření okna vypne")
        if "w2/5" not in problems:
            problems.append("w2/5")

    
    # Vytvoření okna
    try:
        if 3 in threadsjson:

            root = tk.Tk()
            root.geometry("400x300")
            root.title("Automatické přihlášení obědů")
            root.minsize(320, 300)
            root.maxsize(320, 300)
            root.configure(bg=bgc)

            # Vytvoření menu
            menu = tk.Menu(root)
            root.config(menu=menu)

            menu.add_cascade(label="Přehled", command=changeToPrehled)
            menu.add_cascade(label="Nastavení", command=changeToNastaveni)
            menu.add_cascade(label="Chat GPT", command=changeToCgpt)
            menu.add_cascade(label="Rozšířené možnosti", command=changeToRm)

            changeToPrehled()

            #start vlakno1 vlakno2 vlakno4

            thread4 = threading.Thread(target=vlakno4)
            if 4 in threadsjson:
                thread4.start()

            def rth2():
                global thread2
                
                thread2 = threading.Thread(target=vlakno2)
                if 2 in threadsjson:
                    thread2.start()

            root.after(1000, rth2)

            root.protocol('WM_DELETE_WINDOW', closeGUI)
            root.mainloop()
            
            while restart_gui == False and brk_end_loop == False:
                pass
                
            if restart_gui != False:
                restart_gui = False
                startGUI()
        
    except Exception as excp:
        writeToDebug(f"Error2: Could not start GUI. Exception: {excp}")
        if "e2" not in problems:
            problems.append("e2")

startGUI()