Info.md
=======
- Všechny potřebné informace pro tento projekt

1. Errory a varování:
    Error1/1: Could not load config.json Exception {excp}
    Error1/2: Could not load settings file Exception {excp}
    Error2: Could not start GUI. Exception: {excp}
    Error3/1: Could not get infoUpdateInterval from from {settingsFile} while updating window. Exception: {excp}
    Error3/2: Could not get infoUpdateInterval from from {settingsFile} while updating currentData.txt. Exception: {excp}
    Error3/3: Could not get infoUpdateInterval from from {settingsFile} while updating window. Exception: {excp}
    Error4: Error occurred while starting thread5. Exception: {excp}
    Error5: Error occurred while loading Přehled. Exception: {excp}
    Error6: Could not import cryptography.fernet
    Error7/1: Error occurred while loading settings from {settingsFile} while startSettings. Exception: {excp}
    Error7/2: Error occurred while loading settings from {settingsFile} while startSettings (GPT). Exception: {excp}
    Error8/1: Error while saving settings: {excp}
    Error9/1: encrypt_value is not set to 'Ano' or 'ne'
    Error9/2: use_gpt_value is not set to 'Ano' or 'ne'
    Error10: Error occured while trying to order lunch. Exception: {excp}

    Warning1: Při pokusu restartovat vlákno 1 (přeskočit čekání) došlo k zychycení potencionálního problému. Vlákno 1 neběží, takže funkce pro přihlášení obědu neběží. (/1)
    Warning2/_: Vlákno {vlakno} je zakázáno funkce {funkce} nebude fungovat a kód se může na nečekaných místech robít, hrozí stráta dat /a kód se automaticky po zavření okna vypne /kód nebude fungovat

    Chyba: Funkce není povolena <- chyba při otevírání Rozšírených možností, které nejsou povoleny
    Uložení nastavení: "Chcete uložené změny uprlatnit už teď? (Může přijít ke problémům v kódu - soubory se uloží do konfiguračního souboru nastavení, ale při přijmutí se změny nastaví v běžícím kódu, při chybě můžete restartovat potřebná vlákna) <- kód používá proměny, ve kterých jsou uloženy potřebné info, při

1.1. Troubleshooting:
    Error1: Zkontrolujte zda soubor config.json existuje a zjistěte jak váš Python Interpeer přistupuje k cwd. 
    Error2: Zkontrolujte chybu a případně se ji pokuste opéravit (pozor, když nastane chyba v funkci volaná z startGUI a nemá try-except tak chybu uidíte u e2)
    Error3: Nemusí se jednat o specifikovanou chybu, vše uvidíte v Exception, zkuste projít konfigurační soubory jestli jsou OK a případně upravit
    Error4: Při této chybě se může jednat o použití 'cls' na Linuxech - nahraďte 'cls' s 'clear' nebo s chybou root2, či s voláním exitPg2
    Error5: Nezle jednoduše určit chybu, jedná se něco se scénou Přehled, musíte si chybu najít sami
    Error6: Stáhněte si cryptography pomocí pip install cryptography (případně pip install cryptography.fernet)
    Error7: Zkontrolujte zda soubor pro nastavení se spravně sestaven a zda máte knihovnu cryptography
    Error8: V chybové hlášce uvidíte o jakou chybu se jedná. Buď nastala chyba s získáváním hodnoty z pole, nebo je chyba s některým z json souborů.
    Error9: Dopdown by měl být nastaven na hodnoty Ano nebo ne, pokud tomu tak není, tato chyba se objeví. S tím asi nic.
    Error10: Nastala chyba při přihlašování, nejspíš se jedná o špatné údaje. Zkontrolujte chubu a případně se zeptejte někoho, kdo umí progrtamovat.

    *Pokud nastane chyba a Exception je 'název', tak se jedná nejspíše o chybu v .json souboru, že ten 'název' nebyl nalezen. Zkontrolujte daný json soubor*

    Warning1: Je možné že se chyba objeví, protože nebylo možné přistoupit k proměně -> pokud neběží časovač pokuste se přijít na problém, pokud běží ignorujte to

    Chyba, Funkce není povolena -> v config.json nastavte v sekci 'all' allowRM na true
    Uložení nastavení: "Chcete uložené změny uprlatnit už teď? (Může přijít ke problémům v kódu - soubory se uloží do konfiguračního souboru nastavení, ale při přijmutí se změny nastaví v běžícím kódu, při chybě můžete restartovat potřebná vlákna) -> při chybě to smáčknutí Ano je možné že dojde, restartujte kód


