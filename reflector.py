class reflector(object):
    def __init__(self, r):
        # Precondition: reflector choice must be a string
        assert isinstance(r, str)
        self.reflectors = {"A":"EJMZALYXVBWFCRQUONTSPIKHGD",
                           "B":"YRUHQSLDPXNGOKMIEBFZCWVJAT",
                           "C":"FVPJIAOYEDRZXWGCTKUQSBNMHL"}
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.choice = r # For __repr__
        self.reflect_dict = {}

        # Construct a dictionary from the alphabet to the reflector scramble.
        # (but really, it goes both ways)
        for i in range(len(self.alphabet)):
            self.reflect_dict[self.alphabet[i]] = self.reflectors[r][i]
        
    def reflect(self, character):
        return self.reflect_dict[character]
    def __repr__(self):
        return "Reflector: " + self.choice
    def __str__(self):
        return self.__repr__()
