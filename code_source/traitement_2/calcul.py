from utils import singular_noun, split_lst
import os
import nltk
from nltk import word_tokenize
from nltk.tag import StanfordPOSTagger
import pandas as pd

# tags Fr
jar = 'Lib/StanfordTagguer/stanford-postagger.jar'
model = 'Lib/StanfordTagguer/models/french-ud.tagger'
pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8' )

# environnement
java_path = 'C:/Program Files (x86)/Common Files/Oracle/Java/javapath/java.exe'
os.environ['JAVAHOME'] = java_path


def moyenne(l):
    """calcul de la moyenne des valeurs d’une liste de nombres l"""
    return sum(l) / len(l)


def variance(moy, l):
    """Calcul de la variance des valeurs d'une liste de nombres l."""
    return sum([(x - moy(l)) ** 2 for x in l]) / len(l)


def delta(l, x):
    return sum(map(lambda element: 1 if element > x else -1, l))


def mediane(l):
    """calcul de la mediane des valeurs d’une liste de nombres l"""
    return (sum(sorted(l)[len(l)//2-1:len(l)//2+1])/2.0, sorted(l)[len(l)//2])[len(l) % 2] if len(l) else None


def lst_frq(l):
    return [round(i/sum(l), 3) for i in l]


def frq_mot_dico(fichier): # frquence de mots sur un texte simple
    """Calcul de la fréquence de mots avec filtre sur les noms communs

       Parameters
       ----------
       fichier : str(txt -> couple)
         Prend en entrée un fichier texte .

       Output
       ----------
       dict(mot : frquence) trié
    """
    # open and read the file
    file = open('{}.txt'.format(fichier), mode='r', encoding='utf-8').read()
    #list accentuation
    stop = {'a': ['à', 'ã', 'á', 'â'],
            'e': ['é', 'è', 'ê', 'ë'],
            'i': ['î', 'ï'],
            'u': ['ù', 'ü', 'û'],
            'o': ['ô', 'ö'],
            ' ': [',', "?", ';', '.', ':', '/', '!', '§', '%', 'µ', '*', '£', '$', '¤', '&', '"', '{', '(', '[', '-', '|', '`', '_', '\'', 'ç', '@', ')', ']', '°', '=', '+', '}', '²', '<', '>', '\n'],
            '': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']}
    
    # Loop to remoove accentuation
    for (character, accented_characters) in stop.items():
        for accented_character in accented_characters:
            file = file.replace(accented_character, character)
    
    file = file.upper()
    file = file.lower()
    
    words = [i for i in file.split(" ") if not len(i) <= 4]
    
    big_list_of_list = split_lst(words, 66000)
    
    tag = sum([eval(str(pos_tagger.tag(lst))) for lst in big_list_of_list], [])
    
    phrase = [mot for mot in tag if 'NOUN' in mot or 'ADJ' in mot or 'ADV' in mot or 'PUNCT' in mot or 'VERB' in mot]
    
    nouns = [mot for mot in phrase if 'NOUN' in mot or 'PUNCT' in mot]
    
    wordlist = [i[0] for i in nouns]
    
    wordlist = singular_noun(' '.join(wordlist)).split()
    
    # stopwords
    stopwords = set(open(r'Lib/Lexique/stopwords.txt','r', encoding="utf8").read().splitlines())
    
    wordlist_without_sw = [word for word in wordlist if not word in stopwords]
    
    #capitalize the first character of each word
    wordlist_without_sw = [word.capitalize() for word in wordlist_without_sw]

    freq = dict()
    
    for word in wordlist_without_sw: 
        if word in freq.keys():
            freq[word] = freq[word]+1
        else: 
            freq[word] = 1
    
    return {k: v for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True)} # Sort dic by value


def frq_mot(string): # frequence de mots sur 'mot_mot\nmot_mot'
    wordlist = word_tokenize(string.replace('_', ' '))
    dic = dict(nltk.FreqDist(wordlist))
    return {k: v for k, v in sorted(dic.items(), key=lambda item: item[1], reverse=True)}


def wordcloud_dico(couples, seuil): # couples = 'mot_mot\nmot'
    couples = couples.replace('\n', ' ') # string
    words = couples.replace('_', ' ') # string
    words_freq = frq_mot(words) # dictionary of word frequencies

    df_words_freq = pd.DataFrame(words_freq.items(), columns=['word', 'freq'])
    df_couples = pd.DataFrame(tuple([couple.split('_') for couple in word_tokenize(couples)]), columns=['FirstWord', 'SecondWord'])
    
    couples_freq = dict() # dictionary of couplpes frequencies
    
    for first_word, second_word in zip(df_couples.FirstWord, df_couples.SecondWord):
        couple = first_word + ' ' + second_word
        couple = couple.upper()
        couple_freq = words_freq.get(first_word) + words_freq.get(second_word)
        new = {couple:couple_freq}
        couples_freq.update(new)
    
    df_couples['FirstFreq']=''
    df_couples['SecondFreq']=''
    get_frq = (lambda x: df_words_freq.loc[df_words_freq['word']==x].iloc[0,1])
    for i in range(len(df_couples)):
        df_couples['FirstFreq'][i] = get_frq(df_couples['FirstWord'][i]) # incrementing in the DataFrame
        df_couples['SecondFreq'][i] = get_frq(df_couples['SecondWord'][i]) # incrementing in the DataFrame
    df_couples['GlobalFreq'] = df_couples['FirstFreq'] + df_couples['SecondFreq']
    
    l = []
    for i in zip(df_couples['FirstWord'], df_couples['SecondWord'], df_couples['FirstFreq'], df_couples['SecondFreq'], df_couples['GlobalFreq']):
        if (i[0], i[1]) not in l:
            l.append((i[0], i[1]))
        else: # duplicates are droped
            df_couples = df_couples.drop(df_couples[(df_couples.FirstWord == i[0]) & (df_couples.SecondWord == i[1])].index) # All are dropped !
            new_line = {'FirstWord': i[0], 'SecondWord': i[1], 'FirstFreq': i[2], 'SecondFreq': i[3], 'GlobalFreq': i[4]} # Get one of dropped
            df_couples = df_couples.append(new_line, ignore_index = True) # Add it to dataframe
    df_couples = df_couples.sort_values(by='GlobalFreq', ascending=False) # Sort dataframe by descending of global frequencies
    
    df_couples['Bigram'] = df_couples['FirstWord'] + ' ' + df_couples['SecondWord']
    
    dic_global = pd.Series(df_couples.GlobalFreq.values,index=[df_couples.Bigram][0]).to_dict()
    dic_global = {k.upper(): v for k, v in dic_global.items()}
    global_sorted = {k: v for k, v in sorted(dic_global.items(), key=lambda item: item[1], reverse=True)}
    
    limit = round(len(global_sorted) * seuil)
    df_couples = df_couples.iloc[limit:]
    dic_couples_mot = dict(list(global_sorted.items())[limit:])

    most_frq_bigram = df_couples.loc[(df_couples['GlobalFreq'] == max(df_couples['GlobalFreq']))]
    
    if most_frq_bigram['FirstFreq'].values[0] > most_frq_bigram['SecondFreq'].values[0]:
        most_frq_word = most_frq_bigram['FirstWord'].values[0]
    elif most_frq_bigram['FirstFreq'].values[0] < most_frq_bigram['SecondFreq'].values[0]:
        most_frq_word = most_frq_bigram['SecondWord'].values[0]
    else:
        most_frq_word = most_frq_bigram['FirstWord'].values[0]
        
    return dic_couples_mot, most_frq_word