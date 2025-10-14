def unicode_to_latex(unicode_string):
    def char_to_latex(c):
        return f'\\char"{ord(c):04X}'

    result = []
    i = 0
    while i < len(unicode_string):
        c = unicode_string[i]

        # Speciální případ pro nový řádek
        if c == '\n':
            result.append('\\\\')  # LaTeX nový řádek
            i += 1
            continue

        # Zpracuj blok velkého písmena
        if c == '©':
            i += 1
            block = ''
            while i < len(unicode_string) and unicode_string[i] != '®':
                block += unicode_string[i]
                i += 1
            if i == len(unicode_string):
                raise ValueError("Chybí ukončovací znak ® pro blok 'velké_písmeno'")
            i += 1  # přeskoč '®'

            if '½' in block:
                part1, part2 = block.split('½', 1)
                latex_part1 = ''.join(char_to_latex(ch) for ch in part1)
                latex_part2 = ''.join(char_to_latex(ch) for ch in part2)
                latex_block = f'{{\\color{{red}}\\overlaychars{{{latex_part1}}}{{-3pt}}{{{latex_part2}}}}}'
            else:
                latex_block = '{\\color{red}' + ''.join(char_to_latex(ch) for ch in block) + '}'
            result.append(latex_block)
        else:
            result.append(char_to_latex(c))
            i += 1
    return ''.join(result)


vstup = "dnes je\n©1½p®\na ne ©s½3®obota."
print(unicode_to_latex(vstup))
