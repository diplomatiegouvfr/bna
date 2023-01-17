#Types rajoutés dans le dictionnaire :
#PAYS
#CONTI (continent)
#ORG (organisation)
#ENTR (entreprise)
#CAPITALE
#DEVISE
#MOIS

PP = "par:pas"

#print le type de chaque mot du dictionnaire
def afficheTag(self,passe,dictionnary):
    for i in passe.values():
        taille = len(i)
        for j in range(0,taille):
            print(i[j],dictionnary.searchingType(i[j]))
    return 0

#Fonction qui crée un dictionnaire dans lequel on a les tags de tous les mots par phrase
#Index correspondant �  ceux du dictionnaire du texte, on peut donc les comparer dans la fonction ME
#quand un mot possède plusieurs types/tags dans le dictionnaire on associe "dynamiquement" le tag correspondant �  la phrase
def associeTag(self,passe,dictionnary):
    text = {}
    a = -1
    for i in passe.values():
        phrase = []
        a+=1
        taille = len(passe[a])
        for j in range(0,taille):
            if len(dictionnary.searchingType(i[j]))==1 or dictionnary.searchingType(i[j])=='NULL': #Si le mot n'a qu'un type ou son type est indéfini (NULL)
                str = ''.join(dictionnary.searchingType(i[j]))
                phrase.append(str)
#                phrase.append(i[j])
            elif "VER" in dictionnary.searchingType(i[j]) and PP in dictionnary.searchingPP(i[j]) and "NOM" not in dictionnary.searchingType(i[j-1]): #Si le dictionnaire indique que c'est un participe passé, on le tag en temps que PP (et non VER)
                phrase.append("PP")
            elif ("NOM" in dictionnary.searchingType(i[j]) or "PAYS" in dictionnary.searchingType(i[j])) and "VER" in dictionnary.searchingType(i[j]) and "ADJ" not in dictionnary.searchingType(i[j]) : # Si le mot est un NOM et un VER mais pas un ADJ
                if j-1>=0 and ("ART:ind" in dictionnary.searchingType(i[j-1]) or "ART:def" in dictionnary.searchingType(i[j-1]) or "ADJ:dem" in dictionnary.searchingType(i[j-1])): #si notre mot est précédé d'un déterminant alors c'est un NOM
                    phrase.append("NOM")
    #                    phrase.append(i[j])
                elif j-2>=0 and ("ART:ind" in dictionnary.searchingType(i[j-2]) or "ART:def" in dictionnary.searchingType(i[j-2])): #si mot qui précède notre mot est précédé d'un déterminant
                    if j-1>=0 and "ADJ" in dictionnary.searchingType(i[j-1]): #si le mot qui précède notre mot est un ADJ, alors notre mot est un NOM
                        phrase.append("NOM")
    #                   phrase.append(i[j])
                    elif j-1>=0 and "CONTI" in dictionnary.searchingType(i[j-1]):
                        phrase.append("VER")
                    else:
                        phrase.append(dictionnary.searchingType(i[j])) #Si mot qui précède notre mot n'est pas précédé par un article alors on laisse tel quel
    #                   phrase.append(i[j])
                elif j+1<taille and "NOM" in dictionnary.searchingType(i[j+1]) and "ADJ" in dictionnary.searchingType(i[j+1]): #si notre mot est suivi d'un mot �  la fois NOM et ADJ alors c'est un NOM sinon c'est un VER
                    phrase.append("NOM")
    #               phrase.append(i[j])
                elif j-1>= 0 and "ADJ:pos" in dictionnary.searchingType(i[j-1]):
                    phrase.append("NOM")
                else:
                    phrase.append("VER")
#                    phrase.append(i[j])
            elif "NOM" in dictionnary.searchingType(i[j]) and ("ADJ" in dictionnary.searchingType(i[j]) or "ADJ:pos" in dictionnary.searchingType(i[j])) and "VER" not in dictionnary.searchingType(i[j]) and "AUXE" not in dictionnary.searchingType(i[j]) and "PRE" not in dictionnary.searchingType(i[j]): #si c'est un NOM et un ADJ ou un ADJ possessif mais pas un VER ni un AUXE ni un PRE
                if j-1>=0 and "NOM" in dictionnary.searchingType(i[j-1]) and "ADJ" not in dictionnary.searchingType(i[j-1]) and "ADV" not in dictionnary.searchingType(i[j-1]) and j!=0: #prend la phrase d'avant en compte, si notre mot est précédé par un NOM pas par un ADJ ou un ADV alors c'est un ADJ
                    phrase.append("ADJ")
#                    phrase.append(i[j])
                elif "ADJ:dem" in dictionnary.searchingType(i[j-1]):
                    phrase.append("NOM")
                elif j+1<taille and "NOM" in dictionnary.searchingType(i[j+1]) and "ADJ" not in dictionnary.searchingType(i[j+1]): #si notre mot est succédé par un NOM qui n'est pas un ADJ alors notre mot est un ADJ
                    phrase.append("ADJ")
