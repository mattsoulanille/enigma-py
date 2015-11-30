class rotor(object):
    def __init__(self, rotor_number, rotor_position, *args):
        self.rotors = {1:("EKMFLGDQVZNTOWYHXUSPAIBRCJ","Q"),
                       2:("AJDKSIRUXBLHWTMCQGZNPYFVOE","E"),
                       3:("BDFHJLCPRTXVZNYEIWGAKMUSQO","V")}

        self.rotor = self.rotors[rotor_number]

        self.position = rotor_position
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        self.left = self.rotors[rotor_number][0]
        self.right = self.alphabet

        self.original_position = rotor_position
        self.debug = False
        

    def advance_rotor(self):
        self.position = (self.position + 1) % len(self.alphabet)


    # Accounts for half of the rotor's position
    def caesar_shift(self, character):
        new_index = (self.alphabet.index(character) + self.position) % len(self.alphabet)
        if self.debug:
            print 'caesar shift ' + str(character) + ' to ' + str(self.alphabet[new_index])
        return self.alphabet[new_index]

    # Accounts for the other half of the rotor's position
    def caesar_shift_back(self, character):
        alphabet_index = self.alphabet.index(character)
        alphabet_len = len(self.alphabet)
        new_index = (alphabet_index - self.position + alphabet_len) % alphabet_len

        if self.debug:
            print 'caesar shift back ' + str(character) + ' to ' + str(self.alphabet[new_index])
        
        return self.alphabet[new_index]

    def right_to_left(self, (character, advance) ):
        advance_next = False
        if advance:
            if self.alphabet[self.position] == self.rotor[1]:
                advance_next = True
            self.advance_rotor()
            
        shifted = self.caesar_shift(character)
        encoded = self.left[self.right.index(shifted)]
        if self.debug:
            print 'encode rtl ' + shifted + ' to ' + encoded + ' advance_next: ' + str(advance_next)
        shifted_back = self.caesar_shift_back(encoded)

            

        return (shifted_back, advance_next)

    def left_to_right(self, character):
        shifted = self.caesar_shift(character)
        encoded = self.right[self.left.index(shifted)]
        if self.debug:
            print 'encode ltr ' + character + ' to ' + encoded
        shifted_back = self.caesar_shift_back(encoded)

        return shifted_back

    def reset(self):
        self.position = self.original_position
    

