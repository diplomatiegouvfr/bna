#Un texte = un dictionnaire
#Une liste = une phrase
#Clé = numéro de la phrase, valeur = liste (= phrase)

#Types rajoutés dans le dictionnaire :
#PAYS
#CONTI (continent)
#ORG (organisation)
#ENTR (entreprise)
#CAPITALE
#DEVISE
#MOIS

#crée un dictionnaire qui désigne si phrase active 1 ou passive 0
#renvoie un dictionnaire
def activeOuPassive(self):
    voix = {}
    a=-1
    for i in self.values():
        a+=1
        taille = len(i)
        voix[a]=1
        for j in range(0,taille):
            if j+1<taille and "AUXE" in i[j] and i[j+1]=="PP": #si auxiliaire être placé devant participe passé = voix passive
                voix[a]=0
            if j+2<taille and "AUX" in i[j] and i[j+1]=="été" and i[j+2]=="PP": #si auxiliaire avoir placé devant "été" + participe passé = voix passive
                voix[a]=0
    return voix

#Fonction qui compte le nombre de verbes dans une phrase
def compteVER(self): # liste en entrée
    compt = 0
    for i in self:
        if i=="VER":
            compt=+1
    return compt

#Fonction qui compte le nombre d'auxiliaires être dans une phrase
def compteAUXE(self):
    compt = 0
    for i in self:
        if "AUXE" in i:
            compt=+1
    return compt

def compteAUX(self):
    compt = 0
    n= len(self)
    for i in range(n):
        if "AUX" in self[i] and i+1<n and "PP" in self[i+1]:
            compt +=1
    return compt

def get_verb(self, text): #self : dico avec tag, text dico avec mots
    verbs = {}
    a=-1
    for i,k in zip(self.values(), text.values()):
        a+=1
        taille = len(i)

        if compteVER(self[a])<=1:
            for j in range(0,taille):
                if "VER" in i[j]:
                    verbs[a] = k[j]

        elif compteAUXE(self[a])<=1: # AUXE
            for j in range(0,taille):
                if "AUXE" in i[j]:
                    verbs[a] = k[j]


        elif compteAUX(self[a]) <= 1:
            for j in range(0,taille):
                #On prend le prochain nom qui précède ou succède selon la voix
                if "AUX" in i[j]:
                    verbs[a] = k[j]

        else:  #si pas VER
            verbs[a] = "NULL"
    if len(verbs) != len(text):
        return verif_verb(verbs,text)
    return verbs


