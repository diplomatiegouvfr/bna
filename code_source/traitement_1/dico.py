import os
import pickle  # Serialisation
import pandas
import sys
import numpy as np

LEXIQUE_CSV = "lexique/LexiqueEssai.csv"
LEXIQUEFINAL = "lexique/LexiqueFinal.txt"
DICO_FILE = "dict"

class Lexique:
	def __init__(self, load=True): #constructeur
		"""Constructeur des objets de la classe, par defaut essaye de charger le dict plutot que le recreer."""
		if load:
			if os.path.isfile(DICO_FILE):  # Si le fichier existe dans le repertoire courant
				try:
					with open(DICO_FILE, "rb") as dicoBin:
						self.wordsDico = pickle.load(dicoBin) # On charge le dico
						print("Le fichier {} a été chargé pour gagner du temps.".format(DICO_FILE))
				except:
					self.wordsDico = self.createDico(LEXIQUE_CSV) # On le recrée
				return

		self.wordsDico = self.createDico(LEXIQUE_CSV)

	def createDico(self, lexiqueFile):
		"""Creer le dict d['mot'] : ('TYPE', 'mot-de-dependance')."""
		dico = {}
		data = pandas.read_csv(lexiqueFile, dtype={"5_genre":object, "6_nombre":object, "11_infover":object,
		"12_nbhomogr":object, "14_islem":object, "15_nblettres":object, "16_nbphons":object, "Unnamed: 11":object,
		"Unnamed: 12":object, "Unnamed: 13":object})
		i=2
		for tup in data.itertuples():
			if tup[1] not in dico:
				dico[tup[1]] = [(tup[3], tup[2], i, tup[4],str(tup[6]))] #tag, lemme, nb lignes, genre, participe passé
			else:
				dico[tup[1]].append((tup[3], tup[2], i, tup[4], tup[6]))
			i+=1
		return dico

	def saveDico(self):
		"""Enregistre le dict dans un fichier dont le nom est dans DICO_FILE."""
		fileName = DICO_FILE if DICO_FILE != "" else input("Entrez un nom de fichier pour enregistrer le dico : ")
		with open(fileName, "wb") as dicoBin:
			pickle.dump(self.wordsDico, dicoBin, fix_imports=False)

	def contenu(self, mot):
		if self.wordsDico.get(mot):
			return 1
		return 0

	def research(self):
		j=len(sys.argv)
		if j>1:
			for i in range(1,j):
				self.searchingPrint(sys.argv[i])

	def searchingGender(self, mot):
		if(self.contenu(mot)):
			return self.wordsDico.get(mot)[0][3]
		else:
			return "NULL"

	def searchingLemme(self, mot):
		#Retourne le lemme (pays si mot est une capitale)
		if(self.contenu(mot)):
			return self.wordsDico.get(mot)[0][1]
		else:
			return "NULL"

	def searchingLigne(self, mot):
		if(self.contenu(mot)):
			return self.wordsDico.get(mot)[0][2]
		else:
			return "NULL"

	def searchingType(self, mot):
		types = []
		if(self.contenu(mot)):
			i=len(self.wordsDico.get(mot))
			for j in range(0,i):
				types.append(self.wordsDico.get(mot)[j][0])
			return types
		else:
			return "NULL"

	def searchingPP(self, mot): #recherche le temps ou participe passé
		lst = []
		if self.contenu(mot):
			n = len(self.wordsDico.get(mot))
			for i in range(n):
				if type(self.wordsDico.get(mot)[i][4]) is str:
					lst.append(self.wordsDico.get(mot)[i][4])
		if len(lst) != 0:
			return lst
		return "NULL"


	def searchingPrint(self, mot):
		if(self.contenu(mot)):
			i=len(self.wordsDico.get(mot))
			print("- ligne(s) où se trouve le mot (+tag) :",mot)
			for j in range(0,i): #lequel prioriser ?
				print(self.wordsDico.get(mot)[j][2],self.wordsDico.get(mot)[j][0])
			return 1
		else:
			print("- non contenu dans le dictionnaire :",mot)
			return 0

	def searching(self, mot): #contenu 1 pas contenu 0
		if(self.contenu(mot)):
			return 1
		return 0

	def search(self, attributes):
		#Recherche les mots qui correspondent aux attributs donnés
		attr = set(['AUX', 'ADV', 'PRE', 'NOM', 'VER', 'ADJ', 'CON', 'MOIS', 'ART', 'PRO' ,'AUXE'
 ,'CONTI', 'ENTR', 'ORG', 'PAYS', 'CAPITALE', 'DEVISE'])
		lst = []


		soustraction = attr-set(attributes)
		print(soustraction)
		for k in self.wordsDico.keys():
			compt = 0
			for at in attributes:
				for type in self.searchingType(k):
					if (type not in soustraction and at == type):
						compt+=1

			if compt == len(attributes):
				lst.append(k)
		return lst


if __name__ == "__main__": #python mathilde.py arg1 arg2 arg3
	l = Lexique()
	l.research()
	#print(l.searching(""))
