class enigma(object):
    # Constructs and holds all the parts of the enigma machine
    def __init__(self, rotor_choices=[1,2,3], rotor_positions=[0,0,0], reflect_choice='B', plugboard_pairs=[]):
        from rotor_set import rotor_set
        from rotor import rotor
        from reflector import reflector
        from plugboard import plugboard

        # for sorting out non-alphabetic characters
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Precondition: Rotor choices must have the same length as rotor start
        # positions. (allows for different sizes of enigma machines but is untested)
        assert len(rotor_choices) == len(rotor_positions)
        rotors = [rotor(r, p) for r, p in zip(rotor_choices, rotor_positions)]
        reflector = reflector(reflect_choice)
        
        self.rotor_set = rotor_set(rotors, reflector)
        self.plugboard = plugboard(plugboard_pairs)
        
    def encode(self, to_encode):
        # Remove all non-alphabetic characters
        # and make the string uppercase
        formatted = ''
        for c in to_encode:
            u = c.upper()
            if u in self.alphabet:
                formatted += u

        # Encode the string (or decode. it's the same process)
        switched = self.plugboard.encode(formatted)
        encoded = self.rotor_set.encode(switched)
        switched_back = self.plugboard.encode(encoded)

        # Reset the rotor after
        self.rotor_set.reset()
        return switched_back

    # Decoding is the same as encoding.
    def decode(self, to_decode):
        return self.encode(to_decode)

    def __repr__(self):
        return " ".join(['Enigma with', self.rotor_set.__repr__(), self.plugboard.__repr__()])

    def __str__(self):
        return self.rotor_set.rotors.__repr__()

 

if __name__ == '__main__':
    
    import argparse

    parser = argparse.ArgumentParser(description='Enigma machine emulator')
    parser.add_argument('ciphertext', type=str, help='text to encode')
    parser.add_argument('rotors', type=str, default="1,2,3", help=('enigma rotors to use left to right separated by commas. ' +
                                                  'e.g. "1,2,3" would put rotor 1 by the reflector, rotor 2' +
                                                  ' in the middle, and rotor 3 by the lightbox. Default = "1,2,3"'))
    parser.add_argument('rotor_positions', type=str, default="H,D,X", help=('starting positions for rotors from right to left separated by commas.' +
                                                           'can be integers or letters. ' +
                                                           'e.g. "0,1,2" would set the rotors to "A B C". Default = "H,D,X"'))
    parser.add_argument('reflector', type=str, default="B", help='enigma reflector to use. "A", "B", or "C". Default = "B"')
    parser.add_argument('plugboard_pairs', type=str, nargs='*', default = '', help='enigma plugboard. Add plugs like so. A:B C:D E:Z.... Default is no plugs.')

    args = parser.parse_args()

    rotors = [int(x) for x in args.rotors.split(',')]
    rotors.reverse()
    rotor_positions = args.rotor_positions.split(',')
    rotor_positions.reverse()

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for r in range(len(rotor_positions)):
        if rotor_positions[r].upper() in alphabet:
            rotor_positions[r] = alphabet.index(rotor_positions[r].upper())

    rotor_positions = [int(x) for x in rotor_positions]

    plugs = [[x.split(':')[0].upper(), x.split(':')[1].upper()] for x in args.plugboard_pairs]

    e = enigma(rotors, rotor_positions, args.reflector.upper(), plugs)
    print e.encode(args.ciphertext)
        
