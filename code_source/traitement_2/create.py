from nltk.tokenize import word_tokenize
import re


def OpenTxtStr(file_without_extension, fichier):
    fichier_str = open(r'sorties_v4/{}/categories/{}.txt'.format(file_without_extension, fichier), mode='r', encoding="utf-8").read()
    return fichier_str


def save_to_txt_file(text, fichier):
    
    with open(f'sorties_v4/{fichier}/{fichier}_couples.txt', mode="w", encoding="utf-8") as f:
        for i in text:
            if "." in i:
                f.write(i + "\n")
            else:
                 f.write(i)
    return print('{}_couples created and saved as TXT'.format(fichier))


def create_categ(data, fichier):
    # afin d'écraser le traitement precedent
    files = [
        'insatisfaisant',
        'passable',
        'satisfaisant',
        'tres_insatisfaisant',
        'tres_passable',
        'tres_satisfaisant',
        'assez_insatisfaisant',
        'assez_passable',
        'assez_satisfaisant',
        ]
    for f in files:
        open(f'sorties_v4/{fichier}/categories/{f}.txt', 'w').close()
    
    # Liste des intensités
    intensites = ['assez', 'tres']
    polarites = ['insatisfaisant', 'passable', 'satisfaisant']
    
    # classification des phrases dans les dossiers correspondants
    for ligne in data:
        phrase = word_tokenize(ligne)
        intensite = any(intensite in phrase for intensite in intensites)
        if intensite:
            polarite = phrase[-2]
            intensite =  phrase[-3]
            if (intensite in intensites) and (polarite in polarites): # gestion d'erreurs
                with open(f'sorties_v4/{fichier}/categories/{intensite}_{polarite}.txt', 'a') as f:
                    f.write(re.findall(r'\b\w+_\w+\b', ligne)[0] + '\n')
        elif not intensite:
            polarite = phrase[-2]
            if polarite in polarites: # gestion d'erreurs
                with open(f'sorties_v4/{fichier}/categories/{polarite}.txt', 'a') as f:
                    f.write(re.findall(r'\b\w+_\w+\b', ligne)[0] + '\n')

if __name__ == "__main__":
    pass
