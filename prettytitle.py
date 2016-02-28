DONTCAP = (
    # Don't capitalize articles (a, an, the),
    # unless the article is part of an artist's name.
    "a", "an", "the",
    # Don't capitalize coordinating conjunctions:
    "and", "but", "or", "nor", "for", "yet", "so",
    # Don't capitalize these prepositions:
    "as", "at", "by", "for", "in", "of", "on", "to",
    # The word versus (and its abbreviated form vs. or v.) is commonly left
    # in lower case, despite its being a preposition of more than 3 characters.
    "vs", "versus",  # NOTE: not adding 'v' here because of roman number V
    # The word Et cetera (and its abbreviated form etc.) is also commonly left
    # in lower case when used to represent the phrase and so on or and so forth.
    "etc",
    # Capitalize contractions and slang consistent with the rules above
    # to the extent that such clearly apply.
    # For example, do not capitalize o' for of, or n' for and, etc.
    "o'", "n'",
    # Some additional words used as slang...
    "ov", "ye"
)
# All prepositions with four or more letters
# such as into, from, with, upon, etc. should be capitalized.

RUSCAPITALIZE = ("сатана", "сатаны", "сатане", "сатану", "сатаной",
                 "дьявол", "дьявола", "дьяволу", "дьяволом", "дьяволе",
                 "христос", "христ", "христа", "христу", "христом", "христе",
                 "иисус", "иисуса", "иисусу", "иисусом", "иисусе",
                 "тьма", "тьмы", "тьме", "тьмой", "тьмою", "тьму",
                 "хаос", "хаоса", "хаосе", "хаосом", "хаосу",
                 "пустота", "пустоты", "пустотой", "пустоте")

CYRILLIC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
CONSONANTS = "BCDFGHJKLMNPQRSTVWXZ" + "БВЖЗЙКЛМНПРСТФХЦЧШЩ"
PLUSES = "ЪЬ-'`"


def pw_eng(w, newsent=False):
    # Capitalize every part of words with '-' or '/'
    for symbol in "-/":
        if symbol in w:
            return symbol.join(pw_eng(x, newsent=True) for x in w.split(symbol))
    return w.capitalize()


def pw_rus(w, newsent=False):
    if newsent:
        return w.capitalize()
    if w.lower() in RUSCAPITALIZE:
        return w.capitalize()
    return w.lower()


def pretty_word(s, newsent=False, lang="eng"):
    if not s:
        return ""
    if not newsent and (s.lower() in DONTCAP):
        return s.lower()
    if s[-1] in ".!?;:)]…":
        return pretty_word(s[:-1], newsent=newsent, lang=lang) + s[-1]
    if s[0] in "(['\"…":
        return s[0] + pretty_word(s[1:], newsent=newsent, lang=lang)
    if s.startswith("..."):
        return "..." + pretty_word(s[3:], newsent=newsent, lang=lang)

    # Don't touch abbreviatures and roman numbers
    if (s.isupper() and (s.strip("().-IVXLCDM") == "")) or (s.count(".") > 0):
        return s

    # Don't touch words with only consonant letters,
    # it's most likely not a regular word.
    if (len(s) > 1) and (s.upper().strip(CONSONANTS + PLUSES) == ""):
        return s

    if lang == "eng":
        return pw_eng(s, newsent)
    elif lang == "rus":
        return pw_rus(s, newsent)


def pretty_string(s, lang=None):
    newwords = []
    newsent = True

    # Lang detect. FIXME: Primitive for now
    if not lang:
        if any(x in s for x in CYRILLIC):
            lang = "rus"
        else:
            lang = "eng"

    for w in s.split():
        word = pretty_word(w, newsent, lang=lang)
        newwords.append(word)
        newsent = (word[-1] in ".!?;:)]…") or (word in ("-", "/", "—"))

    if lang == "eng":
        # also capitalize the very last word
        newwords[-1] = pretty_word(newwords[-1], True, lang="eng")

    if newwords[-1] == "Cover)":
        newwords[-1] = "cover)"
    if newwords[-1] == "Cover]":
        newwords[-1] = "cover]"
    return " ".join(newwords)