2. Vlákna:
    1vlákno: spustí funkci na obědnávání, poté časovač <- přičaosvači to zapíše za jak dlouho novy update jidel
    2vlákno: Když klikneš na čaš spustí to vlákno1 znovu
    3vlákno: gui < hlavní chod aplikace, není vlákno
    4vlákno: Zapíše data do currentData.txt (vlákna, běží kód, posl obj, celkem obj, problémy)
    5vlákno: Když se zavře 3vlákno spustí se toto a naslouchá na entru pro spuštění vlákna 3

2.2 Troubleshooting:
    - Pokud se neobjeví nic v logu, můžete se chybu pokusit opravit v sekci Rozšířené možnosi
    - Můžete skusit startnout program v módu kontroly programu (config.json: data > runCheck nastavte na true), nebo si data znovu nastavit přes setup (config.json: data > setup nastavte na true)
    - Když chybu nenajdete kontaktujte mě, já pomůžu :3


3. debug.txt:
    - V debug.txt najdete log chyb na místech v kódu kde jsou chyby pravděpodobné
    - Pokud chcete vypnout zápis do debugu, přepněte debug v config sekci all na false
    - V některých veřejných verzích je debug základně vypnut
    - Error "Error5: Error occurred while loading P ehled. Exception: name 'restartV1' is not defined" můžete ignorovat, pak to opravím


4. Trénování Chat GPT:
    - Vyplňte všechny info v sekci Chat GPT > klikněte na trénovat > trénovat (otevřít trénovací soubor umožňuje raw editaci souboru)
    - Při chybě jděte do konverzace a pokuste se Chat GPT vysvětlit co má dělat sám, historie chatu je jedno, jen je potřeba aby odpovídal ve formátu 1 nebo 2
    - Použití Chat GPT lze vypnot přímo v ní dedikované sekci


5. Rozšířené možnosi:
    - Povolte v config.json "allowRM" (nastavte na true) a můžete vstoupit
    - Při nesprávněm zacházení může dojít k: zastavení kódu, strátě dat a dalším problémům - pracování tu je na vlastní riziko
    - Můžete zde upravovat běh vláken, spravovat soubory v built-in text editoru a upravit proměny v kódu - více funkcí přijde až později
    - Při nějaké chybě možná bude nutno nutno spustit kód v kontrolním režimu, nebo znovu nastavit možnost  (config.json: data > runCheck nastavte na true   nebo   config.json: data > setup nastavte na true)


6. *Odstraněno*


7. Chat GPT
    - Když si Chat GPT vytrénujete sami, varovaní se zbavíte když v nastavení (json osuboru) nastavíte trained na True
    - Více info přijde s implementací Caht GPT


8. Další info:
    - Nezavírejte kód pomocí crtl + c > zavře se hlavní vlákno ale jiná běžící vlákna se nazavřou (zejména vlákno 1)
    - Na jakýkoli problém mě upozorni
    - Nech soubor vypnout pomocí: zavení okna a pak vepsání exit, nebo pomocí nastavení v config.json v sekci all ShutOnClose na true
    - Za jakýkoli problém na stravě či šloním účtě neručím, je to na tvé vlastní riziko (ale i tak by snad žádně němělo být)
    - Musí být instalované knihovny requests a cryptography (.fernet) - jestli jste noví v Pythonu, stáhnete si je příkazem: pip install <knihovna>
    - Kliknutím na text kolik zbývá do dalšího obědnání resetujete časovač a obědnávka se hned uskuteční
    - Co znamená když je slovo v množinové závorce? {} znamená, že když bude v ní např.: 'vlákno', tak že v debug.txt místo '{vlákno}' uvidíte '1' > číslo vlákna, tak to funguje všude
    - Kdyby se něco "podělalo" - problém na vašem účtě, problém na škole kvůli tomuto kódu, tak si vzpomeň, že sis ho sám dobrovolně stahoval :) (komu to není jasné, tak za to přebíráte zodpoveďnost vy)


