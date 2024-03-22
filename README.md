# strava
Objednává na Stravě z nenovějšího objedu oběd 2.
Kód ještě není v úplně nejlepší formě, ale alespoň dělá to co má.
Níže pak bude rychle popsané fungování a další potřebné inforamce.


### Požadavky
Program potřebuje k běhu splňovat následující podmínky:

1. Operační systém s Pythonem
    - Program je napsaný v Pythonu, takže nemá moc velké požadavky, ale o tom více dole ([Python](https://python.org), [Info o Pythonu - jak si ho stáhnout, atd.](https://python.org/about/gettingstarted/))

2. 32 nebo 64 bitový systém
    - Jen píšu aby bylo jasné, že to funguje snad všude

3. 150 kB volného místa
    - 150 kB je 0.15 MB, je to málo, ale i tak je dobré vědět kolik to má

4. Na ram, cpu, nebo gpu to nemá žádné požadavky
    - Můžete to zkusit stusti i na bramboře, je to Python takže třeba...


### Jak kód funguje?
Vše se dozvíte ve souboru data/info.md, ale zde budou základní věci alespoň.
Vše potřebné si najdete, nebo mi napište.

1. Obecně fungování
    1. Fungování
        - Kód má všechny potřebné soubory ve stejné složce (podsložce) jako je kód na objednávání samotný.
        - Stačí spustit soubor *gui.py* a program vás navede co máte dělat.
        - Konkrétně o objednávání jídel se dozvíte níže.
    
    2. Setup
        - Jakmile jste spustili kód, měl by se vám zobrazit setup.
        - Zdali se vám program otevře do okna pro objednávání, znamená to že nejspíš byl setup vypnutý, pro více info přejděte na [sekci o debugování](#Debugging).
        - Zde je potřeba abyste zadali vaše údaje na stravu a pokračovali dále.
        - Jako další krok je potřeba abyste si nastavili Chat GPT, jenže s tímto jsem měl menší problémy a Ještě to nefunguje, takže můžete Nastavování tady přeskočit.
        - Po dokončení setupu by se měl kód otevřít na uživatelském rozhraní programu.

    3. Uživatelské rozhraní
        - Okno, které vidíte má několik kateorií:
            - Přehled
            - Nastavení
            - Chat GPT
            - Rozšířené možnosti
        - Přepínat mezi nimi můžete pomocí stisknutí tlčítka pro danou kategorii *Momentálně nefunguje pro Linuxová zařízení.
        - Dané kategorie si více rozebereme níže:
            1. Přehled <br>
                Přehled slouží k zobrazení aktivity u objednávání. Vidíte zde běh programu, celkem objednáno obědů a poslední objednávku.
                Jakmile kliknete na text s časem do příští objednávky, tak by se vám měl čas resetovat a nový pokus o obědnání by měl hned proběhnout.
                Více info v data/info.md.
            2. Nastavení <br>
                Je to nastavení, co byste čekali. Nastavte zde vše co potřebujete, upravte jméno, heslo**, vše potřebné.
                Po stistkutí uložit by vám mělo vyskočit oznámení, zdali chcete změny uplatnit už teď. Program si ze souboru na začátku načte pouze potřebné info pro start a zbytek si bere přímo ze souborů, které si znovu otevře, takže to minimálně ovlivní fungování a běh programu.
                Více věcí ohledně nastavování najdete v data/info.md.
                ** Při ukládání hesla máte na výbeř možnost šifrování hesla, slouží to pouze, aby při např ukázání souboru nebylo hned možné vidět heslo, protože klíč k dešifrování se nechází ve stejném souboru (případně bych chtěl do budoucna opravit)
            3. Chat GPT <br>
                Chat GPT momentálně nefunguje a není nutné zadávat cokoli s ním spojeného. Do budoucna bych to chtěl přepracovat, upravit aby to fungovalo.
                Zatím si můžete vyplnit jaká jídla máte a nemáte rádi, to se nestratí.
                Zde je zbytečné cokoli říkat, až s updatem, který opraví Chat GPT - více v data/info.md.
            4. Rozšířené možnosti <br>
                Naleznete zde pár věcí jak se dostat do programu, ne všechny ale fungují, jsou pouze experimentání a můžou i rozbít program.
                Radši bych nechal program ať si funguje jak je.
                Pro více info o rozšířených možnostech se dočete v [sekci pro vývojáře](#pro-vývojáře).
        - Program má i sekci bez GUI, tedy jen s konzolí.
        - Když okno zavřete, měla by se vám ona zmíněná sekce otevřít - na výběr teď máte ze tří možností:
            1. Zmáčknete enter
                - Po zmáčknutí entru by se vám mělo okno zpět otevřít.
                - Program objednává a funguje na pozadí i bez okna.
                - Více info o tomto v [sekci pro vývojáře](#pro-vývojáře).
            2. Napíšete "res" a zmáčknete enter
                - Tento příkaz restartuje kód.
                - Res oficiálně ukončí daný proces který probíhá a uloží potřebné věci - není doporučené kód ukončovat jakýmkoli jiným způsobem - a znovu kód spustí.
                - Pro více info se podívejte do sekce [jak s programem nezacházet](#jak-s-programem-nezacházet).
            3. Napíšete "exit" a zmáčknete enter
                - Tento příkaz Ukončí běh kódu.
                - Exit oficiálně ukončí daný Všechny potřebné procesy tak jak má a uloží potřebné inmformace.
                - Pro více info se podívejte do sekce [jak s programem nezacházet](#jak-s-programem-nezacházet).



        - Je možné, že když cokoliv nebude fungovat, že se více dozvíte v info.md, nebo v souboru debug.txt, případně mi napište.

    4. Objednávání jídel
        - Kód se každou stanovenou dobu přihlásí k vašemu školnímu účtu na stravě a pokusí se objednat stanovený oběd.
        - Všechny možné nastavení najdete v sekci Nastavení v programu, nebo ve souboru data/settings.json.
        - Chtěl jsem to ještě udělat, že to zůstane třeba den přihlášené, že se to nebude muset pokaždé přihlašovat, ale nevím jestli by to fungovalo.
        - Objednávnání trvá jen chvilku, počkejte pár sekund a mělo by to být.
        - Pozor: kód nespracovává chyby při objednávání moc dobře, takže když víte, že se něco pokazilo, tak zkontrolujte debug.txt


### Pro vývojáře
- Více sem přijde brzo
- Čekejte: Info o vláknech, Popsaný běh programu, další info


### Debugging
- Info k debugování.
- Tento seznam nemusí obsahovat vše, kdyžtak mi napište a já se to pokusím vyřešit
1. Debugování při startu:
    - Když vám nefunguje setup, nebo program nejde spustit.
    - Podrobněji v data/info.md.
    1. Setup
        - Když se vám kód při prvním spuštění nezapne do setup módu udělejte následující kroky:
            1. Otevřete soubor data/config.json
            2. V souboru data/config.json najďete sekci "data"
            3. V ní přepněte setup z *false* na *true*
            4. Uložte soubor a spusťte program znovu
        - Je možné, že nastala chyba při setupu, např. že se vám heslo nezašifruje, pak postupujte podle těchto kroků:
            1. Zkontrolujte debug.txt
            2. Podle infomací přejděte do data/info.md
            3. V sekci debugging by měla být odpověď
            4. Jestli nemáte řešení tam mi napište
        
    2. Problémy se spouštěním
        - Je možné, že program nelze sputit, tak zkontrolujte:
            1. Soubor data/debug.txt - v něm uvidíte důvod
            2. Jestli máte stažené všechny knihovny
                - Podívejte se do souboru gui.py a zkontorujte, zda-li jsou všehcny knihovny přístupné.
                - Příkazy níže napište do příkazového řádku vašeho počítače.
                - Jestli vám nějaká chybí, použijte příkaz `pip install <název knihovny>`
                - Aktualizujte knihovny pomocí příkazu `pip install --upgrade <název knihovny>`
                - Zkontrolujte danou knihovnu pomocí příkazu `pip show <název knihovny>`
                - Více info o pip najdete na stránkách [PyPi](https://pypi.org)
            3. Že je Python správně nainstalovan a případně další faktory, které mohou způsobovat chybu

2. Přepínání "scén"
    - Scény považuji možnosti jako je Nastavení, Chat GPT, Rozšířené Možnosti a přehled.
    - Je možné, že mezi scény nelze přepínat, s tím zatím nic neuděláte, to musím já opravit.
    - Na Linuxech to fungovat nemusí, když si najdete jak to opravit, můžete, ale časem to opravím oficiálně.

3. Další chyby
    - Jedna důležitá rada: vše najdete v data/info.md.
    - Jesli ne, tak mi napište, já s něčím přijdu.

4. Program bez GUI
    - Zda-li vám nefunguje kód zodpovědný za objednávání mimo GUI, můžete se to pokusit vyřešit nastavováním různých věcí, kód bych nechal tak jak je, protože mně to funguje.
    - V data/info.md je více info kdyby bylo potřeba.
    - Je možné, že nastane chyba, která shodí celý program, která může nastat kdykoli a kdekoli, ale když běží více vláken najednou, tak chyba v jednom z nich neukončí celý program, ostatní vlákan tomu brání. Více info v [sekci pro vývojáře](#pro-vývojáře).


### Jak s programem nezacházet
1. Vypínání a restartování:
    - Program má pro vypínání a restartování několik způsobů.
    - Je potřeba aby se uložily informace, které má program jen aktuálně a mohly by být potřeba při příštím zpuštění.
    1. Vypínání
        - Pro vypnutí udělejte následující kroky:
            1. Zvřete GUI okno
            2. Vepiště do konzole exit (nebo odejít)
            3. Stiskněte enter a chvíli počkejte
        - Jakýkoli jiný způsob by mohl ztratit nějaké důležité informace.
        - Ačkoli by to až tak moc nevadilo, je to spíše funkce do budoucna.
    2. Restartování
        - Program někdy potřebuje restartovat, tak je tu možnost jak to udělat rychleji.
        - Je zde pár způsobů, prvním z nich je:
            1. Zavřete GUI okno
            2. Vepište do konzole "res", nebo "restart"
            3. Potvrďte zmáčknutím entru
        - Další způsoby zde stále existují, ale není potřeba je znát.
    3. Další možnosti
        - Dřive byla možnost vstoupt do tzv. "cmd módu", jenže tato možnost je od verze 0.87 odebrána.
        - Stále je možné z kódu vyvolat funkci pro ukončení programu.

2. Správa vláken
    - Do tohoto se nechci moc motat, vše info o vláknech najdete v sekci [pro vývojáře](#pro-vývojáře), nebo v souboru data/info.md.
    - Pokud nemusíte, tak nechte program si určit jaká vlákna potřebuje použít sám.
    - Pokud se ale rozhodnete zkusit jak vlákna fungují, nedoporučujeme vlákno ukončit uprostřed nějakého většího procesu - mohlo by to vést ke chybám.
    - Dávejte si pozor, abyste nespustili 5. vlákno pokud nemusíte, můžou se pak otevřít 2 okna, chci to takhle nechat, protože občas se to hodí, ale někdy to může způsobit problémy.


### Další inforamce
1. Všeobecné poznámky:
    - Není doporučené kód ukončovat jakýmkoli jiným způsobem než zavřením GUI okna a vepsáním "exit" do konzole. Pro více info se podívejte do sekce [jak s programem nezacházet](#jak-s-programem-nezacházet).
    - Verze: cislo; A -> Alfa; a -> verze a; + -> nedokončená verze, rozšíření napsané verze, ale nedokončené; může být i třeba: 1.0Ba+
    - V souboru data/settings.json je sekce pro odesílání mailu když nastane daná situace, ale potřebuje to hodně práce s knihovnami pro maily a zároveň to má vysoké požadavky na mail, takže to snad ani přidávat nebudu.
    - Momentálně si program musíte aktualizovat sami z githubu, ale časem bych chtěl přidat klienta pro aktualizace
    - V souboru data/currentData.txt jsou uloženy inforamce jako: *kolik zbývá do další objednávky*, *poslední objednávka*, atd. - i když tam něco upravíte, program si určité věci přepíše zpět.