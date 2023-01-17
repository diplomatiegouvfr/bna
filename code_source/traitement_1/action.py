#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas

def action(self, dico):
    text = {}
    a = -1
    dictio = mots(self)
    for i in self.values():
        a+=1
        taille = len(i)
        comptplus = 0
        comptmoins = 0
        for j in range(0,taille):
            for k,m in dictio.items():
                if k==dico.searchingLemme(i[j]):
                    if m =="-":
                        comptmoins = comptmoins + 1
                    else:
                        comptplus = comptplus + 1
        if comptmoins != 0 or comptplus != 0:
            if comptmoins > comptplus:
                if negation(i):
                    text[a] = "+"
                else:
                    text[a] = "-"
            elif comptmoins < comptplus:
                if negation(i):
                    text[a] = "-"
                else:
                    text[a] = "+"
            else:
                text[a] = "N"
        else:
            text[a] = "N"
    return text

def mots(self):
    mots = {}

    df = pandas.read_csv("lexique/polarite.csv")

    for tup in df.itertuples():
        if (tup[2] == "positive"):
            mots[tup[1]] = "+"
        else:
            mots[tup[1]] = "-"

    return mots

#0 rien, 1 maximum

def negation(phrase):
    if "ne" in phrase:
        return 1
    return 0
