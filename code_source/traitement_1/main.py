#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 10/03/2020
#Synopsis : python3 main.py nomfichier
#Quentin Sinh MEAE/DNUM/SIN/sinhq

import dico,miseenforme,tag,grammaire,intensite,action,ecriture, transformation
import sys
import os
import frequence
import traitement

if __name__ == "__main__":
    files = sys.argv
    n = len(files)
    if (n==1):
        print("Entrer un fichier en paramètre")
    for i in range (1, n):
        path = files[i]
        if (os.path.isfile(path)):
            with open(path,'rt', encoding='utf-8') as f:
                data = f.read()

                dictionnary = dico.Lexique()

                texte = miseenforme.passes(data,dictionnary) #mise en forme du texte

                tags = tag.associeTag(data,texte,dictionnary) #on associe les types à chaque mot

                maitre,esclave = grammaire.ME(tags,texte) #on désigne le maitre et l'esclave de chaque phrase

                verbs = grammaire.get_verb(tags, texte)

                inten = intensite.intensite(texte, tags) #intensité de chaque phrase

                act = action.action(texte, dictionnary)

                transf = transformation.transform(texte, dictionnary)

                #On écrit dans le fichier CSV nommé en fonction de la date et de l'heure

                filef = files[i].split(".")[0].split("/")[1]

                freq = frequence.create_table_freq()

                pathfile = ecriture.ecrire(texte,maitre,esclave,act,inten, transf, verbs, filef, freq)

                traitement.create_csv(pathfile)

