import pandas as pd
import unidecode

class Lexicon:
    LEXIQUE_CSV_FR = r'Lib/Lexique/Lexique383.csv'
    
    def __init__(self):
        self.french_lexicon =  self.LEXIQUE_CSV_FR

    def remove_accent(self):
        return unidecode.unidecode(self)
    
    
    def create_lexicon(df):
        hashdict = dict()
        for row in df.itertuples():
            k, v = row[1], (row[2], row[3], row[4], row[5], row[6],
                            row[7], row[8], row[9], row[10], row[11],
                            row[12], row[13], row[14], row[15], row[16])
            if hashdict.get(k) is None:
                hashdict[k] = [v]
            else:
                hashdict[k].append(v)
        return hashdict
    
    @property
    def french_lexicon(self):
        return self._french_lexicon
    
    @french_lexicon.setter
    def french_lexicon(self, csv_file: str):
        lexicon=pd.read_table(csv_file, delimiter = ';', dtype={"1_ortho":str, "2_phon":str, "3_lemme":str,
		"4_cgram":str, "5_genre":str, "6_nombre":str, "7_freqlemfilms2":object, "8_freqlemlivres":object,
		"9_freqfilms2":object, "10_freqlivres":object, "11_infover":str, "12_nbhomogr":object, "13_nbhomoph":object,
        "14_islem":object, "15_nblettres":object, "16_nbphons":object})
        hashdict = dict()
        for row in lexicon.itertuples():
            k, v = row[1], (row[2], row[3], row[4], row[5], row[6],
                            row[7], row[8], row[9], row[10], row[11],
                            row[12], row[13], row[14], row[15], row[16])
            if hashdict.get(k) is None:
                hashdict[k] = [v]
            else:
                hashdict[k].append(v)
        self._french_lexicon = hashdict
    

    
