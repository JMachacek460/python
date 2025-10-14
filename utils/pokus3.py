import subprocess
import os
import re

def rozdel_slabiky_tex(slovo):
    tex_source = rf"""
\documentclass{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage[czech]{{babel}}
\AtBeginDocument{{\shorthandoff{{"-}}}} % vypne české zkratky
\begin{{document}}
\showhyphens{{{slovo}}}
\end{{document}}
"""
    filename = "hyphen_test"

    with open(f"{filename}.tex", "w", encoding="utf-8") as f:
        f.write(tex_source)

    subprocess.run(["lualatex", "-interaction=nonstopmode", f"{filename}.tex"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    hyphenated = None

    def vycistit_radek(line):
        line = re.sub(r'\\T1\/[^\s]+', '', line)
        return line.strip()

    with open(f"{filename}.log", "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "[]" in line and '-' in line:
                clean_line = vycistit_radek(line)
                clean_line = re.sub(r'^\[\]\s*', '', clean_line)
                hyphenated = clean_line
                break

    for ext in [".aux", ".log", ".tex", ".pdf"]:
        try:
            os.remove(f"{filename}{ext}")
        except FileNotFoundError:
            pass

    if hyphenated:
        return hyphenated.split('-')
    else:
        return [slovo]


def rozdel_vetu_na_slabiky_tex(veta):
    vysledek = []
    for slovo in veta.split():
        slabiky = rozdel_slabiky_tex(slovo)
        vysledek.extend(slabiky + [' '])
    vysledek = vysledek[:-1]  # odstraní poslední mezeru
    return '\u200B'.join(vysledek)

# ✅ TEST
vtupni_text2 = rozdel_vetu_na_slabiky_tex("trojúhelník bezoký lučišník")
print(vtupni_text2)
