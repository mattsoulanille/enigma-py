class plugboard(object):
    def __init__(self, plug_pairs):
        # A dictionary that will hold all the letter swaps
        self.replace = {}

        # for __repr__
        self.plug_pairs = [x for x in plug_pairs] 
        if self.plug_pairs is not []:
            self.plug_pairs.sort()
        
        # Precondition: replacement pairs must have length 2
        assert all((len(x) == 2 for x in self.plug_pairs)) 

                
        for pair in self.plug_pairs:
            pair = [pair[0].upper(), pair[1].upper()]
            assert (pair[0] not in self.replace and
                    pair[1] not in self.replace and
                    pair[0] not in self.replace.values() and
                    pair[1] not in self.replace.values())

            if (pair[0] != pair[1]):  # plugging a plug into itself does nothing

                self.replace[pair[0]] = pair[1]
                self.replace[pair[1]] = pair[0]


    # Puts a character (string of size 1) through the plugboard
    def encode_char(self, char):
        assert isinstance(char, str)
        
        char = char.upper()
        if char in self.replace:
            return self.replace[char]
        else:
            return char
    def encode(self, to_encode):
        assert isinstance(to_encode, str)

        out = ''
        for char in to_encode:
            out += self.encode_char(char)
        return out


    def __repr__(self):
        return "Plugboard: " + self.plug_pairs.__repr__()
    def __str__(self):
        return self.__repr__()
        
if __name__ == '__main__':
    p = plugboard((('a','k'), ('j','z')))
