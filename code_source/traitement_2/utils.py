import os
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from stop_words import get_stop_words
import re
from word import Word
from nltk.tokenize import word_tokenize
import unidecode
from nltk.stem import SnowballStemmer
fr = SnowballStemmer('french')

def extract_file_info(file_path):
    #Extract the base name of the file (with the extension)
    base_name = os.path.basename(file_path)
    #Extract the name of the file without the extension
    file_name_without_extension = os.path.splitext(base_name)[0]
    #Extract the path of the file without the file name
    path_without_file_name = os.path.dirname(file_path)
    #Extract the short name of the file
    short_name = os.path.basename(os.path.dirname(file_path))
    return file_name_without_extension, base_name, path_without_file_name, short_name


def remove_punctuation(text):
    punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@'
    return re.sub('[' + punctuation + ']+', ' ', text)


def remove_numbers(text):
    return re.sub('([0-9]+)', '', text)


def remove_whitespaces(text):
    return text.strip()


def simplify_sent(text):
    text = text.replace(" est "," ")
    text = text.replace(" de "," ")
    return text


def set_stopwords():
    stopwords = set()
    stopwords.update(set(get_stop_words('french'))) # from spacy
    stopwords.update(fr_stop) # from stop-words
    stopwords.update(set(open(r'Lib/Lexique/stopwords.txt','r', encoding="utf8").read().splitlines())) # from MEAE
    stopwords_ok = {'assez', 'très',
                    'dos', 'nouveau', 'nouveaux', 'parole', 'personne', 'personnes', 'valeur'} # Those we want to keep
    [stopwords.remove(stopword_ok) for stopword_ok in stopwords_ok]
    return stopwords


def remove_sw(sent_tokens, stopwords):
    """Return sentences without stopwords"""
    return [s for s in sent_tokens if not any(w in stopwords for w in s)]


def remove_duplicates(sent_tokens, stopwords):
    """Return sentences without duplicates"""
    return [s for s in sent_tokens if not s[0] == s[1]]


def tag(word):
    return Word(word).cgram


def lem(word):
    return Word(word).lemme


def lemme_replace(sent_tokens):
    unknown_words = []
    for i, s in enumerate(sent_tokens):
        for k, w in enumerate(s):
            try:
                sent_tokens[i][k] = lem(w)[0]
            except TypeError:
                unknown_words.append(w)
    return sent_tokens, unknown_words


def tag_sent_tokens(sent_tokens):
    return [(w, tag(w)) for s in sent_tokens for w in s]


def remove_accent(self):
    return unidecode.unidecode(self)


def singular_noun(string): #input type -> string
    """Transformation de noms communs du pluriel au singulier

       Parameters
       ----------
       string : str(txt -> couple ou texte avec ' ')
         Prend en entrée un fichier texte incluant des couples
         de mots separes par des underscores '_', '\n', ' '.

       Output
       ----------
       string avec des '_' et '\n'
       ou
       string avec ' '
    """
    strings = string
    strings = (' '.join((' '.join(strings.split('\n'))).split('_'))).split()

    ou = open(r'Lib/Lexique/ou_oux.txt','r', encoding="utf8").read().splitlines()
    ail = open(r'Lib/Lexique/ail_aux.txt','r', encoding="utf8").read().splitlines()
    al = open(r'Lib/Lexique/al_als.txt','r', encoding="utf8").read().splitlines()
    al_noms = open(r'Lib/Lexique/al_aux.txt','r', encoding="utf8").read().splitlines()
    eu = open(r'Lib/Lexique/eu_eus.txt','r', encoding="utf8").read().splitlines()
    au = open(r'Lib/Lexique/au_aus.txt','r', encoding="utf8").read().splitlines()
    invariables_noms = open(r'Lib/Lexique/invariables.txt','r', encoding="utf8").read().splitlines()
    
    new_strings = []
    
    for nom in strings :
        
        # On commence par les exceptions
        if nom in invariables_noms:
            new_string = nom
            new_strings.append(new_string)
        
        # 1. Les noms qui terminent en -ou prennent un « s » final au pluriel, sauf :
        elif nom in ou:
            new_string = nom.replace("oux", "ou")
            new_strings.append(new_string)
        
        # 1.1 Les noms qui terminent en -ou prennent un « s » final au pluriel :
        elif nom[-3:] == 'ous':
            new_string = nom.replace("ous", "ou")
            new_strings.append(new_string)
    
        # 2. Les noms qui terminent en -ail prennent un « s » final au pluriel, sauf :
        elif nom in ail:
            new_string = nom.replace("aux", "ail")
            new_strings.append(new_string)
        
        # 2.2 Les noms qui terminent en -ail prennent un « s » final au pluriel :
        elif nom[-4:] == 'ails':
            new_string = nom.replace("ails", "ail")
            new_strings.append(new_string)        
    
        # 3. Les noms qui terminent en -al font leur pluriel en -aux, sauf :
        elif nom in al:
            new_string = nom.replace("als", "al")
            new_strings.append(new_string)
        
        # 3.3 Les noms qui terminent en -al font leur pluriel en -aux:
        elif nom in al_noms:
            new_string = nom.replace("aux", "al")
            new_strings.append(new_string)
    
        # 4. Les noms qui terminent en -eu prennent un « x » final au pluriel, sauf :
        elif nom in eu:
            new_string = nom.replace("eus", "eu")
            new_strings.append(new_string)
        
        # 4.4 Les noms qui terminent en -eu prennent un « x » final au pluriel :
        elif nom[-3:] == 'eux':
            new_string = nom.replace("eux", "eu")
            new_strings.append(new_string)
    
        # 5. Les noms qui terminent en -au prennent un « x » final au pluriel, sauf :
        elif nom in au:
            new_string = nom.replace("aus", "au")
            new_strings.append(new_string)
        
        # 5.5 Les noms qui terminent en -au prennent un « x » final au pluriel:
        elif nom[-3:] == 'aux':
            new_string = nom.replace("aux", "au")
            new_strings.append(new_string)
    
        # 6. Les noms qui terminent en -eau font leur pluriel en -x :
        elif nom[-4:] == 'eaux':
            new_string = nom.replace("eaux", "eau")
            new_strings.append(new_string)
    
        # 8. Les noms qui terminent en -s :
        elif nom[-1:] == 's' and not nom in invariables_noms:
            new_string = nom.replace(nom, nom[:-1])
            new_strings.append(new_string)
    
        # 8. Les noms qui terminent en -s, -x ou -z sont invariables :
        elif nom[-1:] == 's' or nom[-1:] == 'x' or nom[-1:] == 'z':
            new_strings.append(nom)
    
        else:
            new_strings.append(nom)
          
    if '_' in str(string):
        c=[]  
        it = iter(new_strings)
        for x, y in zip(it, it):
            c.append(x)
            c.append('_')
            c.append(y)
            c.append('\n')
        new_strings= ''.join(c)
    else:
        new_strings = ' '.join(new_strings)
        
    return new_strings #" ".join(new_strings)


def suppr_doublons(lst):
    unique_sentences = [sent for sent in lst if fr.stem(word_tokenize(sent)[0]) != fr.stem(word_tokenize(sent)[1])]
    return list(filter(None, unique_sentences))


def normalisation(string):
    return re.sub(r'[\n_]', ' ', string)


def split_lst(big_list, limit):
    "Return a list split into list of lists python on every n element"
    return [big_list[i:i+limit] for i in range(0, len(big_list), limit)]


def format_nbr(nbr):
    return "{:,}".format(nbr)



