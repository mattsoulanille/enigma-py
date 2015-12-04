
import argparse



class enigma_cracker(object):
    def __init__(self, ciphertext, wordlist):

        self.ciphertext = ciphertext.upper()
        self.wordlist = [x.rstrip('\n').upper() for x in wordlist.readlines()]

        self.results = []

    def attack(self):
        from itertools import permutations, product
        from enigma import enigma

        rotors = [1,2,3]
        start_points = range(26)
        rotor_perms = [x for x in permutations(rotors, 3)]
        position_choices = [x for x in product(start_points, start_points, start_points)]
        
        runs = 0
        total_runs = len(rotor_perms) * len(position_choices) * len(self.wordlist)
        print "Will now check for matches in " + str(total_runs) + " decodings"
        
        
        for rotor_choices in rotor_perms:
            #print rotor_choices
            for rotor_positions in position_choices:
                
                e = enigma(rotor_choices, rotor_positions)
                matches = 0
                decoded = e.encode(self.ciphertext)

                for word in self.wordlist:
                    if word in decoded:
                        matches += 1
                    runs += 1

                    if runs % 1000000 == 0:
                        print "Tried " + str(runs) + " of " + str(total_runs)
                    

                self.results.append([matches, decoded, e.__repr__()])
                
        self.results.sort(key=lambda x: x[0])

    def print_results(self, count):

        for x in range(count):
            r = self.results[-1-x]
            print "Found " + str(r[0]) + " matches in decoding " + r[1] + "\n Settings: " + str(r[2])

            

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Dictionary attack on an enigma message.')
    parser.add_argument('ciphertext', type=str, help='encoded enigma text to attack')
    parser.add_argument('wordlist', type=file, help='wordlist to search from')

    args = parser.parse_args()
    
    cracker = enigma_cracker(args.ciphertext, args.wordlist)
    cracker.attack()
    cracker.print_results(5)
