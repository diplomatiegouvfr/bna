#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time,csv,os.path
import phrase
import frequence


save_path = 'sorties/' # Nom du dossier de sortie

pronoms = {"vous", "nous", "ils", "il", "elles", "elle", "lui"} # Eliminer les pronoms qui ne sont pas pertinent

def ecrire(texte,maitre,esclave,act,inten, transf, verbs, entry, dic):
    file1 = time.strftime('%d%m%y-%H%M%S') # ajout d'un timestamp

    if not(os.path.exists(os.path.join(save_path, entry))):
        os.mkdir(os.path.join(save_path, entry))

    file = entry+"."+file1+".csv"

    file = os.path.join(entry, file)

    file2 = os.path.join(save_path, file)
    data = ""

    with open(file2, "w", encoding="utf-8") as f_write: # Création du fichier CSV
        writer = csv.writer(f_write)
        writer.writerow(["phrase", "maitre", "esclave", "polarite", "intensite", "transformation", "verbe", "sujetFreq", "CODFreq"])

        for row in zip(texte,maitre.values(),esclave.values(),act.values(),inten.values(), transf.values(), verbs.values()): 
            compt = 0
            if row[1] == "NULL":
                compt+=1
            if row[2] == "NULL":
                compt+=1
            if row[3] == "N":
                compt+=1
            if row[4] == 0.5:
                compt+=1
            if row[5] == "NULL":
                compt+=1
            if row[6] == "NULL":
                compt+=1

            if compt >= 3:
               writer.writerow([row[0]])
            elif row[1] == "NULL" and row[2] == "NULL": #si maitre et esclave sont nuls
                writer.writerow([row[0]])
            else:
                newRow = []

                newRow.append(row[0])
                if row[1] not in pronoms and len(row[1])>5:
                    newRow.append(row[1])
                else:
                    newRow.append("NULL")
                if row[2] not in pronoms and len(row[2])>5:
                    newRow.append(row[2])
                else:
                    newRow.append("NULL")
                newRow.append(row[3])
                newRow.append(row[4])
                newRow.append(row[5])
                newRow.append(row[6])

                newRow.append(frequence.calculate(dic, row[1]))
                newRow.append(frequence.calculate(dic, row[2]))
                writer.writerow(newRow)
                data += phrase.create_sentence(row)

    file3 = os.path.join(entry, entry+"."+file1+".txt") # Création du fichier TXT contenant les phrases

    with open(os.path.join(save_path, file3), "w", encoding="utf-8") as f:
        f.write(data)

    return file2
