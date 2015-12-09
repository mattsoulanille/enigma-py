


class enigma_fast(object):
    def __init__(self):
        self.reflectors = {"A":"EJMZALYXVBWFCRQUONTSPIKHGD",
                           "B":"YRUHQSLDPXNGOKMIEBFZCWVJAT",
                           "C":"FVPJIAOYEDRZXWGCTKUQSBNMHL"}
        
        self.rotors = {1:("EKMFLGDQVZNTOWYHXUSPAIBRCJ","Q"),
                       2:("AJDKSIRUXBLHWTMCQGZNPYFVOE","E"),
                       3:("BDFHJLCPRTXVZNYEIWGAKMUSQO","V")}

        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.alphabet_dict = {x:y for y, x in enumerate(self.alphabet)}

        self.reflector_lists = {}
        for key, value in self.reflectors.items():
            self.reflector_lists[key] = [self.alphabet_dict[char] for char in value]

        self.encode_lists = {}


        self.size = len(self.alphabet)

        for key, value in self.rotors.items():
            self.encode_lists[key] = ([self.alphabet_dict[char] for char in value[0]], self.alphabet_dict[value[1]])

        self.decode_lists = {}

        for key, value in self.encode_lists.items():
            encode_alphabet = value[0]
            s = sorted([x for x in enumerate(encode_alphabet)], key=lambda k: k[1])
            self.decode_lists[key] = ([x[0] for x in s], value[1])
            
            
        
    def rotor_shift(self, c, position, encode_list):
        size = len(encode_list)
        shifted = (c + position + size) % size
        encoded = encode_list[shifted]
        shifted_back = (encoded - position + size) % size
        return shifted_back

    def step_positions(self, rotor_positions, rotor_ids): # assumes an enigma with 3 rotors

        new_pos = [x for x in rotor_positions] # make a copy so as not to write over rotor_positions

        if new_pos[1] == self.encode_lists[rotor_ids[1]][1]: # the rollover position
            new_pos[1] = (rotor_positions[1] + 1) % self.size
            new_pos[2] = (rotor_positions[2] + 1) % self.size
        
        if new_pos[0] == self.encode_lists[rotor_ids[0]][1]: # the rollover position
            new_pos[1] = (rotor_positions[1] + 1) % self.size

        new_pos[0] = (rotor_positions[0] + 1) % self.size
        
        return new_pos


    def encode(self, to_encode, rotor_ids=[3,2,1], rotor_starts=[0,0,0], reflector_id='B'):

        rotor_positions = [x for x in rotor_starts]
        output = ""
        for char in to_encode:
            u = char.upper()
            if u in self.alphabet:
                
                encoded = self.alphabet_dict[u]
                rotor_positions = self.step_positions(rotor_positions, rotor_ids)
                for i in range(len(rotor_ids)):
                    encoded = self.rotor_shift(encoded, rotor_positions[i], self.encode_lists[rotor_ids[i]][0])

                encoded = self.reflector_lists[reflector_id][encoded]

                for i in reversed(range(len(rotor_ids))):
                    encoded = self.rotor_shift(encoded, rotor_positions[i], self.decode_lists[rotor_ids[i]][0])

                output += self.alphabet[encoded]
        return output


if __name__ == "__main__":
    import pdb
    e = enigma_fast()
