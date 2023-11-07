#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pykakasi
from nltk.tokenize import SyllableTokenizer

vocali = "aàeèéiìoòuùy"
sonority_hierarchy = [
               vocali,  # vocali.
               "lmnrw",        # consonanti nasali
               "zvsf",         # consonanti fricative
               "bcdgtkpqxhj,.; ",  # stops.
           ]


syllabe_tokenizer = SyllableTokenizer(lang="ita",
                                      sonority_hierarchy=sonority_hierarchy)
kks = pykakasi.kakasi()


def get_conversion_table(katakana):
    conversion_table = dict(zip(map(katakana2acii, katakana), katakana))    
    conversion_table['fa'] = conversion_table['fu'] + conversion_table['a']
    conversion_table['fe'] = conversion_table['fu'] + conversion_table['e']
    conversion_table['du'] = conversion_table['do']
    conversion_table['ce'] = conversion_table['chi'] + conversion_table['e']
    return conversion_table

def katakana2acii(kana):
    return kks.convert(kana)[0]['passport']

def ascii2katakana(syllabe):
    return conversion_table[syllabe.lower()]
  

def convert2katakana(text):
    text = (text.replace('ss', 's')
                .replace('tt', 't')
                .replace('ll', 'l')
                .replace('pp', 'p')
                .replace('rr', 'r'))
    syllabes = syllabe_tokenizer.tokenize(text.lower())
    
    output_text = []
    for syllabe in syllabes:
        syllabe = syllabe.replace('l', 'r')
        if (syllabe.startswith('ch') or syllabe.startswith('gh')):
            kana = ascii2katakana(sylabe.replace("h", ''))
        elif syllabe == 'ci':
            kana = ascii2katakana('chi')
        elif syllabe == 'gi':
            kana = ascii2katakana('ji')
        elif syllabe in ('ca', 'cu', 'co'):
            kana = ascii2katakana(syllabe.replace('c', 'k'))
        elif syllabe in conversion_table.keys():
            kana = ascii2katakana(syllabe)
        elif syllabe == 'tu':
            kana = convert2katakana('tou')
        elif syllabe.endswith('n'):
            kana = convert2katakana(syllabe.replace('n', '')) + ascii2katakana('n')
        elif (syllabe[0] not in vocali) and (syllabe[1] not in vocali):
            new_str = syllabe[0] + 'u' + syllabe[1:]
            kana = convert2katakana(new_str)
        elif (syllabe[0] not in vocali):
            kana = convert2katakana(syllabe[0] + 'u' ) + convert2katakana(syllabe[1:])
        elif (syllabe[-1] not in vocali):
            new_str = syllabe + 'u'
            kana = convert2katakana(new_str)
        elif (syllabe[-1] in vocali) and (syllabe[-2] in vocali):
            kana = convert2katakana(syllabe[:-1]) + convert2katakana(syllabe[-1])
        else:
            kana = syllabe
        output_text.append(kana)
    return "".join(output_text)

katakana = list(map(chr, range(ord(u'\u30A1'), ord(u'\u30FF'))))
conversion_table = get_conversion_table(katakana)

text = "rosali"
katakana_name = convert2katakana(text) + convert2katakana('ya')
print(katakana_name)
print(katakana2acii(katakana_name))


# In[ ]:




