class rotor(object):
    def __init__(self, rotor_number, rotor_position, *args):
        # some standard enigma rotors
        self.rotors = {1:("EKMFLGDQVZNTOWYHXUSPAIBRCJ","Q"),
                       2:("AJDKSIRUXBLHWTMCQGZNPYFVOE","E"),
                       3:("BDFHJLCPRTXVZNYEIWGAKMUSQO","V"),
                       4:("ESOVPZJAYQUIRHXLNFTGKDCMWB","J"),
                       5:("VZBRGITYUPSDNHLXAWMJQOFECK","Z")}

        self.rotor = self.rotors[rotor_number]
        self.rotor_number = rotor_number
        
        self.position = rotor_position

        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # Set up a dictionary for going from letter to letter index
        # in the alphabet. Faster than alphabet.index(letter)
        self.alphabet_dict = {x:y for y, x in enumerate(self.alphabet)}

        # The size of the alphabet (in case
        # one wants to use a different alphabet)
        self.size = len(self.alphabet)
                                                                                
        # The left and right sides of the rotor.
        # A rotor is a bijection from the alphabet to the alphabet
        # (it is a funciton that is both one to one and onto). A rotor can
        # be represented as a bijection from a scrambled alphabet to a normal alphabet.
        # In this implementation, the left side is scrambled and
        # the right is normal. It doesn't matter which side is which, however.
        self.left = self.rotors[rotor_number][0]
        # Dictionaries for fast lookup
        self.left_dict =  {x:y for y, x in enumerate(self.left)}

        self.right = self.alphabet
        self.right_dict = {x:y for y, x in enumerate(self.right)}

        # Save the original position so the rotor can be reset to it
        self.original_position = rotor_position


        # The position at which the rotor will trigger the next rotor
        # in the enigma machine to advance
        self.advance_position = self.alphabet_dict[self.rotor[1]]

    def advance_rotor(self):
        # Advances the rotor. Loops around
        self.position = (self.position + 1) % self.size


    # Accounts for the rotor's position offset from the letter A
    # before the encoding happens
    def caesar_shift(self, character):
        new_index = (self.alphabet_dict[character] + self.position) % self.size
        return self.alphabet[new_index]

    # Accounts for the rotor's position offset from the letter A
    # after the encoding happens
    def caesar_shift_back(self, character):
        alphabet_index = self.alphabet_dict[character]
        new_index = (alphabet_index - self.position + self.size) % self.size
        return self.alphabet[new_index]


    # Encodes from right to left (from keypad to reflector direction)
    # determines whether or not the next rotor should advance
    def right_to_left(self, (character, advance) ):
        advance_next = (self.position == self.advance_position)
        if advance:
            self.advance_rotor()

        shifted = self.caesar_shift(character)
        encoded = self.left[self.right_dict[shifted]]
        shifted_back = self.caesar_shift_back(encoded)

        return (shifted_back, advance_next)

    # Encodes from left to right (from reflector to lightbox/keypad)
    def left_to_right(self, character):

        shifted = self.caesar_shift(character)
        encoded = self.right[self.left_dict[shifted]]
        shifted_back = self.caesar_shift_back(encoded)

        return shifted_back

    # Resets the rotor position
    def reset(self):
        self.position = self.original_position

    # string representation...
    def __repr__(self):
        return 'Rotor ' + str(self.rotor_number) + ' Position ' + str(self.position)
    def __str__(self):
        return self.__repr__()
