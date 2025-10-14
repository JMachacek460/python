def dopln_samohlasky_do_velkych_pismen(text, samohlasky):
    result = []
    i = 0
    while i < len(text):
        if text[i] == '©':
            start = i
            i += 1
            content = ''
            while i < len(text) and text[i] != '®':
                content += text[i]
                i += 1
            if i < len(text) and text[i] == '®':
                i += 1  # Přeskočíme '®'

                # Oddělíme části podle '½'
                parts = content.split('½')
                first = parts[0]
                second = parts[1] if len(parts) > 1 else ''

                # Najdeme samohlásky za '®'
                vowels = ''
                while i < len(text) and text[i] in samohlasky:
                    vowels += text[i]
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
                        # není kam vložit – ignorujeme
                        pass
                else:
                    # jen odstraníme '¹'
                    first = first.replace('¹', '')
                    second = second.replace('¹', '')

                result.append('©' + first + ('½' + second if second else '') + '®')
            else:
                # pokud chybí koncová značka, připojíme vše a pokračujeme
                result.append('©' + content)
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)



samohlasky = ('a', 'i', 'o', '\u0xE040', '\u0065')
vstup = "dnes je ©1¹½p®aondeli a ne ©s¹½3®obota tyto ©n¹®eedele."
vystup = dopln_samohlasky_do_velkych_pismen(vstup, samohlasky)
print(vystup)
