import os
from nltk.tokenize import word_tokenize

from word import Word
from create import save_to_txt_file, create_categ
from utils import remove_punctuation, remove_numbers, remove_whitespaces, simplify_sent, lemme_replace, set_stopwords, remove_sw, remove_duplicates, tag, remove_accent


def sent_to_word_pairs(short_name, fichier):
    #short_name_file, fichier = "MINCUL_2022", "MINCUL_2022.180722-095637"
    
    text = open(f'sorties/{short_name}/{fichier}.txt','rU', encoding="utf8").read()
    
    text_processing = text.lower()
    text_processing = remove_punctuation(text_processing)
    text_processing = remove_numbers(text_processing)
    text_processing = remove_whitespaces(text_processing)
    
    text_processing = simplify_sent(text_processing) # remove "de" and "est"
    
    text_processing = text_processing.split('\n') # create sent tokens
    text_processing = [word_tokenize(sentence) for sentence in text_processing] # return sentences containting words
    
    lexicon_lemmatizer = lemme_replace(text_processing) # return a tuple
    text_processing = lexicon_lemmatizer[0] # lemmatized with lexicon
    unknown_words = lexicon_lemmatizer[1] # words wich are not in lexicon
    
    stop_words = set_stopwords()
    text_pasring = remove_sw(text_processing, stop_words) # return sentences without stopwords
    text_pasring = remove_duplicates(text_pasring, stop_words) # return sentences without duplicates
    text_parsing_tag = [[(w, tag(w)) if Word(w).exists else (w, ['NA']) for w in s] for s in text_pasring] # apply tag to words
    text_parsing_tag = [[w[0] for w in s] for s in text_parsing_tag if any(tag in ['NOM', 'ADJ', 'ADV', 'NA'] for tag in set(s[0][1]+s[1][1]))] # return parsing by tag
    
    # Sentence structuring by adding ' ', '.', '_'
    formatted_text = list(map(lambda x: x[:1] + list("_") + x[1:] + list("."), text_parsing_tag)) 
    formatted_text = list(map(lambda x: x[:3] + list(" ") + x[3:], formatted_text))
    formatted_text = list(map(lambda x: x[:5] + list(" ") + x[5:] if len(x)==7 else x, formatted_text))
    formatted_text = list(map(lambda x: ''.join(x), formatted_text))
    
    formatted_text = list(map(lambda x: x.replace("satisfaire","satisfaisant"), formatted_text)) # fix lem error
    formatted_text = list(map(lambda x: remove_accent(x), formatted_text)) # remove accent
        
    
    try:
        os.mkdir('sorties_v4') # folder init
        os.mkdir('sorties_v4/{}'.format(fichier)) # subfolder init
        os.mkdir('sorties_v4/{}/categories'.format(fichier)) # subfolder init
    except OSError as e:
        print(os.strerror(e.errno))
    
    save_to_txt_file(formatted_text, fichier) # pairs of words saved in txt format
        
    create_categ(open(f'sorties_v4/{fichier}/{fichier}_couples.txt', 'r', encoding='utf-8'), fichier) # pairs of words sorted by categories in txt format




