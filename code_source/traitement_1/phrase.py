#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def create_sentence(row):
    """Cree une phrase représentant les paramètres de cette derniere"""
    if "NULL" not in row:
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
            intensite = "très"

        if intensite == "":
            phrase = row[1]+" de "+row[2]+" est "+polarite+".\n"
        else:
            phrase = row[1]+" de "+row[2]+" est "+intensite+" "+polarite+".\n"
        return phrase
    return ""
