text = """	Ưżuṡazailian. Uṡaz:
	- Upun atư bah, édhom éctaupuzużuċ (300010) ul. Éṡb ẻtớtaulupużuzuluċ (9000010) ul, atife hơm ịfusus.
	Ipáde żơt, rarmoż, mơt mơc ịfẽ hơm.
	Ágizud, ĩmabon? Ibe mfiáhailiág? Ibzaé gơc ịpr.
"""

lowerDict = {
    'Ƞ': 'ȡ',
    'Ȍ': 'ȍ',
    'Ț': 'ț',
    'Ȟ': 'ȟ',
}

def lower(txt):
    for letter in lowerDict:
        txt = txt.replace(letter, lowerDict[letter])

    txt = txt.lower()
    return txt

replaceDict = {
    ',': '',  # punctuations
    '.': '',
    'á': 'a', 'à': 'a', 'ả': 'ã', # vowels
    'é': 'e', 'è': 'e', 'ẻ': 'ẽ', 'ț': 'ẹ', 'ȟ': 'ȡ',
    'í': 'i', 'ì': 'i', 'ỉ': 'ĩ', 'ȍ': 'ị',
    'ó': 'o', 'ò': 'o', 'ỏ': 'õ', 'ớ' : 'ơ', 'ờ': 'ơ',
    'ú': 'u', 'ù': 'u', 'ủ': 'ũ', 'ứ': 'ư',
    'ĩ': 'ɪ',
    'ị': 'y',
    'ẹ': 'ø',
    'ẽ': 'ε',
    'ȡ': 'œ',
    # 'a': 'ə',
    'ơ': 'ə',
    # 'ã': 'a',
    'õ': 'ɔ',
    'ư': 'ɯ',
    'ũ': 'ʊ',
    'r': 'ɾ',  # consonants
    'ż': 'ʧ',
    'ṡ': 'ʃ',
    'z': 'ʦ',
    'c': 'k',
    'ċ': 'x',

}

def replace(txt):
    for letter in replaceDict:
        txt = txt.replace(letter, replaceDict[letter])
    return txt

def main(txt):
    print(replace(lower(txt)))

# main(text)