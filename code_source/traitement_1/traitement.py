import os
import time
import pandas as pd
import numpy as np
import csv
import math
from nltk.stem.porter import PorterStemmer
import copy

out = "sorties/"

def check_category(row):
    """renvoie la polarite et l'intensite d'une ligne"""
    if row[3] == "N":
        polarite = "passable"
    elif row[3] == "+":
        polarite = "satisfaisant"
    else:
        polarite = "insatisfaisant"

    if row[4] <= 0.3:
        intensite = "assez"
    elif row[4] <= 0.6:
        intensite = ""
    else:
        intensite = "tres"

    return polarite, intensite

def write(path, dic):
    """Permet d'écrire dans path le nombre de fois que le mot doit apparaitre"""
    with open(path, "w", encoding="utf-8", newline="") as f_write:
        for k, v in dic.items():
            writer = csv.writer(f_write)
            for i in range(math.ceil(v*100)): # On fait x100 pour avoir une approximation correcte
                writer.writerow([k])

def combine(dic, stemmer):
    """Fonction permettant d'enlever les mots pluriels du dictionnaire"""
    result = dict()

    for k1, v1 in dic.items():
        tmp = ""
        for k2, v2 in dic.items():
            if stemmer.stem(k1) == stemmer.stem(k2) and k1 != k2:
                # On regarde si les mots ont la meme racine et qu'ils sont différents
                tmp = min(k1, k2, key=len) # On prend le mot le plus court
                result[tmp] = math.log(v1["compte"]+v2["compte"]+math.e)*((v1["coef"]+v2["coef"])/2) #on attribut un nouveau score

        if k1 not in result.keys() and tmp == "":
            result[k1] = math.log(v1["compte"]+math.e)*v1["coef"]
    return result


def check(mot1, mot2, row, dic):
    """Attribut pour chaque mot un compteur et le coefficient selon la table des bigrammes"""
    result = copy.deepcopy(dic)

    if (type(mot1) is float and not(math.isnan(mot1))) or type(mot1) is str:
        if mot1 not in result.keys():
            result[mot1] = dict()
            result[mot1]["compte"] = 0
        result[mot1]["compte"] += 1
        result[mot1]["coef"] = row[7]

    if (type(mot2) is float and not(math.isnan(mot2))) or type(mot2) is str:
        if mot2 not in result.keys():
            result[mot2] = dict()
            result[mot2]["compte"] = 0
        result[mot2]["compte"] += 1
        result[mot2]["coef"] = row[8]

    return result

def normalize(dic) -> dict:
    """Permet de représenter un mot en fonction de son importance"""
    total = sum(dic.values())

    result = dict()
    for k, v in dic.items():
        result[k] = (v*100)/total
    return result


def create_csv(path): 
    """Méthode permettant de créer les fichiers pour le rendu"""

    tres_satisfaisant = dict()
    satisfaisant = dict()
    assez_satisfaisant = dict()

    tres_passable = dict()
    passable = dict()
    assez_passable = dict()

    tres_insatisfaisant = dict()
    insatisfaisant = dict()
    assez_insatisfaisant = dict()

    # On créé un nouveau dossier
    os.mkdir(path[:-4])
    data = pd.read_csv(path)

    stemmer = PorterStemmer()

    for index, row in data.iterrows(): # on vient utiliser le fichier .csv qu'on a créé grace au module ecriture
        polarite, intensite = check_category(row)
        mot1 = row[1]
        mot2 = row[2]
        if polarite == "passable":
            if intensite == "assez":
                assez_passable = check(mot1, mot2, row, assez_passable)
            elif intensite == "":
                passable = check(mot1, mot2, row, passable)
            else:
                tres_passable = check(mot1, mot2, row, tres_passable)
        elif polarite == "satisfaisant":
            if intensite == "assez":
                assez_satisfaisant = check(mot1, mot2, row, assez_satisfaisant)
            elif intensite == "":
                satisfaisant = check(mot1, mot2, row, satisfaisant)
            else:
                tres_satisfaisant = check(mot1, mot2, row, tres_satisfaisant)
        else:
            if intensite == "assez":
                assez_insatisfaisant = check(mot1, mot2, row, assez_insatisfaisant)
            elif intensite == "":
                insatisfaisant = check(mot1, mot2, row, insatisfaisant)
            else:
                tres_insatisfaisant = check(mot1, mot2, row, insatisfaisant)


    # creation des csv

    write(path[:-4]+"/tres_satisfaisant.csv", normalize(combine(tres_satisfaisant, stemmer)))
    write(path[:-4]+"/assez_satisfaisant.csv", normalize(combine(assez_satisfaisant, stemmer)))
    write(path[:-4]+"/satisfaisant.csv", normalize(combine(satisfaisant, stemmer)))

    write(path[:-4]+"/tres_passable.csv", normalize(combine(tres_passable, stemmer)))
    write(path[:-4]+"/assez_passable.csv", normalize(combine(assez_passable, stemmer)))
    write(path[:-4]+"/passable.csv", normalize(combine(passable, stemmer)))

    write(path[:-4]+"/tres_insatisfaisant.csv", normalize(combine(tres_insatisfaisant, stemmer)))
    write(path[:-4]+"/assez_insatisfaisant.csv", normalize(combine(assez_insatisfaisant, stemmer)))
    write(path[:-4]+"/insatisfaisant.csv", normalize(combine(insatisfaisant, stemmer)))

if __name__=="__main__":
    stemmer = PorterStemmer()

    dic = {"ordinateurs":14, "ordinateur":15}

    # print(combine(dic, stemmer))

