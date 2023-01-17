from lexique import Lexicon

class Word:
    LEXIQUE = Lexicon().french_lexicon
    
    def __init__(self, word):
        self.word = word
        self.exists = word
        self.parametres = word
        
    def check_word(self, word):
        def decorator(func):
            def wrapper():
                if self.french_lexicon.get(word):
                    return func()
                else:
                    print(f"<{word}> don't exist")
            return wrapper
        return decorator
    
    
    @property
    def exists(self):
        return self._exists
    

    @exists.setter
    def exists(self, word):
        if self.LEXIQUE.get(word):
            self._exists = True
        else:
            self._exists = False
        
    
    @property
    def parametres(self):
        return self._parametres
    

    @parametres.setter
    def parametres(self, word):
        self._parametres = self.LEXIQUE.get(word)
    
    @property
    def phon(self):
        return [l[0] for l in self._parametres]
    
    @property
    def lemme(self):
        return [l[1] for l in self._parametres]
    
    @property
    def cgram(self):
        return [l[2] for l in self._parametres]
    
    @property
    def genre(self):
        return [l[3] for l in self._parametres]
    
    @property
    def nombre(self):
        return [l[4] for l in self._parametres]
    
    @property
    def freqlemfilms2(self):
        return [l[5] for l in self._parametres]
    
    @property
    def freqlemlivres(self):
        return [l[6] for l in self._parametres]
    
    @property
    def freqfilms2(self):
        return [l[7] for l in self._parametres]
    
    @property
    def freqlivres(self):
        return [l[8] for l in self._parametres]
    
    @property
    def infover(self):
        return [l[9] for l in self._parametres]
    
    @property
    def nbhomogr(self):
        return [l[10] for l in self._parametres]
    
    @property
    def nbhomoph(self):
        return [l[11] for l in self._parametres]
    
    @property
    def islem(self):
        return [l[12] for l in self._parametres]
    
    @property
    def nblettres(self):
        return [l[13] for l in self._parametres]
    
    @property
    def nbphons(self):
        return [l[14] for l in self._parametres]
    
    
    
    
    
    
    
