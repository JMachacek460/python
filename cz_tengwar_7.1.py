# cz_tengwar.py

import subprocess
import os
import re
from slovniky.cestina_tengvar_map import cestina_tengvar  # ⬅ přidáno
from slovniky.sprezky_samohlasek_map import sprezky_samohlasek  # ⬅ přidáno

####################################################
def rozdel_slovnik_slabik_tex(seznam_slov):
    tex_source = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[czech]{babel}
\AtBeginDocument{\shorthandoff{"-}}
\begin{document}
""" + '\n'.join([f"\\showhyphens{{{slovo}}}" for slovo in seznam_slov]) + "\n\\end{document}"

    filename = "hyphen_batch"

    with open(f"{filename}.tex", "w", encoding="utf-8") as f:
        f.write(tex_source)

    subprocess.run(["lualatex", "-interaction=nonstopmode", f"{filename}.tex"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    vysledky = {}
    current_word = None

    with open(f"{filename}.log", "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = re.search(r'\\T1/.*?\[\](.*?-.*)', line)
            if match:
                hyph = match.group(1).strip()
                hyph = re.sub(r'\\T1/[^\s]+', '', hyph).strip()
                word = hyph.replace('-', '')
                slabiky = hyph.split('-')
                vysledky[word] = slabiky

    for ext in [".aux", ".log", ".tex", ".pdf"]:
        try:
            os.remove(f"{filename}{ext}")
        except FileNotFoundError:
            pass

    return vysledky
def rozdel_vetu_na_slabiky_tex(veta):
    slova = re.findall(r'\w+', veta)
    unikatni_slova = sorted(set(slova))
    slovnik_slabik = rozdel_slovnik_slabik_tex(unikatni_slova)

    vysledek = []
    for slovo in veta.split():
        ciste = re.sub(r'\W+', '', slovo)
        if ciste in slovnik_slabik:
            slabiky = slovnik_slabik[ciste]
        else:
            slabiky = [slovo]
        vysledek.extend(slabiky + [' '])
    vysledek = vysledek[:-1]
    return '\u200B'.join(vysledek)



####################################################
##def rozdel_slabiky_tex(slovo):
##    tex_source = rf"""
##\documentclass{{article}}
##\usepackage[utf8]{{inputenc}}
##\usepackage[T1]{{fontenc}}
##\usepackage[czech]{{babel}}
##\AtBeginDocument{{\shorthandoff{{"-}}}} % vypne české zkratky
##\begin{{document}}
##\showhyphens{{{slovo}}}
##\end{{document}}
##"""
##    filename = "hyphen_test"
##
##    with open(f"{filename}.tex", "w", encoding="utf-8") as f:
##        f.write(tex_source)
##
##    subprocess.run(["lualatex", "-interaction=nonstopmode", f"{filename}.tex"],
##                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
##
##    hyphenated = None
##
##    def vycistit_radek(line):
##        line = re.sub(r'\\T1\/[^\s]+', '', line)
##        return line.strip()
##
##    with open(f"{filename}.log", "r", encoding="utf-8", errors="ignore") as f:
##        for line in f:
##            if "[]" in line and '-' in line:
##                clean_line = vycistit_radek(line)
##                clean_line = re.sub(r'^\[\]\s*', '', clean_line)
##                hyphenated = clean_line
##                break
##
##    for ext in [".aux", ".log", ".tex", ".pdf"]:
##        try:
##            os.remove(f"{filename}{ext}")
##        except FileNotFoundError:
##            pass
##
##    if hyphenated:
##        return hyphenated.split('-')
##    else:
##        return [slovo]
##
##
##def rozdel_vetu_na_slabiky_tex(veta):
##    vysledek = []
##    for slovo in veta.split():
##        slabiky = rozdel_slabiky_tex(slovo)
##        vysledek.extend(slabiky + [' '])
##    vysledek = vysledek[:-1]  # odstraní poslední mezeru
##    return '\u200B'.join(vysledek)
##
##
#####################################################




# ░░░ 1. Převod běžného textu na Unicode řetězec
def text_to_unicode(text, mapping, verbose=True):
    result = []
    unknown = set()
    i = 0

    while i < len(text):
        matched = False
        for l in range(3, 0, -1):
            chunk = text[i:i + l]
            if chunk in mapping:
                result.extend(mapping[chunk])
                i += l
                matched = True
                break
        if not matched:
            unknown.add(text[i])
            result.append(ord(text[i]))  # nebo např. 0xFFFD pro �
            i += 1

    if verbose and unknown:
        print("⚠️  Upozornění: některé znaky nejsou ve slovníku cestina_tengvar:")
        for ch in sorted(unknown):
            print(f" - '{ch}' (U+{ord(ch):04X})")

    return ''.join(chr(cp) for cp in result)


def replace_newlines_with_backslash(text: str) -> str:
    # Nejprve sjednotíme CR+LF na LF (většinou už je to tak po načtení)
    text = text.replace('\r\n', '\n')
    # Pak nahradíme všechny LF za dvojité zpětné lomítko
    return text.replace('\n', r'\\')

def dopln_samohlasky_do_velkych_pismen(text, samohlasky):
    import regex as re  # Lepší práce s Unicode než klasický `re`

    # Nastavení rovnocenných počátečních znaků
    start_markers = {'©', 'ª','«'}
    end_marker = '®'

    # Převedeme text na seznam znaků s ohledem na celé Unicode znaky
    chars = list(text)
    result = []
    i = 0

    while i < len(chars):
        if chars[i] in start_markers:
            start_char = chars[i]
            start = i
            i += 1
            content = ''
            while i < len(chars) and chars[i] != end_marker:
                content += chars[i]
                i += 1
            if i < len(chars) and chars[i] == end_marker:
                i += 1  # Přeskočíme '®'

                # Oddělíme části podle '½'
                parts = content.split('½')
                first = parts[0]
                second = parts[1] if len(parts) > 1 else ''

                # Najdeme samohlásky za '®'
                vowels = ''
                while i < len(chars) and chars[i] in samohlasky:
                    vowels += chars[i]
                    i += 1

                # Nahradíme '¹' podle přítomnosti samohlásek
                if vowels:
                    if '¹' in first:
                        first = first.replace('¹', vowels)
                        second = second.replace('¹', '')  # pro jistotu
                    elif '¹' in second:
                        second = second.replace('¹', vowels)
                        first = first.replace('¹', '')
                    else:
                        pass  # není kam vložit – ignorujeme
                else:
                    # jen odstraníme '¹'
                    first = first.replace('¹', '')
                    second = second.replace('¹', '')

                result.append(start_char + first + ('½' + second if second else '') + end_marker)
            else:
                # pokud chybí koncová značka, připojíme vše a pokračujeme
                result.append(start_char + content)
        else:
            result.append(chars[i])
            i += 1
    return ''.join(result)

def unicode_to_latex(unicode_string, velikost='Huge'):
    ## podporovane velikosti normalsize Large Huge
    def char_to_latex(c):
        return f'\\char"{ord(c):04X}'
    # kontrola a případné nastavení výchozí hodnoty
    if velikost not in ['normalsize', 'Large', 'Huge']:
        velikost = 'Huge'

    result = []
    result.append('\\')
    result.append(velikost)
    
    i = 0
    while i < len(unicode_string):
        c = unicode_string[i]

        # Speciální případ pro nový řádek
        if c == '\n':
            result.append('\\\\')  # LaTeX nový řádek
            i += 1
            continue

        # Zpracuj blok velkého písmena
        if c in {'©', 'ª','«'}:
            start_marker = c
            i += 1
            block = ''
            while i < len(unicode_string) and unicode_string[i] != '®':
                block += unicode_string[i]
                i += 1
            if i == len(unicode_string):
                raise ValueError("Chybí ukončovací znak ® pro blok 'velké_písmeno'")
            i += 1  # přeskoč '®'

            # Nastav překrytí podle typu markeru
            if velikost == 'normalsize':
                if start_marker == '©':
                    overlay_shift = '-1.5pt'
                elif start_marker == 'ª':
                    overlay_shift = '-5pt'
                elif start_marker == '«':
                    overlay_shift = '-7.5pt'
                else:
                    overlay_shift = '-3pt'  # výchozí hodnota (pro jistotu)
            elif velikost == 'Large':
                if start_marker == '©':
                    overlay_shift = '-2pt'
                elif start_marker == 'ª':
                    overlay_shift = '-8pt'
                elif start_marker == '«':
                    overlay_shift = '-11pt'
                else:
                    overlay_shift = '-3pt'  # výchozí hodnota (pro jistotu)
            else:
               # Huge
                if start_marker == '©':
                    overlay_shift = '-3pt'
                elif start_marker == 'ª':
                    overlay_shift = '-11pt'
                elif start_marker == '«':
                    overlay_shift = '-16pt'
                else:
                    overlay_shift = '-3pt'  # výchozí hodnota (pro jistotu)

            if '½' in block:
                part1, part2 = block.split('½', 1)
                latex_part1 = ''.join(char_to_latex(ch) for ch in part1)
                latex_part2 = ''.join(char_to_latex(ch) for ch in part2)
                latex_block = f'{{\\color{{red}}\\overlaychars{{{latex_part1}}}{{{overlay_shift}}}{{{latex_part2}}}}}'
            else:
                latex_block = '{\\color{red}' + ''.join(char_to_latex(ch) for ch in block) + '}'
            result.append(latex_block)
        else:
            result.append(char_to_latex(c))
            i += 1
    return ''.join(result)


# 3. Vstupní text a zpracování
###########################################
# na začátek každého řádku přida znak \u200B abych moh detekovat samohlasky na začátku řádku
with open("vstup.txt", "r", encoding="utf-8") as f:
    vstupni_text1 = ''.join('\u200B' + radek for radek in f)

upraveny_text=replace_newlines_with_backslash(vstupni_text1)
upraveny_text=upraveny_text.replace('\t', r'')
upraveny_text=upraveny_text.replace('#', r'\\')



vstupni_text1=vstupni_text1.replace('(','(\u200B')
vstupni_text1=vstupni_text1.replace('[','(\u200B')
vstupni_text1=vstupni_text1.replace('\t','\u200B')  #tabulátor je nucené rozdělení slova na slabiky
vstupni_text1=vstupni_text1.replace('\n',' xcx ')   #konce odstavce
vstupni_text1=vstupni_text1.replace('#',' xbx ')    # # je konec řadku bez konce odstavce
vstupni_text1=vstupni_text1.replace('-','\u2013')    # # je konec řadku bez konce odstavce
#print(ascii(vstupni_text1))

vstupni_text2 = rozdel_vetu_na_slabiky_tex(vstupni_text1)
#print(ascii(vstupni_text2))
vstupni_text2=vstupni_text2.replace(' \u200bxcx\u200b \u200b','\\') #konce odstavce
vstupni_text2=vstupni_text2.replace(' \u200bxcx','\\') #konec odstavce na konci dokumentu
 
vstupni_text2=vstupni_text2.replace(' \u200bxbx\u200b \u200b','#')  # # je konec řadku bez konce odstavce
vstupni_text2=vstupni_text2.replace(' \u200bxbx','#')  # # je konec řadku bez konce odstavce na konci dokumentu
#print(ascii(vstupni_text2))

# Nahradit dve samohlasky za sebou např "iu" za "i​\u200Bu"  evangelium

for sprezka, nahrazeni in sprezky_samohlasek.items():
    vstupni_text2 = vstupni_text2.replace(sprezka, nahrazeni)
#

unicode_string = text_to_unicode(vstupni_text2, cestina_tengvar)
#print(unicode_string)

#####################################################################

tengwar_samohlasky = ('\uE040', #a
                      '\uE046', #e
                      '\uE044', #i
                      '\uE045', #y
                      '\uE04A', #o
                      '\uE04C', #u
                      '\uE041', #ä
                      '\uE04B', #ö
                      '\uE04D', #ü
                      '\uE047', #ě
                      ) 

unicode_string_doplneny = dopln_samohlasky_do_velkych_pismen(unicode_string, tengwar_samohlasky)

## podporovane velikosti 'normalsize' 'Large' 'Huge'
latex_rendered=unicode_to_latex(unicode_string_doplneny,'Large')


#print(latex_rendered)
# nahrazuje mezery mezi slovy za mbox
for space_code in ['\\char"0020', '\\char"00A0']:
    latex_rendered = latex_rendered.replace(space_code, ' \\mbox{ } ')

#latex_rendered = latex_rendered.replace('\\char"200B', '')


#print(latex_rendered)


#######################################################################
# LaTeX šablona


# načtení šablony
with open("template.tex", "r", encoding="utf-8") as f:
    tex_template = f.read()

tex_code = tex_template.format(upraveny_text=upraveny_text, latex_rendered=latex_rendered)

###########################################################

def generate_pdf(tex_code, output_name="tengwar_output"):
    tex_filename = f"{output_name}.tex"
    with open(tex_filename, "w", encoding="utf-8") as f:
        f.write(tex_code)
    try:
        subprocess.run(["xelatex", "-interaction=nonstopmode", tex_filename], check=True)
        print(f"✅ PDF vygenerován: {output_name}.pdf")
    except subprocess.CalledProcessError as e:
        print("❌ Chyba při kompilaci XeLaTeX:", e)
    for ext in ["aux", "log"]:
        try:
            os.remove(f"{output_name}.{ext}")
        except FileNotFoundError:
            pass

###########################################################        
# ▶️ Spuštění
generate_pdf(tex_code)

