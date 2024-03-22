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
Vše potřebné si najdete nebo mi napište.

1. Obecně fungování
    1. Fungování
        - Kód má všechny potřebné soubory ve stejné složce (podsložce) jako je kód na objednávání samotný.
        - Stačí spustit soubor *gui.py* a program vás navede co máte dělat.
        - Konkrétně o objednávání jídel se dozvíte níže.
    
    2. Setup
        - Jakmile jste spustili kód, měl by se vám zobrazit setup.
        - Zdali se vám program otevře do okna pro objednávání, znamená to že nejspíš byl setup vypnutý, pro více info přejděte na [sekci o debugování](#Debuging).
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
            1. Přehled
                Přehled slouží k zobrazení aktivity u objednávání. Vidíte zde běh programu, celkem objednáno obědů a poslední objednávku.
                Jakmile kliknete na text s časem do příští objednávky, tak by se vám měl čas resetovat a nový pokus o obědnání by měl hned proběhnout.
                Více info v data/info.md.
            2. Nastavení
                Je to nastavení, co byste čekali. Nastavte zde vše co potřebujete, upravte jméno, heslo*, vše potřebné.
                Po stistkutí uložit by vám mělo vyskočit oznámení, zdali chcete změny uplatnit už teď. Program si ze souboru na začátku načte pouze potřebné info pro start a zbytek si bere přímo ze souborů, které si otevře, takže to minimálně ovlivní fungování a běh programu.
                Více věcí ohledně nastavování najdete v data/info.md.
                * Při ukládání hesla máte na výbeř možnost šifrování hesla, slouží to pouze, aby při např ukázání souboru nebylo hned možné vidět heslo, protože klíč k dešifrování se nechází ve stejném souboru (případně bych chtěl do budoucna opravit)
            3. Chat GPT
                Chat GPT momentálně nefunguje a není nutné zadávat cokoli s ním spojeného. Do budoucna bych to chtěl přepracovat upravit aby to fungovalo.
                Zatím si můžete vyplnit jaká jídla máte a nemáte rádi, to se nestratí.
                Zde je zbytečné cokoli říkat, až s updatem, který opraví Chat GPT - více v data/info.md
            4. Rozšířené možnosti
                Naleznete zde pár věcí jak se dostat do programu, ne všechny ale fungují, jsou pouze experimentání a můžou i rozbít program.
                Radši bych nechal program ať si funguje jak je.
                Pro více info o rozšířených možnostech se dočete v [sekci pro vývojáře](#pro-vývojáře).
        - Program má i sekci bez GUI, tedy jen s konzolí.
        - Když okno zavřete, měla by se vám ona zmíněná sekce otevřít, navýběr teď máte ze dvou možností:
            1. Zmáčknete enter
                - Po zmáčknutí entru by se vám mělo okno zpět otevřít.
                - Program objednává a funguje na pozadí i bez okna.
                - Více info o tomto v [sekci pro vývojáře](#pro-vývojáře).
            2. Napíšete "res" a zmáčknete enter
                - Tento příkaz restartuje kód.
                - Res oficiálně ukončí daný proces který probíhá a uloží potřebné věci - není doporučené kód ukončovat jakýmkoli jiným způsobem - a znovu kód spustí.
                - Pro více info se podívejte do sekce [jak s programem nezacházet](#jak-s-programem-nezacházet).


        - Je možné, že když cokoliv nebude fungovat, že se více dozvíte v info.md, nebo v souboru debug.txt, případně mi napište.


### Pro vývojáře
 - Info o vláknech atd.


### Debuging
- setup, přepínbání scén, další chyby, info v souoru curr, bez GUI


### Jak s programem nezacházet
1. Vypínání a restartování:
    - Program má pro vypínání a restartování několik způsobů.
    - Je potřeba aby se uložily inforame, které má program jen aktuálně a mohly by být potřeba při příštím zpuštění.
    1. Vypínání
        - Pro vypnutí udělejte následující kroky:
            1. Zvřete GUI okno
            2. Vepiště do konzole exit (nebo odejít)
            3. Stiskněte enter a chvíli počkejte
        - Jakýkoli jiný způsob by mohl stratit nějaké důležité informace.
        - Ačkoli by to až tak moc nevadilo, je to spíš funkce do budoucna.
    2. Restartování
        - Program někdy potřebuje restartovat, tak je tu možnost jak to udělat rychleji.
        - Je zde pár způsobů:, prvním z nich je:
            1. Zavřete GUI okno
            2. Vepište do konzole "res", nebo "restart"
            3. Potvrďte zmáčknutím entru
        - Další způsoby zde stále existují, ale není potřeba je znát.
    3. Další způsoby
        - Dřive byla možnost vstoupt do tzv. "cmd módu", jenže tato možnost je od verze 0.87 odebrána.
        - Stále je možné z kódu vyvolat funkci pro ukončení programu.

2. Správa vláken
    - Do tohoto se nechci moc motat, vše najdete v sekci [jak s programem nezacházet](#jak-s-programem-nezacházet), nebo v souboru data/info.md.
    - Pokud nemusíte, tak nechte program si určit jaká vlákna potřebuje použít sám.
    - Pokud se ale rozhodnete zkusit jak vlákna fungují, nedoporučujeme vlákno ukončit uprostřed nějakého většího procesu - mohlo by to vést ke chybám
    - Dávejte si pozor abyste nestartovali 5 vlákno pokud nemusíte, můžou se pak otevřít 2 okna, chci to takhle nechat, protože občas se to hodí, ale někdy to může způsobit problémy.


### Další inforamce
1. Všeobecné poznámky:
    - Není doporučené kód ukončovat jakýmkoli jiným způsobem než zavřením GUI okna a vepsáním "exit" do konzole. Pro více info se podívejte do sekce [jak s programem nezacházet](#jak-s-programem-nezacházet).
    - Jak fungují verze
