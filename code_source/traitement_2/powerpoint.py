from pathlib import Path
from calcul import frq_mot_dico
from nltk import sent_tokenize


def check_picture(categ, placeholder_text, placeholder_picture, file_without_extension):
    """Verifie la presence d'une image png dans un fichier, attribution en
       conséquence de l'image en question dans la diapositive ou bien d'un commentaire
       
       Parameters
       ----------
       categ :
         Prend en entrée le nom de la catégorie (exemple: assez_passble)

       placeholder_text :
         Récupère l'emplacement textuel de la diapositive

       placeholder_picture :
         Récupère l'emplacement graphique de la diapositive

       file_without_extension :
         Prend en entrée le nom du fichier png sans l'extension'


       Output
       ----------
       objet de slide *image* ET objet de slide *textuel*
    """
    my_file = Path("sorties_v4/{}/wc_output/wordcloud_output_{}.png".format(file_without_extension, categ))
    picture = ''
    placeholder_text.text = ''
    if my_file.is_file():
        picture = placeholder_picture.insert_picture(r"sorties_v4/{}/wc_output/wordcloud_output_{}.png".format(file_without_extension, categ))
        placeholder_text.text = ''
    if not my_file.is_file():
        placeholder_text.text = 'Données insuffisantes'
        print(categ, "<données insuffisantes>")
    return picture, placeholder_text.text


def slide_text(num, text):
    """Boucle nécessaire pour l'integration de texte"""
    for shape in num.shapes:
        if not shape.has_text_frame:
            continue
        text_frame = shape.text_frame
    text_frame.text = text
    return


def commentaires(mention, placeholder_text2, pic, dict_frequence, expression):
    """Verifie la presence du commentaire 'donnee insuffisante' afin
       d'adapter la mention dans le bas de la diapositive"""
    if pic=='Données insuffisantes' or len(dict_frequence)==0:
        placeholder_text2.text = "\nLes données sont insuffisantes pour effectuer une analyse cohérente."
    elif not pic=='Données insuffisantes':
        expression = expression.capitalize()
        mention1 = mention.replace("_", " ")
        mention1 = mention1.replace("tres", "très")
        placeholder_text2.text = f'\nLes expressions sont classées en fonction de l’appréciation faite. Dans cette partie de l’analyse, l’expression « {expression} » est jugée par les utilisateurs comme étant celle la plus associée à « {mention1} ». '
    return placeholder_text2


def reponse(short_name_file, word, placeholder_text):
    """récupère les phrases en fonction de la présence d'un mot spécifier en paramètre
       dans un fichier pour la slide  20
    
       Parameters
       ----------
       short_name_file :
         Prend en entrée le nom de la catégorie (exemple: BNA_2020_SPM)

       word :
         Prend en entrée le mot clé (exemple: 'Ordinateur')

       placeholder_text :
         Récupère l'emplacement textuel de la diapositive

       Output
       ----------
       retourne les phrases incluant le mot spécifié
    """
    # open and read the file
    file = open('entrees/{}.txt'.format(short_name_file), mode='r', encoding='utf-8').read()
   
    data1 = file.replace('. ', '\n')
    data = data1.replace('\n', '. ')
    sent = sent_tokenize(data)
    sentences = [i for i in sent if len(i) >= 15]
    
    listOfWords = []
    listOfWords.append(word)
    listOfWords = [x.lower() for x in listOfWords]
    reponses = ''
    compteur = 0
    
    a = frq_mot_dico("entrees/{}".format(short_name_file))
    a = dict((k.lower(), v) for k,v in a.items())
    word = str(listOfWords[0])
    freq = str(a.get(word))
    for sentence in sentences:
        if (not str(sentence).find(str(listOfWords[0])) == -1) and compteur < 10:
            reponses = reponses + "« " + sentence + " »" + " (x" + freq + "), "
            compteur = compteur + 1
        else:
            pass
    return reponses


if __name__ == "__main__":
    pass