9. Jak kód funguje?
    0. Jako první se v hlavní smyčce načtou info z data/config.json a zknotroluje se v jakém módu má začít program. Pokud v hlaním, tak pokračuje
    1. Kód nastartuje hlavní vlákno a spustí GUI (pojmenováno jako vlákno 3 je hlavní vlákno - hlavní chod programu i když se nejedná o vlákno)
    2. V tomto startu se zapne vlákno 1, 2 a 4
    3. Vlákno 4 se obnovuje na intervalu updateInfoInterval (v settings.json sekce mainSettings) - zároveň na tomto intevralu se obnovuje scéna Přehled
    4. Vlákno 1 zatím nejspíš dokončilo objednávání obědů a teď bude čekat na určitou dobu (v settings.json sekce mainSettings > orderUpdateInterval) - když klikneš na čas, tak se čekání přeruší a provede se objednání a začne znovu čekat
    5. Zatímco je všechno připravené a kód už běží můžete upravit nastavení programu, chat gpt a pokud si věříte tak i Rozšířené možnosti :) 
    6. GUI okno zavřete kliknutím na X na liště okna. Poté entrem nastartujete okno znovu, nebo napsáním exit program vypnete (ano, tvrá to tak dlouho)
    7. Program se vypíná, to zahrnuje: vypnutí všech vláken - jako první se vypnou vlákna 2 - 4, pak při napsání exit se vypne vlákno 1 a naklonec samotné vlákno 5. Ještě předním se nastaví potřebné věci v currenData souboru a v config.json v sekci data se nastaví properShutdown na true. Další potřebné věci pro kód se také uloží aby mohl kód pokračovat tam, kde skončil.


10. Jak začít?
    - Tento odstavec je určen pro ty, kdo jsou noví v Pythonu
    1. Pokud nemáte, tak si stáhněte Python, na všech platformách ho najdete na webu https://python.org, nebo pro Windows na MS Storu
    2. Stáhněte si požadované knihovny - otevřete terminál (napište do vyhledávací lišty 'terminál', nebo 'cmd') a napište 'pip install requests' a 'pip install cryptography'
    3. Spusťte kód a dokončete nastavení aplikace s módu setup (pokud vám to nenabídne, podívejte se, jestli setup je podporován ve vaší vezri a jestli ano, tak jďete do config.json a v sekci data nastavte setup na 'true')
    4. Prozkoumejte kód a zjistěte co dělá - jo, jasně, vím že jsem to sem nemusel dávat, ale fakt to udělejte
    5. Můžete zavřít GUI (graphical user interface) okno - zavřete to bílé okno a nechat na pozadí běžet pouze terminál - jen to černé (modré) okno s pythonem, to ale hlavně nezavírejte
    6. Zmáčknutím entru okno znovu otevřete, napsáním res a poté zmáčknutím entru kód restartujete a napsáním exit odejdete, prosím, vypínejte kód pouze pomocí exit


11. Podporované funkce:
    - Vlákna: 1, 2, 3, 4, 5
    - Cmd
    - Přehled, Nastavení, Nastavení GPT, Rozšířené možnosti > každý má své funce, jako např. v Nastavení můžete změny uplatnit už hned, ale nechce se mi to vypisovat, jen RM
    - RM: Spravovat vlákna, soubory config.json a ..., CMD Mód

    - Možná jsem něco vynechal, neva - setup a check nejsou podporovány

12. Verze:
    - Informace o verzích do datumu níže
    - Poslední update tohoto odstavce: 16:00 24.03.2024
    - Dostupné verze:
        0.88 - veřejná verze; 22.03.2024; optimalizováno pro python 3.11.3; vytvořeno ve VS Code
            - Updaty: Oprava objednávání, oprava res.py, optimalizace
            - Poznámky: přepínání "scén" stále nefunguje pro Linuxy
            
        0.86B - veřejná (beta) verze; 02.03.2024; optimalizováno pro python 3.11.3; vytvořeno ve VS Code
            - Updaty: Větší podpora pro Linuxy, používatený setup, bugfixy
            - Poznámky: GPT pořád nemá podporu a setup není kompletní

        0.85c - veřejná verze; 12.02.2024; optimalizováno pro python 3.11.3
            - Updaty: bugfixy
            - Poznámky: nastavení nejsou nastavena na úplně základní, vše si zatím udělejte sami (seetup je rozpracován, základně nastaven na false), pro nové verze nejspíš udělám github

        0.85b - neveřejná verze; 10.02.2024; optimalizováno pro python 3.11.3
            - Updaty: obědnávání jídel, oprava kódu
            - Poznámky: nastavení nejsou nastavena na úplně základní, vše si zatím udělejte sami (ani setup ještě není), pro nové verze možná udělám github
            !!! tato verze byla od 12.2.2024 stažena (nikdy nikde nebyla, ale ok)