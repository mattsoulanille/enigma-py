
import argparse



class enigma_cracker(object):
    def __init__(self, ciphertext, wordlist):

        self.ciphertext = ciphertext.upper()
        self.wordlist = [x.rstrip('\n').upper() for x in wordlist.readlines()]

        self.results = []
        self.formatted_results = []

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
                        matches += len(word)
                        # make a thing that takes into account the probability of finding a string of letters in a random string of letters.
                    runs += 1

                    if runs % 1000000 == 0:
                        print "Tried " + str(runs) + " of " + str(total_runs) + " " + str(round(float(runs) / total_runs, 2)*100) + "%"
                    

                self.results.append([matches, decoded, e.__repr__()])
                
        self.results.sort(key=lambda x: x[0])


    def format_results(self):

        for x in reversed(self.results):
            self.formatted_results.append( "Found " + str(x[0]) + " letter matches in decoding " + x[1] + " Settings: " + str(x[2]))

    def write_results(self, out_file):
        assert isinstance(out_file, file)

        if self.formatted_results == []:
            self.format_results()
        
        for line in self.formatted_results:
            out_file.write(line+'\n')

    def print_results(self, count):
        if self.formatted_results == []:
            self.format_results()

        for x in range(count):
            print self.formatted_results[x]

            

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Dictionary attack on an enigma message.')
    parser.add_argument('ciphertext', type=str, help='encoded enigma text to attack')
    parser.add_argument('wordlist', type=file, help='wordlist to search from')
    parser.add_argument('-o', '--outfile', type=str, help='write results to a file instead of printing')
    args = parser.parse_args()


    cracker = enigma_cracker(args.ciphertext, args.wordlist)
    cracker.attack()

    if args.outfile is not None:
        import os.path
        assert not os.path.isfile(args.outfile)
        cracker.write_results(open(args.outfile, 'w+'))

    else:
        cracker.print_results(5)