#                    phrase.append(i[j])
                elif j-1>=0 and "ART:def" in dictionnary.searchingType(i[j-1]):
                    phrase.append("NOM")
                else:
                    phrase.append(dictionnary.searchingType(i[j]))
#                    phrase.append(i[j])
            elif "AUXE" in dictionnary.searchingType(i[j]) and "VER" in dictionnary.searchingType(i[j]): #or adj ?
                if "AUXE" in dictionnary.searchingType(i[j-1]) and j!=0:
                    phrase.append("VER")
#                    phrase.append(i[j])
                else:
                    phrase.append("AUXE")
#                    phrase.append(i[j])
            elif "VER" in dictionnary.searchingType(i[j]) and "ADJ" in dictionnary.searchingType(i[j]):
                if j-1>=0 and "AUXE" in dictionnary.searchingType(i[j-1]) or "AUX" in dictionnary.searchingType(i[j-1]):
                    phrase.append("VER")
#                    phrase.append(i[j])
                else:
                    phrase.append("ADJ")
#                    phrase.append(i[j])
            elif "NOM" in dictionnary.searchingType(i[j]) and "ADV" in dictionnary.searchingType(i[j]) and "ADJ" not in dictionnary.searchingType(i[j]) and "VER" not in dictionnary.searchingType(i[j]) and "AUXE" not in dictionnary.searchingType(i[j]):
                if j-1>=0 and "AUXE" in dictionnary.searchingType(i[j-1]):
                    phrase.append("ADV")
#                    phrase.append(i[j])
                else:
                    phrase.append(dictionnary.searchingType(i[j]))
#                    phrase.append(i[j])
            elif "NOM" in dictionnary.searchingType(i[j]) and "ADJ" in dictionnary.searchingType(i[j]) and "AUXE" in dictionnary.searchingType(i[j]) and "ADV" not in dictionnary.searchingType(i[j]) and "VER" not in dictionnary.searchingType(i[j]):
                if (j+1<taille and j-1>=0 and "NOM" in dictionnary.searchingType(i[j-1]) and ("PRO:ind" in dictionnary.searchingType(i[j+1]))) or (j+1<taille and "ART:ind" in dictionnary.searchingType(i[j+1])) : #ça prend la phrase d'avant
                    phrase.append("AUXE")
#                    phrase.append(i[j])
                else:
                    phrase.append(dictionnary.searchingType(i[j]))
#                    phrase.append(i[j])
            elif "ADJ" in dictionnary.searchingType(i[j]) and "PRE" in dictionnary.searchingType(i[j]) and "NOM" not in dictionnary.searchingType(i[j]):
                if "ADV" in dictionnary.searchingType(i[j-1]):
                    phrase.append("PRE")
#                    phrase.append(i[j])
                elif j<taille-1 and ("PRO:per" in dictionnary.searchingType(i[j+1]) or "ART:def" in dictionnary.searchingType(i[j+1])):
                    phrase.append("PRE")
#                    phrase.append(i[j])
                else:
                    phrase.append(dictionnary.searchingType(i[j]))
            elif "ADV" in dictionnary.searchingType(i[j]) and "PRE" in dictionnary.searchingType(i[j]):
                if j<taille-1 and ("PRO:per" in dictionnary.searchingType(i[j+1]) or "ART:def" in dictionnary.searchingType(i[j+1])
                 or ("VER" in dictionnary.searchingType(i[j+1]) and "inf" in dictionnary.searchingPP(i[j+1]))):
                 phrase.append("PRE")
                else:
                 phrase.append("ADV")
            elif "ART:def" in dictionnary.searchingType(i[j]) and "PRO:per" in dictionnary.searchingType(i[j]):
                if j+1<taille and ("NOM" in dictionnary.searchingType(i[j+1]) or "CONTI" in dictionnary.searchingType(i[j+1]) or "PAYS" in dictionnary.searchingType(i[j+1])):
                    phrase.append("ART")
                else:
                    phrase.append("PRO")
            elif "AUXE" in dictionnary.searchingType(i[j]) and "ADJ" in dictionnary.searchingType(i[j]) and "NOM" in dictionnary.searchingType(i[j]):
                if j-1>=0 and "NOM" in dictionnary.searchingType(i[j-1]):
                    phrase.append("AUXE")
                else:
                    phrase.append("ADJ")

#                    phrase.append(i[j])
            else:
                phrase.append(dictionnary.searchingType(i[j]))
#                phrase.append(i[j])
        text[a] = phrase
    return text

#son indique ADJ au lieu de ADJ:pos

#placement dans la phrase, pour pas prendre la phrase d'avant ou d'après
#compter les verbes, s'il y en a déj�  un...
