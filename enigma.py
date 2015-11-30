class rotor_set(object):
    def __init__(self, rotors, reflector):

        from rotor import rotor



        self.rotors = rotors
        self.rotors_reversed = self.rotors[::-1]
        self.reflector = reflector

    def encode_character(self, character):
        input = (character, True) # 'True': Always advance the first rotor
        for rotor in self.rotors:
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

        
class enigma(object):
    def __init__(self, rotor_choices=[1,2,3], rotor_positions=[0,0,0], reflect_choice='B'):
        from rotor import rotor
        from reflector import reflector
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.rotors = [rotor(r, p) for r, p in zip(rotor_choices, rotor_positions)]
        self.reflector = reflector(reflect_choice)
        
        self.rotor_set = rotor_set(self.rotors, self.reflector)
        
    def encode(self, to_encode):
        formatted = ''
        for c in to_encode:
            u = c.upper()
            if u in self.alphabet:
                formatted += u

        return self.rotor_set.encode(formatted)
    def reset(self):
        self.rotor_set.reset()

if __name__ == '__main__':
    e = enigma([3,2,1])
