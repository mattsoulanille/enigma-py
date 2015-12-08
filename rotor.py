class rotor(object):
    def __init__(self, rotor_number, rotor_position, *args):
        self.rotors = {1:("EKMFLGDQVZNTOWYHXUSPAIBRCJ","Q"),
                       2:("AJDKSIRUXBLHWTMCQGZNPYFVOE","E"),
                       3:("BDFHJLCPRTXVZNYEIWGAKMUSQO","V")}

        self.rotor = self.rotors[rotor_number]
        self.rotor_number = rotor_number

        self.position = rotor_position

        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.alphabet_dict = {x:y for y, x in enumerate(self.alphabet)}

        self.size = len(self.alphabet)
        
        self.left = self.rotors[rotor_number][0]
        self.left_dict =  {x:y for y, x in enumerate(self.left)}

        self.right = self.alphabet
        self.right_dict = {x:y for y, x in enumerate(self.right)}

        self.original_position = rotor_position
        self.debug = False
        
        self.advance_position = self.alphabet_dict[self.rotor[1]]

    def advance_rotor(self):
        self.position = (self.position + 1) % self.size


    # Accounts for half of the rotor's position
    def caesar_shift(self, character):
        new_index = (self.alphabet_dict[character] + self.position) % self.size
        if self.debug:
            print 'caesar shift ' + str(character) + ' to ' + str(self.alphabet[new_index])
        return self.alphabet[new_index]

    # Accounts for the other half of the rotor's position
    def caesar_shift_back(self, character):
        alphabet_index = self.alphabet_dict[character]

        new_index = (alphabet_index - self.position + self.size) % self.size

        if self.debug:
            print 'caesar shift back ' + str(character) + ' to ' + str(self.alphabet[new_index])
        
        return self.alphabet[new_index]

    def right_to_left(self, (character, advance) ):
        advance_next = ((self.position - self.advance_position) + self.size) % self.size

        if advance == 0:
            self.advance_rotor()
        elif advance == 1 and advance_next == 0:
            self.advance_rotor()
                    
            
        shifted = self.caesar_shift(character)
        encoded = self.left[self.right_dict[shifted]]
        
        if self.debug:
            print 'encode rtl ' + shifted + ' to ' + encoded + ' advance_next: ' + str(advance_next)
        shifted_back = self.caesar_shift_back(encoded)

        return (shifted_back, advance_next)

    def left_to_right(self, character):
        shifted = self.caesar_shift(character)
        encoded = self.right[self.left_dict[shifted]]
        if self.debug:
            print 'encode ltr ' + character + ' to ' + encoded
        shifted_back = self.caesar_shift_back(encoded)

        return shifted_back

    def reset(self):
        self.position = self.original_position
    
    def __repr__(self):
        return 'Rotor ' + str(self.rotor_number) + ' Position ' + str(self.position)
    def __str__(self):
        return self.__repr__()
