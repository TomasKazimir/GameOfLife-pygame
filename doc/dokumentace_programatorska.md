> Tomáš Kazimír\
> ZS 2024/202\
> NPRG030


# Programátorská dokumentace

## Struktura projektu
Projekt je rozdělen do několika souborů, které se starají o různé části programu. Následuje stručný popis jednotlivých souborů:
- main.py: Vstupní bod programu. Inicializuje objekt hry a spouští hlavní smyčku.
- game.py: Obsahuje třídu Game, která zajišťuje herní logiku a vykreslování. Hlavní třída programu.
- gui/: Adresář obsahující třídy a komponenty související s grafickým uživatelským rozhraním.
  - base/: Adresář obsahuje základní třídy pro GUI prvky.
    - gui_element.py: Obsahuje třídu GUIElement pro základní vlastnosti GUI prvků. 
    - gui_element_setup.py: Obsahuje třídu GUIElementSetup pro nastavení GUI prvků.
    - button.py: Obsahuje třídu Button pro tlačítka.
    - input_box.py: Obsahuje třídu InputBox pro vstupní pole.
    - label.py: Obsahuje třídu Label pro textové popisky.
  - clear_button.py: Obsahuje třídu ClearButton pro tlačítko, které smaže všechny buňky.
  - load_button.py: Obsahuje třídu LoadButton pro tlačítko pro načtení stavu mřížky ze souboru.
  - noise_button.py: Obsahuje třídu NoiseButton pro tlačítko, které vloží náhodně živé buňky.
  - reset_button.py: Obsahuje třídu ResetButton pro tlačítko, které resetuje pravidla a mřížku.
  - rule_inputbox.py: Obsahuje třídu RuleInputBox pro vstupní pole pro zadání pravidel.
  - save_inputbox.py: Obsahuje třídu SaveInputBox pro vstupní pole pro zadání názvu souboru pro uložení.
- load.py: Obsahuje funkce pro načítání uložených stavů mřížky ze souboru.
- generation.py: Obsahuje metodu pro výpočet nové generace buněk.
- utils.py: Obsahuje pomocné funkce pro validaci pravidel a parsování pravidel.
- doc/: Adresář obsahující dokumentaci.
  - dokumentace_programatorska.md: Programátorská dokumentace (tento soubor).
  - dokumentace_uzivatelska.md: Uživatelská dokumentace.

## Pygame

Pro vykreslování grafického uživatelského rozhraní a herní plochy je použita knihovna Pygame.\
Pygame je knihovna pro tvorbu her v Pythonu, která poskytuje jednoduché rozhraní pro práci s grafikou, zvukem a vstupem.\
Uživatelské vstupy jako kliknutí myší a stisknutí kláves jsou zpracovány pomocí Pygame eventů.\
Stejně tak je pomocí Pygame vykreslována herní plocha a grafické prvky.

V retrospektivě by bylo možné použít knihovnu Tkinter pro tvorbu GUI, kde jsou GUI prvky jako tlačítka, vstupní pole a popisky součástí knihovny.\
Zvolil jsem Pygame, protože jsem chtěl vyzkoušet práci s knihovnou, která je určena pro tvorbu her.\
Zároveň jsem si chtěl vyzkoušet naimplementovat GUI prvky sám, což bylo pro mě zajímavé a poučné.

## Hlavní součásti programu

Centrální metodou programu je metoda `loop` třídy `Game` (soubor `game.py`).\
Ta obsahuje hlavní smyčku programu, která se stará o následující:
- Zpracování událostí (uživatelského vstupu) pomocí Pygame eventů.
- Vygenerování nové generace buněk.
- Vykreslení herní plochy a GUI prvků.

### Zpracování událostí
Zpracování událostí je implementováno v metodě `handle_events`.\
Metoda zpracovává události pomocí Pygame eventů.\