#Fonction qui renvoie deux dictionnaires (maitre et esclave)
#Il n'y a qu'un maitre et un esclave par phrase
#clé = numéro de la phrase, valeur = mot
def ME(self,text): #self : dico avec tag, text dico avec mots
    maitre = {}
    esclave = {}
    voix = activeOuPassive(self)
    a=-1
    for i,k in zip(self.values(), text.values()):
        a+=1
        taille = len(i)
        countVER = 0
        countAUXE = 0
        countAUX = 0
        if compteVER(self[a])<=1:
            for j in range(0,taille):
                if "VER" in i[j]:
                    countVER=+1
                #cherche pour des noms communs
                if voix[a] == 1:
                    if (i[j]=="NOM" or i[j]=="ENTR" or i[j]=="CAPITALE" or i[j]=="ORG" or i[j]=="PRO:per") and countVER==0 and k[j]!="se":
                        maitre[a] = k[j]
                    if (i[j]=="NOM" or i[j]=="ENTR" or i[j]=="CAPITALE" or i[j]=="ORG" or i[j]=="PRO:per") and countVER==1 and k[j]!="se":
                        esclave[a] = k[j]

                if voix[a] == 0:
                    if (i[j]=="NOM" or i[j]=="ENTR" or i[j]=="CAPITALE" or i[j]=="ORG" or i[j]=="PRO:per") and countVER==1 and k[j]!="se":
                        maitre[a] = k[j]
                    if (i[j]=="NOM" or i[j]=="ENTR" or i[j]=="CAPITALE" or i[j]=="ORG" or i[j]=="PRO:per") and countVER==0 and k[j]!="se":
                        esclave[a] = k[j]

        elif compteAUXE(self[a])==1: # AUXE
            for j in range(0,taille):
                if "AUXE" in i[j]:
                    countAUXE=+1
                #cherche pour des noms communs
                if voix[a] == 1:
                    if (i[j]=="NOM" or i[j]=="ENTR" or i[j]=="CAPITALE" or i[j]=="ORG" or i[j]=="PRO:per") and countAUXE==0 and k[j]!="se":
                        maitre[a] = k[j]
                    if (i[j]=="NOM" or i[j]=="ENTR" or i[j]=="CAPITALE" or i[j]=="ORG" or i[j]=="PRO:per") and countAUXE==1 and k[j]!="se":
                        esclave[a] = k[j]
                if voix[a] == 0:
                    if (i[j]=="NOM" or i[j]=="ENTR" or i[j]=="CAPITALE" or i[j]=="ORG" or i[j]=="PRO:per") and countAUXE==1 and k[j]!="se":
                        maitre[a] = k[j]
                    if (i[j]=="NOM" or i[j]=="ENTR" or i[j]=="CAPITALE" or i[j]=="ORG" or i[j]=="PRO:per") and countAUXE==0 and k[j]!="se":
                        esclave[a] = k[j]
                #cherche pour les pronoms
                elif countAUXE==1 and (i[j] == "PRO:per"):
                    if voix[a]==1:
                        esclave[a] = k[j]
                        break
                    else:
                        maitre[a] = k[j]
                        break
                elif countAUXE==0 and (i[j] == "PRO:per"):
                    if voix[a]==0:
                        esclave[a] = k[j]
                        break
                    else:
                        maitre[a] = k[j]
                        break


        elif compteAUX(self[a]) == 1:
            for j in range(0,taille):
                #On prend le prochain nom qui précède ou succède selon la voix
                if "AUX" in i[j]:
                    countAUX=+1
                if voix[a] == 1:
                    if (i[j]=="NOM" or i[j]=="ENTR" or i[j]=="CAPITALE" or i[j]=="ORG" or i[j]=="PRO:per") and countAUX==0 and k[j]!="se":
                        maitre[a] = k[j]
                    if (i[j]=="NOM" or i[j]=="ENTR" or i[j]=="CAPITALE" or i[j]=="ORG" or i[j]=="PRO:per") and countAUX==1 and k[j]!="se":
                        esclave[a] = k[j]
                if voix[a] == 0:
                    if (i[j]=="NOM" or i[j]=="ENTR" or i[j]=="CAPITALE" or i[j]=="ORG" or i[j]=="PRO:per") and countAUX==1 and k[j]!="se":
                        maitre[a] = k[j]
                    if (i[j]=="NOM" or i[j]=="ENTR" or i[j]=="CAPITALE" or i[j]=="ORG" or i[j]=="PRO:per") and countAUX==0 and k[j]!="se":
                        esclave[a] = k[j]

                """if voix[a] == 0:
                    if (i[j]=="NOM" or i[j]=="ENTR" or i[j]=="CAPITALE" or i[j]=="ORG" or i[j]=="PRO:per") and k[j]!="se":
                        maitre[a] = k[j]

                    elif a in maitre.keys():
                        if maitre[a] == i[-1]:
                            esclave[a] = "NULL"
                        else:
                            esclave[a] = ""
                            b = j
                            while b<len(i):
                                esclave[a] += " "+k[b]
                                b+=1"""

        else:  #si pas VER
            maitre[a] = "NULL"
            esclave[a] = "NULL"
    if len(maitre) != len(text) or len(esclave) != len(text):
        return verif(maitre,esclave,text)
    return maitre,esclave

def verif(maitre,esclave,texte): #met des NULL partout ou il manque des choses
    lenM = len(maitre)
    lenE = len(esclave)
    lenT = len(texte)
    m = {}
    e = {}
    for j in range(0,lenT):
        if j not in maitre:
            m[j] = "NULL"
        else:
            m[j] = maitre[j]
    for j in range(0,lenT):
        if j not in esclave:
            e[j] = "NULL"
        else:
            e[j] = esclave[j]
    return m,e

def verif_verb(verbs, texte):
    lenV = len(verbs)
    lenT = len(texte)
    v = {}
    for j in range(0,lenT):
        if j not in verbs:
            v[j] = "NULL"
        else:
            v[j] = verbs[j]
    return v
