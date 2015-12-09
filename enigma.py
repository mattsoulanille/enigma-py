class rotor_set(object):
    def __init__(self, rotors, reflector):

        from rotor import rotor

        self.rotors = rotors
        self.rotors_reversed = self.rotors[::-1]
        self.reflector = reflector

    def encode_character(self, character):
        input = (character, True) # 'True': Always advance the first rotor

        for i in range(len(self.rotors)):
            rotor = self.rotors[i]

            # if this is a middle rotor, do the double step
            if (i > 0 and i < len(self.rotors) - 1) and (rotor.position == rotor.advance_position):
                input = rotor.right_to_left((input[0], True))
            else:
                input = rotor.right_to_left(input)

        
        output = self.reflector.reflect(input[0])
        
        for rotor in self.rotors_reversed:
            output = rotor.left_to_right(output)

        return output

    def encode(self, encode_string):
        output = ''
        for c in encode_string:
            output += self.encode_character(c)
        return output
    def reset(self):
        for rotor in self.rotors:
            rotor.reset()

    def __repr__(self):
        return 'Rotor Set with rotors ' + self.rotors.__repr__()

    def __str__(self):
        return self.rotors.__repr__()
        
class enigma(object):
    def __init__(self, rotor_choices=[1,2,3], rotor_positions=[0,0,0], reflect_choice='B'):
        from enigma import rotor_set
        from rotor import rotor
        from reflector import reflector
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        rotors = [rotor(r, p) for r, p in zip(rotor_choices, rotor_positions)]
        reflector = reflector(reflect_choice)
        
        self.rotor_set = rotor_set(rotors, reflector)
        
    def encode(self, to_encode):
        formatted = ''
        for c in to_encode:
            u = c.upper()
            if u in self.alphabet:
                formatted += u

        encoded = self.rotor_set.encode(formatted)
        self.rotor_set.reset()
        return encoded

    def decode(self, to_decode):
        return self.encode(to_decode)

    def __repr__(self):
        return 'Enigma with ' + self.rotor_set.__repr__()
    def __str__(self):
        return self.rotor_set.rotors.__repr__()

 

if __name__ == '__main__':
    e = enigma([3,2,1])
