def adverbes():
    adv = {
        "infiniment":1,
        "immensément":1,
        "excessivement":1,
        "démesurément":1,

        "complètement":1,
        "entièrement":1,
        "pleinement":1,
        "parfaitement":1,
        "totalement":1,
        "trop":1,
        "execellemment":1,
        "totalement":1,

        "extraordinairement":0.9,
        "extrêmement":0.9,
        "particulièrement":0.9,

        "profondément":0.8,
        "intensément":0.8,
        "globalement":0.8,
        "largement":0.8,
        "systématiquement":0.8,
        "majoritairement":0.8,

        "fortement":0.7,
        "considérablement":0.7,
        "grandement":0.7,
        "notablement":0.7,
        "tellement":0.7,
        "réellement":0.7,
        "très":0.7,
        "beaucoup":0.7,
        "clairement":0.7,
        "manifestement":0.7,
        "généralement":0.7,


        "correctement": 0.6,
        "honnêtement": 0.6,
        "suffisamment": 0.6,
        "respectablement": 0.6,
        "sensiblement":0.6,

        "moyennement":0.5,
        "modestement":0.5,
        "modérément":0.5,
        "relativement":0.5,

        "médiocrement":0.4,
        "insuffisamment":0.3,
        "modiquement":0.4,

        "partiellement":0.3,
        "incomplètement":0.3,
        "faiblement":0.3,
        "difficilement":0.3,
        "peu":0.3,

        "difficilement":0.2,
        "doucement":0.2,
        "horriblement":0.2,
        "quelques":0.2,
        "péniblement":0.2,

        "rarement":0.1,
        "quelque":0.1,
        "atrocement":0.1,
        "pitoyablement":0.1,
        "cruellement":0.1,

        "nullement":0,

        "assez":0.5,
        "davantage":0.1,
        "fort":0.7,

    }

    return adv

def conjonctions():
    conj = {
        "cependant":"ET",
        "pourtant":"ET",
        "néanmoins":"ET",
        "et":"ET",
        "mais":"ET",
        "soit":"OU",
        "ni":"nOU",
        "ou":"OU"
    }

    return conj

def intersection(int1, int2):
    return min(int1, int2)

def union(int1, int2):
    return max(int1, int2)

def negation(int):
    return 1-int

def tres(int):
    if (int == 0.5):
        return int
    elif (int > 0.5):
        return min(int*1.5, 1)
    else:
        return int*0.5

def parametres(phrase, conj):
    conjonction = conjonctions()
    adverbs = adverbes()
    a = "NULL"
    b = "NULL"
    operateur = "NULL"
    nega = [False, False]
    amplificateurs = [False, False]
    et = False
    passOperateur = False
    n = len(phrase)
    for i in range(n):
        mot = phrase[i]
        if (mot in adverbs.keys() and passOperateur==False):
            a = mot
            if i-1>=0 and phrase[i-1] == "pas":
                nega[0] = True
            if i-1>=0 and phrase[i-1] == "très":
                amplificateurs[0] = True

        if mot in adverbs.keys() and passOperateur==True:
            b = mot
            if i-1>=0 and phrase[i-1] == "pas":
                nega[1] = True
            if i-1>=0 and phrase[i-1] == "très":
                amplificateurs[1] = True
            break

        if (mot in conjonction):
            if (mot != "et"):
                operateur = conjonction[mot]
                passOperateur = True
            else :
                et = True
                passOperateur = True

    if (et == True and operateur == "NULL"):
        operateur = conjonction["et"]
    return a, b, operateur, nega, amplificateurs

def operation(phrase, tag):
    #Renvoie l'intensité d'une phrase
    adv = adverbes()
    a, b, op, nega, ampli = parametres(phrase, tag)
    if (a == "NULL" and b == "NULL"):
        return 0.5

    if (a == "NULL"):
        if nega[1]:
            return negation(adv[b])
        elif ampli[1]:
            return tres(adv[b])
        else:
            return adv[b]

    if (b=="NULL"):
        if nega[0]:
            return negation(adv[a])
        elif ampli[0]:
            return tres(adv[a])
        else:
            return adv[a]

    a = adv[a]
    b = adv[b]
    if nega[0] == True:
        a = negation(a)
    if nega[1] == True:
        b = negation(b)

    if ampli[0] == True:
        a = tres(a)
    if ampli[1] == True:
        b = tres(b)

    if op=="nIMP":
        return intersection(a, negation(b))
    elif op=="ET":
        return intersection(a, b)
    elif op=="OU":
        return union(a, b)
    elif op == "nOU":
        return 1-union(a, b)

    return 0.5

def intensite(self, tags):
    dico = {}

    index = 0
    for phrase, tag in zip(self.values(), tags.values()):
        dico[index] = operation(phrase, tag)

        index +=1
    return dico

if __name__=="__main__":
    import dico, miseenforme, tag

    with open("entrees/td8.txt", "rt", encoding="utf-8") as f:
        data = "je suis assez content mais pas insuffisamment"
        dictionnary = dico.Lexique()
        texte = miseenforme.passes(data,dictionnary)

        tags = tag.associeTag(data,texte,dictionnary)
        inten = intensite(texte, tags)
        print(inten)