### Generování herní plochy
Hlavní myšlenkou hry je celulární automat, kde každá buňka může být živá nebo mrtvá. Hra se řídí pravidly, které určují, zda buňka přežije, zemře nebo se narodí. Pravidla hry jsou definována ve formátu `R1/B3/S23`, kde:
- R: Rádius kolem dané buňky, který se počítá jako sousedství.
- B: Počet živých sousedů, kterými musí mrtvá buňka disponovat, aby se stala živou.
- S: Počet živých sousedů, kterými musí buňka disponovat, aby přežila.
- /: Slouží k oddělení jednotlivých částí pravidel.

Buňky a jejich životní prostor jsou reprezentovány 2D seznamem integerů - atribut `board` třídy `Game`, kde 1 značí živou buňku a 0 mrtvou buňku.\
Pokud je simulace spuštěna, každá generace je vypočtena pomocí metody `get_next_generation` (soubor `generation.py`).\
Tato metoda bere jako vstupní parametr 2D seznam integerů - aktuální stav mřížky, a pravidlo, podle kterého se má vypočítat nová generace buněk.\
Pravidlo je předáno jako slovník, kde klíče jsou `R`, `B` a `S` a hodnoty jsou seznamy integerů.\
V okolí kolem každé buňky (velikost okolí udává pravidlo pod klíčem `R`. Např pro hodnotu 1 jde o čtvercovou plochu velikosti 3*3 se středem v dané buňce) se počítají živé buňky - sousedi, jejich počet se uloží do proměnné `num_of_live_neighs`.\
Pokud je buňka živá, zkontroluje se, zda má dostatečný počet živých sousedů (v pravidle pod klíčem `S`), aby přežila. Pokud ne, buňka zemře.\
Pokud je buňka mrtvá, zkontroluje se, zda má dostatečný počet živých sousedů (v pravidle pod klíčem `B`), aby se narodila. Pokud ano, buňka se stane živou.
Vytváří se tak nový 2D seznam integerů, který reprezentuje novou generaci buněk - ten se vrátí jako výstup metody.

### Vykreslení herní plochy
Nejprve se vykreslí herní plocha - buňky.
 - Každá buňka je reprezentována čtvercem, kde živá buňka je vykreslena jako barevný čtverec a mrtvá buňka se nevykresluje.\
 - Vykreslení probíhá pomocí metody `draw_cells` třídy `Game`.


Následně se vykreslí GUI prvky - tlačítka, vstupní pole a popisky.
 - Vykreslení probíhá pomocí metody `draw_gui` třídy `Game`.
 - Každý GUI prvek má svou vlastní metodu `draw` pro vykreslení, která je volána v metodě `draw_gui`.

### Grafické uživatelské rozhraní
Inicializace GUI prvků probíhá v konstruktoru třídy `Game`.
Datová třída GUIElementSetup je zde použita pro pohodlné nastavení vlastností GUI prvků jako je jejich pozice, velikost nebo a text.

 - GUI prvky jsou reprezentovány třídami v adresáři `gui/`.
 - Každý GUI prvek je reprezentován třídou, která dědí od třídy `GUIElement` (soubor `gui_element.py`).
 - Třída `GUIElement` obsahuje metody pro vykreslení, aktualizaci a zpracování událostí GUI prvku.
 - Každý GUI prvek má své vlastní metody, které např. u tlačítek zajišťují jejich specifické chování (např. načtení souboru, smazání buněk atd.).


## Zamyšlení nad implementací
Pracovat s Pygame bylo zábavné. Implementace GUI prvků byla náročnější, než jsem očekával, a zabrala mi více času, než jsem plánoval.\
Samotná herní logika byla relativně jednoduchá, ale bylo důležité správně implementovat pravidla hry a generování nových generací buněk.\
Výzvou bylo také správně implementovat zpracování uživatelského vstupu - 
například vstupní pole (RuleInputBox) pro zadání pravidel hry, kde bylo nutné zajistit validaci a parsování pravidel. Zároveň pro třídu InputBox jsem musel implementovat pohyblivý kurzor, vkládání pomocí ctrl+v, funkci backspacu atd.





