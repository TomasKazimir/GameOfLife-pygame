> Tomáš Kazimír\
> ZS 2024/202\
> NPRG030


# Uživatelská dokumentace

## Obsah
1. [Základní informace](#základní-informace)
2. [Požadavky](#požadavky)
3. [Spouštění](#spouštění)
4. [Pravidla hry](#pravidla-hry)
5. [Ovládání](#ovládání)

## Základní informace 
Tento projekt implementuje tzv. 
Game of Life, což je celulární automat vymyšlený matematikem Johnem Conwayem. Jedná se původně o hru bez hráče, což znamená, že její vývoj je určen jejím počátečním stavem bez dalšího vstupu. Tato implementace však umožnuje uživateli do vývoje hry zasahovat a měnit tak její průběh.

Program umožňuje uživateli následující:
- Spustit a zastavit simulaci.
- Nastavit rychlost simulace.
- Uložit a načíst stav mřížky.
- Resetovat hru - pravidlo i mřížku.
- Zabít všechny buňky.
- Vložit náhodně živé buňky.
- Upravovat pravidla hry.
- Nastavit velikost mřížky. #TODO

## Požadavky
- Python 3.12.7
- pygame (Ujistěte se, že je nainstalován pomocí `pip install pygame`)
- pyperclip (Ujistěte se, že je nainstalován pomocí `pip install pyperclip`)

## Spouštění
1. Naklonujte si repozitář nebo stáhněte soubory projektu.
2. Ujistěte se, že máte nainstalovaný Python a pygame.
3. Spusťte hlavní soubor:
    ```bash
    python main.py
    ```
   Následně se vám otevře okno s herním polem, kde můžete začít 'hrát'.

## Pravidla hry
Herní plochou hry je čtvercová mřížka, kde každá buňka může být živá nebo mrtvá. Hra funguje na principu celulárního automatu, kde každá buňka má 8 (případně i více) sousedů, 
jsou to buňky okolo ní. Pravidla hry jsou následující:
1. **Přežití**: Živá buňka s 2 nebo 3 živými sousedy přežije do další generace.
2. **Narození**: Mrtvá buňka s právě 3 živými sousedy se stane živou buňkou.
3. **Smrt**: Všechny ostatní buňky zemřou.

Tyto pravidla se dají postihnout následujícím zápisem:
```plaintext
        +--> oddělovače
        |
       / \
>>  R1/B3/S23  <<
    |  |  |
    |  |  +--> S: počet živých sousedů, kterými musí buňka disponovat, aby přežila
    |  +--> B: počet živých sousedů, kterými musí mrtvá buňka disponovat, aby se stala živou
    +--> R: rádius kolem dané buňky, který se počítá jako sousedství
```
Pokud bychom chtěli pozměnit pravidla hry, kde např. buňka přežije pouze se 2 živými sousedy, můžeme využít zápis:
```plaintext
>>  R1/B3/S2  <<
```
Nebo bychom chtěli uvažovat sousedství vzdálené 2 buňky (každá buňka tak má 24 sousedů místo původních osmi), můžeme využít zápis:
```plaintext
>>  R2/B3/S23  <<
```

## Ovládání
Po spuštění programu se vám otevře okno programu. Je rozděleno na dvě části:
1. **Herní pole/mřížka**:\
Zde se odehrává samotná hra.\
Buňky můžete vkládat kliknutím/podržením levého tlačítka myši a mazat kliknutím/podržením pravého tlačítka myši.
2. **Ovládací panel**:\
Umístněn v pravé části, nachází se zde odzhora dolů:
   1. Vstupní pole s názvem _**Enter rule**_, kde můžete zadat pravidla hry ve formátu popsaném výše.\
   Po zadání pravidel stiskněte klávesu **Enter** pro jejich aplikaci.
   2. Informativní text:\
   `Active rule` - informace o aktuálním pravidlu. Pokud zadáte do vstupního pole neplatný formát pravidla, zobrazí se zde chybová hláška.\
   `Simulation speed` - Zobrazuje aktuální rychlost simulace. Pomocí **šipek nahoru a dolů** můžete rychlost simulace měnit.\
   `Running/Paused` - Informace o tom, zda simulace běží nebo je pozastavena. Lze měnit stisknutím **mezerníku**. Pokud je simulace pozastavena, můžete manuálně posunout simulaci o jednu generaci stisknutím **pravé šipky**.
   3. Vstupní pole s názvem _**Save current board as**_, kde můžete momentální stav hry uložit tak, že zadáte název, pod kterým chcete stav hry uložit, a stisknete **Enter**.\
   Hra se uloží ve složce `saved_boards` do souboru s příponou .txt.\
   Na prvním řádku je uvedeno pravidlo hry, na druhém řádku je uvedena velikost mřížky a na dalších řádcích je uložen stav mřížky - `.` symbolizuje mrvtou a `o` živou buňku.

   3. Tlačítka, kterými můžete ovládat hru:\
      _**Load board...**_ otevře dialogové okno, kde můžete vybrat soubor s uloženým stavem mřížky.\
      _**Reset game**_ nastaví hru do počátečního stavu (načte `.default_board.txt` ze složky `saved_boards`).\
      _**Insert noise**_ vloží náhodně živé buňky do celé mřížky.\
      _**Clear board**_ smaže všechny buňky.

Program lze ukončit stisknutím **křížku** v pravém horním rohu okna.




