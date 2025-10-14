def vygeneruj_dvojice_slovnik(znaky, dvojhlasky):
    slovnik = {} 
    for a in znaky:
        for b in znaky:
            dvojice = a + b
            if dvojice in dvojhlasky:
                continue
            vystup = f"{a}\\u200B{b}"  # zero-width space
            slovnik[dvojice] = vystup
    return slovnik

def uloz_slovnik_do_souboru(slovnik, nazev_souboru):
    with open(nazev_souboru, "w", encoding="utf-8") as f:
        f.write("sprezky_samohlasek = {\n")
        for k, v in slovnik.items():
            f.write(f"    '{k}': '{v}',\n")
        f.write("}\n")

# --- Hlavní část ---
if __name__ == "__main__":
    vstupni_znaky = "aeiouyáéíóúůýäěöüAEIOUÁÉÍÓÚŮĚÄÖÜ"  # Změň dle potřeby
    #vstupni_znaky = "aeiou"  # Změň dle potřeby
    dvojhlasky = ['au', 'ou', 'eu','ai','ei','oi','Au', 'Ou', 'Eu','Ai','Ei','Oi','AU', 'OU', 'EU','AI','EI','OI']  # Výjimky, které se vynechají
    slovnik = vygeneruj_dvojice_slovnik(vstupni_znaky, dvojhlasky)
##    vycet=['b','c','č','d','ď','f','g','h','j','k','l','m','n','ň','p','q','r','s','š','t','ť','v','w','x','z','ž']
##    for k in vycet:
##        dvojice= k+'ú'
##        slovnik[dvojice]=f"{k}\\u200Bú"
        
    uloz_slovnik_do_souboru(slovnik, "sprezky_samohlasek_map.py")
