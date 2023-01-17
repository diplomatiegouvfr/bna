import re

path = "lexique/freq.txt"

def create_table_freq() -> dict:
    """Créé la table des fréquences des bigrammes"""
    second_letters = []

    dic = dict()

    label = True
    with open(path, "r") as f:

        data = f.readlines()
        for line in data:
            if label:
                letters = re.sub(" ", "", line.strip()).split("\t")
                for l in letters:
                    second_letters.append(l)
                label = False
            else:
                freqs = re.sub(" ", "", line.strip()).split("\t")
                n = len(second_letters)
                for index in range(n):
                    dic[freqs[0][0]+second_letters[index][1]] = int(freqs[index+1]) #décalage de 1 car ligne de la forme : Lettre->freqs
    return(dic)

def bigrammes(mot) -> list:
    """Découpe le mot en bigrammes"""
    n = len(mot)
    up = re.sub("é|è|ê|ë", "e", mot).upper()
    liste = []

    for i in range(n-1):
        liste.append(up[i:i+2])
    return liste

def calculate(dic, mot) -> float:
    """Calcule l'inverse de la fréquence d'un mot en fonction des bigrammes"""
    bigrams = bigrammes(mot)
    summ = 0
    # print(dic.values())
    total = sum(dic.values())

    for b in bigrams:
        if b in dic.keys():
            summ += dic[b]/total

    tmp = summ/len(mot)
    if tmp == 0:
        return 0
    return 1/tmp


if __name__=="__main__":
    pass
