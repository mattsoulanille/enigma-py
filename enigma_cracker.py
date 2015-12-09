
import argparse



class enigma_cracker(object):
    def __init__(self, ciphertext, wordlist, use_fast=False):
        
        self.ciphertext = ciphertext.upper()
        self.wordlist = [x.rstrip('\n').upper() for x in wordlist.readlines()]

        self.results = []
        self.formatted_results = []
        self.use_fast = use_fast

    def attack(self):
        from itertools import permutations, product
        from bisect import insort

        if self.use_fast:
            from enigma_fast import enigma_fast
        else:
            from enigma import enigma


        import sys


        
        rotors = [1,2,3,4,5]
        start_points = range(26)
        rotor_perms = [x for x in permutations(rotors, 3)]
        position_choices = [x for x in product(start_points, start_points, start_points)]
        
        runs = 0
        total_runs = len(rotor_perms) * len(position_choices) * len(self.wordlist)
        print "Will now check for matches in " + str(total_runs) + " decodings"


        
        for rotor_choices in rotor_perms:
            #print rotor_choices
            for rotor_positions in position_choices:
                
                if self.use_fast:
                    e = enigma_fast()
                    decoded = e.encode(self.ciphertext, rotor_choices, rotor_positions)

                else:
                    e = enigma(rotor_choices, rotor_positions)
                    decoded = e.encode(self.ciphertext)
                matches = 0


                for word in self.wordlist:
                    if word in decoded:
                        matches += len(word)
                        # make a thing that takes into account the probability of finding a string of letters in a random string of letters.
                    runs += 1

                    if runs % 1000000 == 0:
                        progress_str = "Tried " + str(runs) + " of " + str(total_runs) + " " + str(round(float(runs) / total_runs, 3)*100) + "%"


                        sys.stdout.write('\r')
                        sys.stdout.flush()
                        to_write = progress_str
                        if self.results != []:
                            to_write += "\tHighest Score: " + str(self.results[-1][0]) + "\tResult: " + self.results[-1][1]
                        sys.stdout.write(to_write)



                # sort while adding elements
                insort(self.results, [matches, decoded, rotor_choices, rotor_positions])
                #self.results.append([matches, decoded, rotor_choices, rotor_positions])

        print # print a newline
        #self.results.sort(key=lambda x: x[0])
        

    def format_results(self):

        for x in reversed(self.results):
            
            self.formatted_results.append( "Found " + str(x[0]) + " letter matches in decoding " + x[1] + " Rotors: " + str(x[2]) + " Start positions: " + str(x[3]))

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
    parser.add_argument('-p', '--profiling', dest='profiling', action='store_true', help='print program profiling results too')
    parser.add_argument('-f', '--fast', dest='fast', action='store_true', help='use enigma_fast instead of enigma')
    parser.set_defaults(profiling=False)
    parser.set_defaults(fast=False)
    args = parser.parse_args()


    cracker = enigma_cracker(args.ciphertext, args.wordlist, args.fast)


    if args.profiling:
        import cProfile
        cProfile.run('cracker.attack()')
    else:
        cracker.attack()

    if args.outfile is not None:
        import os.path
        assert not os.path.isfile(args.outfile)
        cracker.write_results(open(args.outfile, 'w+'))

    else:
        cracker.print_results(5)
