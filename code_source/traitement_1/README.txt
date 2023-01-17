-- Prérequis pour pouvoir exécuter le programme :

    Installer les packages nécessaires : pip install -r requirements.txt


-- Description des dossiers présents :

    Dossier entrees : contient les fichiers à traiter

    Dossier sorties : contient les resultats du programme
    
        Chaque fois que le programme est lancé, cela créer un dossier avec le nom du fichier en entrée dans le dossier /sorties.
            Dans ce dossier :
                - un fichier .CSV est ajouté contenant le sujet, le COD, l'intensité, la polarité, le score calculé du sujet et du COD en fonction de la table des bigrammes de chaque phrase. Le score est l'inverse de la fréquence des bigrammes du mot.
                - Un dossier contenant plusieurs .csv est créé. Chaque .csv est nommé selon les catégories disponibles.
                    Par exemple :  assez_insatisfaisant.csv
                    Dans chaque .csv, il y a des mots qui sont en nombre représentatif respectivement de leur catégorie.
                - un fichier txt sous le format : nomfichier.jjmmaa-hhmmss.txt
                    Chaque phrase du fichier en entrée est remplacé par une phrase montrant la polarité, ainsi que l'intensité de la phrase
            
                      

    Dossier lexique : contient : - le fichier LexiqueEssai.csv qui est un dictionnaire de mot
                                 - le fichier polarite.csv qui contient une liste de mot et leur polarité
                                 - freq.txt (créé par le programme) qui contient la table des bigrammes avec leur fréquence

-- Description des fichiers présents :

    action.py : permet de déterminer si un mot est négative, positif ou neutre

    dico.py : crée un dictionnaire python à partir du LexiqueEssai.csv

    miseenforme.py : prend le td en entrée et le met en forme (dictionnaire python).

    tag.py : associe les types à chacun des mots du texte en fonction de leur position dans la phrase (mots pouvant avoir plusieurs types dans le Lexique).

    grammaire.py : détermine le maître (le sujet, celui qui fait l'action) et l'esclave (celui qui subit l'action) pour chaque phrase.

    intensite.py : détermine l'intensité (de 0 à 1) de la phrase à l'aide d'adverbes de quantité.

    ecriture.py : écrit un fichier .txt et un dossier classifiant les mots selon différentes catégories

    frequence.py : création du fichier freq.txt contenant la table des bigrammes

    phrase.py : création du contenu du fichier .txt 

    traitement.py : permet de créer le dossier contenant les différentes catégories représentées par des fichiers .csv

    transformation.py : détermine si l'action d'une phrase est la transformation ou juste une action-état


-- Description détaillée de certains modules :

    traitement.py : permet notamment de supprimer les mots pluriels grâce à la racine des mots (utilisation du d'un stemmer)

    frequence.py : attribut à chaque mot un score en fonction de la table des bigrammes. Le score est calculé en faisant l'addition des fréquences tous les bigrammes d'un mot. 
    Puis de diviser cette somme par le nombre de bigramme et de faire l'inverse. Cela permet d'attribuer un score haut à un mot peu usité.


-- Utilisation du programme :

    Lancer la commande 

        python3 main.py entrees/nomfichier 

        nomfichier : nom du fichier à traiter




