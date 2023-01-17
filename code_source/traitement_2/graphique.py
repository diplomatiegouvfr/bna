from utils import normalisation
from calcul import lst_frq
from wordcloud import WordCloud

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import scipy.stats
import seaborn as sns
import plotly.express as px


class SimpleGroupedColorFunc(object):
    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


def create_word_cloud(output_path, frq): # nuage de mots principal
    wordcloud = WordCloud(width = 1250, height = 600, 
                    background_color ='white',
                    colormap=('tab10'),
                    min_font_size = 1,
                    max_font_size = 500,
                    prefer_horizontal=1,
                    margin=4,
                    scale = 5,
                    font_path='Lib/font/Raleway-ExtraBold.ttf').generate_from_frequencies(frq) 
    wordcloud.to_file(output_path)
    return print('Main wordcloud saved as PNG')


def create_gauss_chart(file_without_extension, data):
    
    ordered_values = list(data.values())
    ordered_files = list(data.keys())
    
    # Set styles
    plt.style.use(['seaborn-paper', 'seaborn-whitegrid'])
    plt.style.use(['seaborn'])
    sns.set(palette='colorblind')
    matplotlib.rc("font", family="Arial", size=12)
    
    lst = lst_frq(ordered_values) # values frequencies
    
    # set gauss curve parametres
    x_min = 1
    x_max = len(lst)
    mean = (x_min+x_max)/2
    std = 2
    array = np.linspace(x_min, x_max, len(lst))
    
    normal_law = list(scipy.stats.norm.pdf(array,mean,std))
    standar_deviation = [a_elt - b_elt for a_elt, b_elt in zip(normal_law, lst)]
    positive_values = list(map(lambda x: x*-100 if x>0 else 0, standar_deviation))
    negative_values = list(map(lambda x: x*-100 if x<0 else 0, standar_deviation))
    
    labels = ordered_files # set labels ans values
    x = np.arange(len(labels))  # the label locations
    
    fig = plt.figure()
    ax = plt.subplot()
    
    ax.bar(x, negative_values, width=0.6, color='#004889', label='surreprésentation des réponses')
    ax.bar(x, positive_values, width=0.6, color='#0079E7', label='sous-représentation des réponses')
    yticks = mtick.FormatStrFormatter('%.0f%%')
    ax.yaxis.set_major_formatter(yticks)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation = 40)
    ax.legend()
    
    fig.tight_layout()
    fig.set_size_inches(7.97, 4.72, forward=True)
    fig.savefig('sorties_v4/{}/images/gauss_function_stat.png'.format(file_without_extension), dpi=1000)
    
    return print('Gauss graph saved as PNG')


def create_pie_chart(file_without_extension, outputPNGImagePath, data):

    ordered_values = list(data.values())
    ordered_files = list(data.keys())
    
    categories_de_satisfaction = sum(ordered_values)-ordered_values[6]-ordered_values[7]-ordered_values[8]
    total = sum(ordered_values)
    satisfaction = round((categories_de_satisfaction)*100/total)

    y = []
    y = [int(round(float(x/(sum(ordered_values))),2)*100) for x in ordered_values]
    
    fig = px.pie(
        values = y,
        names = ordered_files,
        color = ordered_files,
        color_discrete_map = {
            'très satisfaisant':'#00ab00',
            'satisfaisant':'#00d500',
            'assez satisfaisant':'#00ff00',
            'très passable':'#FF6C00',
            'passable':'#FF8932',
            'assez passable':'#FFA35F',
            'assez insatisfaisant':'#570000',
            'insatisfaisant':'#ab0000',
            'très insatisfaisant':'#ff0000'
            },
        title = '<b>Indice de satisfaction : {}%</b>'.format(satisfaction),
        width = 1000,
        height = 600)
    
    fig.update_traces(
        texttemplate = "<b>%{percent}</b>",
        textposition = "auto",
        sort = False,
        direction = 'clockwise',
        insidetextfont_color = 'white',
        insidetextfont_family = 'Arial',
        insidetextfont_size = 20,
        textinfo = 'value',
        textfont_size = 20,
        hole = 0.3,
        marker = dict(line = dict(color = 'white', width = 3))
        )
    
    fig.update_layout(
        legend = dict(font = dict(family = "Arial", size = 25, color = "black"),
                      x = 1,
                      y = 0.5,
                      traceorder = "normal",
                      itemsizing = 'constant',
                      itemwidth = 50),
        title = dict(font = dict(family = "Arial", size = 25, color = "black")),
        title_x = 0.4
        )
    
    fig.write_image('sorties_v4/{}/images/ExportedPieChart.png'.format(file_without_extension), scale=5)
    
    return print('Pie chart saved as PNG')


def create_wordcloud_categ(file_without_extension, nom_fichier, dic_couples_mot): # cloud('passable')
    text = normalisation(' '.join(dic_couples_mot.keys()))

    color_map = {
        "assez_satisfaisant": ('#75f075', '#14c214', (248,255,247)),
        "satisfaisant": ('#75f075', '#14c214', (248,255,247)),
        "tres_satisfaisant": ('#75f075', '#14c214', (248,255,247)),
        "assez_passable": ('#ff9d4d', '#e66700', (255,247,247)),
        "passable": ('#ff9d4d', '#e66700', (255,247,247)),
        "tres_passable": ('#ff9d4d', '#e66700', (255,247,247)),
        "assez_insatisfaisant": ('#cd4c4c', '#980101', (255,247,247)),
        "insatisfaisant": ('#cd4c4c', '#980101', (255,247,247)),
        "tres_insatisfaisant": ('#cd4c4c', '#980101', (255,247,247)),
    }
    
    if nom_fichier in color_map:
        color, default_color, background = color_map[nom_fichier]
        grouped_color_func = SimpleGroupedColorFunc({color : text}, default_color)
    
  
    wordcloud = WordCloud(max_words=500, width = 640, height = 400, 
                    background_color = background,
                    color_func=grouped_color_func,
                    min_font_size = 6,
                    max_font_size = 700,
                    prefer_horizontal=1,
                    margin=8,
                    scale = 7,
                    font_path='Lib/font/Raleway-ExtraBold.ttf').generate_from_frequencies(dic_couples_mot) 
    
    wordcloud.to_file(f'sorties_v4/{file_without_extension}/wc_output/wordcloud_output_{nom_fichier}.png') 
  
    return print('<wordcloud {}> saved as PNG'.format(nom_fichier))


def create_time_line_chart(df, data, label, output_path):

    fig = px.area(
        df,
        y = data,
        x = label,
        width = 1250,
        height = 600,
        labels={
            data.name: "Effectifs",
            label.name: "Temporalité de la participation au baromètre"
            }
        )
    
    tick_values = [label[i] for i in range(0, len(label), 24)] # timestamps each 24 hours
    tick_text = [i.strftime("%d/%m/%Y") for i in tick_values] # timestamps at string reduce format
    
    fig.update_layout(
        template = "plotly",
        font = dict(
            family = "Arial",
            size = 19
            ),
        xaxis = dict(
            tickformat = "%d/%m/%Y",
            tickmode = 'array',
            tickvals = tick_values,
            ticktext = tick_text,
            tickangle = 30,
            ticksuffix = " "
            ),
        yaxis = dict(
            ticksuffix = " "
            ),
        yaxis_title=None,
        xaxis_title=None,
        )
    
    fig.write_image(output_path, scale=5)
    
    return print('Line chart saved as PNG')


if __name__ == "__main__":
    pass