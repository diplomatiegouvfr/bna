
import dico, miseenforme

verbe_etat = ["paraître", "sembler", "demeurer", "devenir", "rester"] #verbe être

def transformationOuPas(phrase, dico):
    # 0 si la phrase contient un verbe d'état
    # 1 sinon
    n = len(phrase)
    nbV = 0
    verbeEtre = False
    for i in range(n):
        mot = phrase[i]
        if ("VER" in dico.searchingType(mot)):
            nbV +=1
            if dico.searchingLemme(mot) in verbe_etat:
                return 0
            if dico.searchingLemme(mot) == "être":
                verbeEtre = True

    if nbV == 0:
        return 0

    #Si le verbe être est seul dans une phrase, on le considère comme un verbe d'état
    if verbeEtre and nbV == 0:
        return 0
    return 1

def transform(text, dico):
    result = {}
    nbS = len(text)
    for i in range(nbS):
        result[i] = transformationOuPas(text[i], dico)
    return result


if __name__=="__main__":
    with open('entrees/td2.txt','rt', encoding='utf-8') as f:
        data = f.read()

    dictionnary = dico.Lexique()

    texte =miseenforme.passes(data,dictionnary)

    t = transform(texte, dictionnary)
    compt1 = 0
    for k, v in t.items():
        if v != "NULL":
            compt1 +=int(v)
    print(compt1)
    print(t)
