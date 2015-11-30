class reflector(object):
    def __init__(self, r):
        self.reflectors = {"A":"EJMZALYXVBWFCRQUONTSPIKHGD",
                           "B":"YRUHQSLDPXNGOKMIEBFZCWVJAT",
                           "C":"FVPJIAOYEDRZXWGCTKUQSBNMHL"}
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        self.reflect_dict = {}
        for i in range(len(self.alphabet)):
            self.reflect_dict[self.alphabet[i]] = self.reflectors[r][i]

        
    def reflect(self, character):
        return self.reflect_dict[character]
