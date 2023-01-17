#!/usr/bin/env python3
## -*- coding: utf-8 -*-
import re

def passe05(self): #On remplace les abréviations
    text = self.replace("M.","Monsieur")
    text1 = text.replace("M€","millions d'euros")
    text2 = text1.replace("Mds","milliards")
    text3 = text2.replace("Mrds", "milliards")
    text4 = text3.replace("Md", "milliard")
    text5 = text4.replace("Mme", "madame")
    text6 = text5.replace("Dr", "docteur")
    text7 = text6.replace("TTC", "toutes taxes comprises")
    text8 = text7.replace("vol.", "volume")
    return text8

def passe10(self): #ponctuation réliminée, parenthèses ?
    #text = [d.split(r'\w+') for d in self]
    text = self.replace(",",'')
    text1 = text.replace(";",' et ')
    text2 = text1.replace("«",'')
    text3 = text2.replace("»",'')
    text4 = text3.replace(":",'')
    text5 = text4.replace('"','')
    text6 = text5.replace("/",'')
    text7 = text6.replace("(",'')
    text8 = text7.replace(")",'')
    text9 = text8.replace("’","'") #bug d'apostrophe
    text10 = text9.replace("!", "")
    text11 = text10.replace("?", "")
    text12 = text11.replace("œ","oe")
    return text12

def passe15(self): #stopwords
        text1 = self.replace("déjà",'')
        text2 = text1.replace("aussi", '')
        text3 = text2.replace("même", '')
        text4 = text3.replace("mêmes", '')
        text5 = text4.replace("encore", '')
        text6 = text5.replace("ainsi", '')
        text7 = text6.replace("généralement", '')
        text8 = text7.replace("principalement", '')
        text9 = text8.replace("toutefois", '')
        return text9

def passe20(self): #on retire les majuscules
    return self.lower()

def passe25(self): #on retirer les retours charriot + nouvelle ligne
    text = self.replace("|","\n")
    text1 = text.replace("\r"," ")
    text2 = re.sub(r".{1, }", "\n", text1)
    text3 = text2.replace(".", "")
    text4 = re.sub(" et ",".", text3)
    return text4

def passe30(self): #split points
    return self.split("\n")

def passe35(self): #liste mise dans un dico par phrase, une clé, une phrase
    dico = {}
    taille = len(self)
    for i in range(0,taille):
            dico[i] = self[i]
    return dico

def passe40(self): #split espaces
    taille = len(self)
    for i in range(0,taille):
        self[i] = self[i].split(" ")
    return self

def contenu(self,l): #mots non contenus dans le dictionnaire
    text = {}
    a = 0
    j = len(self)
    for k in range(0,j):
        for i in self[k]:
            if l.searching(i)==0 and i!="":
            #if l.searchingPrint(i)==0 and i!="": #si on veut le détail
#                print(i)
                text[a] = i
                a +=1
    return text

def passe50(self,l): # on retire les tirets
    noncontenu = contenu(self,l)
    text = {}
    j = len(self) #nb phrases
    for k in range(0,j):
        text[k] = []
        for i in self[k]: #on parcourt la phrase i->mot
            if i in noncontenu.values():
                i = i.split("-")
                if(len(i)>1): #si le split donne qqchose
                    text[k].append(i[0])
                    text[k].append(i[1])
                else:
                    text[k].append(i[0])
            elif i !='':
                text[k].append(i)
    return text

def passe60(self): # remplacer d', s' et n'
    text = {}
    j = len(self)
    d = "d'"
    s = "s'"
    n = "n'"
    for k in range(0,j):
        text[k] = []
        for i in self[k]:
            if d in i:
                i = i.replace("d'","de ")
                i = i.split(" ")
                text[k].append(i[0])
                text[k].append(i[1])
            elif s in i:
                i = i.replace("s'","se ")
                i = i.split(" ")
                text[k].append(i[0])
                text[k].append(i[1])
            elif n in i:
                i = i.replace("n'","ne ")
                i = i.split(" ")
                text[k].append(i[0])
                text[k].append(i[1])
            else:
                text[k].append(i)
    return text

def passe70(self,dictionnary): # remplacer l'
    text = {}
    j = len(self)
    l = "l'"
    for k in range(0,j):
        text[k] = []
        for i in self[k]:
            if l in i:
                i = i.replace("l'","lo ")
                i = i.split(" ")
                if dictionnary.searchingGender(i[1])=='f':
                    i[0] = i[0].replace("lo","la") #pas les autres lo
                else:
                    i[0] = i[0].replace("lo","le") #pas les autres lo
                text[k].append(i[0])
                text[k].append(i[1])
            else:
                text[k].append(i)
    return text

def passe80(self): #supprimer les phrases vides
    text = {}
    a = -1
    for i in self.values():
        if len(i) != 0:
            a = a + 1
            text[a] = i
    return text

def passes(self,dictionnary):
    a = passe05(self)
    b = passe10(a)
    c = passe15(b)
    d = passe20(c)
    e = passe25(d)
    f = passe30(e)
    g = passe35(f)
    h = passe40(g)
    i = passe50(h,dictionnary)
    j = passe60(i)
    k = passe70(j,dictionnary)
    m = passe80(k)
    return m

#reste = contenu(passe)
#print("mots à ajouter dans le dictionnaire : ")
#for i in reste.values():
#    print(i)

#villes en deux parties ? on analyse deux mots s'ils sont présents
#gérer les adjectifs accordés

if __name__ == "__main__":
    import dico, tag

    with open('entrees/td13.txt','rt', encoding='utf-8') as f:
        data = f.read()

    dictionnary = dico.Lexique()

    #probleme ligne 2
    #probleme avec aujourd'hui ligne 3

    number = 40
    texte =passes(data,dictionnary)
    print(texte[number])
    tags = tag.associeTag(data,texte,dictionnary)
    print(tags[number])
