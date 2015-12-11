class rotor_set(object):
    # Holds rotors and deals with how they rotate
    def __init__(self, rotors, reflector):
        from rotor import rotor

        # Save arguments
        self.rotors = rotors
        self.rotors_reversed = self.rotors[::-1]
        self.reflector = reflector

    def encode_char(self, character):
        # Input for rotor encoding
        input = (character, True) # 'True': Always advance the first rotor
        
        for i in range(len(self.rotors)):
            rotor = self.rotors[i]

            # If this is a middle rotor, do the double step
            # See http://users.telenet.be/d.rijmenants/en/enigmatech.htm#steppingmechanism
            if ((i > 0 and i < len(self.rotors) - 1) and 
                (rotor.position == rotor.advance_position)):

                input = rotor.right_to_left((input[0], True))
            else:
                input = rotor.right_to_left(input)

        # Go through the reflector
        output = self.reflector.reflect(input[0])

        # Back through the rotors in revers order
        # and reverse direction
        for rotor in self.rotors_reversed:
            output = rotor.left_to_right(output)

        return output

    # Wraps the encode_char function in a
    # loop to go through a string
    def encode(self, encode_string):
        output = ''
        for c in encode_string:
            output += self.encode_char(c)
        return output
    # Resets all the rotors
    def reset(self):
        for rotor in self.rotors:
            rotor.reset()

    def __repr__(self):
        return ('Rotor Set with rotors ' + self.rotors.__repr__() +
                ' ' + self.reflector.__repr__())


    def __str__(self):
        return self.rotors.__repr__()
        
