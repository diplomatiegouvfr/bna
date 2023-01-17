# -*- coding: utf-8 -*-

# Synopsis : py main.py nomdufichier
# py main.py sorties/MINCUL_2022/MINCUL_2022.180722-095637.txt

from graphique import create_wordcloud_categ, create_word_cloud, create_pie_chart, create_gauss_chart
from workspace import file_count_data
from couples import sent_to_word_pairs
from calcul import frq_mot_dico, wordcloud_dico
from create import OpenTxtStr
from generateur import generate_ppt
from utils import extract_file_info
import sys
import os
import glob

if __name__ == "__main__":
    
    file_path = sys.argv[1]
    file_name_without_extension, base_name, path_without_file_name, short_name = extract_file_info(file_path)
    
    sent_to_word_pairs(short_name, file_name_without_extension) # word pairs cleaning
    
    fichiers = [os.path.splitext(os.path.basename(file_path))[0] for file_path in glob.glob('sorties_v4/{}/categories/*.txt'.format(file_name_without_extension))]
    data = [OpenTxtStr(file_name_without_extension, file_name) for file_name in fichiers]
    
    categories_dict = {key: value for key, value in zip(fichiers, data)}
        
    wordcloud_directory = f'sorties_v4/{file_name_without_extension}/wc_output'
    try:
        os.makedirs(wordcloud_directory, exist_ok=True)
    except OSError as e:
        print(f'Error creating directory: {e.strerror}')
    
    
    seuil = 0 # seuil qui supprime de la donnée
    categ_frequences = {key: None for key in fichiers} # dictionnaire(categorie:dictionnaire(paire:frequence))
    categ_most_frq_word = {key: None for key in fichiers} # dictionnaire(categ:mot_le_plus_frequent)
    
    # Loop apllying the wordcloud function for non-emlpty files
    for fichier in fichiers:
        empty_file = os.stat(f'sorties_v4/{file_name_without_extension}/categories/{fichier}.txt').st_size == 0
        if not empty_file:
            main_dic = wordcloud_dico(categories_dict.get(fichier), seuil)
            categ_frequences[fichier] = main_dic[0]
            categ_most_frq_word[fichier] = main_dic[1]
            if len(categ_frequences[fichier])>3:
                create_wordcloud_categ(file_name_without_extension, fichier, main_dic[0])
    
    img_directory = f'sorties_v4/{file_name_without_extension}/images'
    try:
        os.makedirs(img_directory, exist_ok=True)
    except OSError as e:
        print(f'Error creating directory: {e.strerror}')
    
    #  main wordcloud
    intput_path = f'entrees/{short_name}'
    main_wordcloud_frq = frq_mot_dico(intput_path)
    output_path = rf'sorties_v4/{file_name_without_extension}/images/wordcloud_output_principal.png'
    create_word_cloud(output_path, main_wordcloud_frq)
    
    # pie chart
    data_path = f"sorties_v4/{file_name_without_extension}/{file_name_without_extension}_couples.txt"
    data = file_count_data(data_path)
    create_pie_chart(file_name_without_extension, output_path, data)
    
    # gaussian chart
    create_gauss_chart(file_name_without_extension, data)
    
    # power point generation
    generate_ppt(short_name, file_name_without_extension, categories_dict, main_wordcloud_frq, categ_most_frq_word) # PowerPoint creation
