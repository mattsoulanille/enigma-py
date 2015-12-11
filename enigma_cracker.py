import argparse

class enigma_cracker(object):
    def __init__(self, ciphertext, analysis_file, use_fast=False):
        
        self.ciphertext = ciphertext.upper()
        self.analysis_file = analysis_file

        self.results = []
        self.formatted_results = []
        self.use_fast = use_fast

    def attack_ngrams(self):
        import math
        
        lines = [x.rstrip('\n').split(' ') for x in self.analysis_file.readlines()]
        ngram_counts = [[x[0].upper(), float(x[1])] for x in lines]
        total = sum([x[1] for x in ngram_counts])
        self.ngrams = [[x[0], math.log10(x[1] / total)] for x in ngram_counts]
        self.ngram_dict = {x:y for x, y in self.ngrams}
        self.ngram_size = len(self.ngrams[0][0])
        self.ngram_floor = math.log10(0.01 / total)
        print self.ngram_floor
        print self.ngram_dict["TION"]
        print self.ngram_dict["AACX"]
        # here is an example recursive implementation of sum_ngram_scores.
        # It is too slow, so I have made another.
        ##########################################################
        # def sum_ngram_scores(decoded, score=None):             #
        #     if type(score) == type(None):                      #
        #         score = 0                                      #
        #     if len(decoded) < 4:                               #
        #         print "Done"                                   #
        #         return score                                   #
        #     else:                                              #
        #         for ngram in self.ngrams:                      #
        #             if ngram[0] == decoded[0:4]:               #
        #                 score += ngram[1]                      #
        #                                                        #
        #         return sum_ngram_scores(decoded[1:], score)    #
        ##########################################################

        # This non-recursive algorithm is also too slow.
        # Maybe the slowness is not from recursion
        #######################################################
        # def sum_ngram_scores(decoded):                      #
        #     score = 0                                       #
        #     for ngram in self.ngrams:                       #
        #         score += ngram[1] * decoded.count(ngram[0]) #
        #     if score == 0:                                  #
        #         return None                                 #
        #     return score                                    #
        #######################################################
        
        # This is much faster because it uses the fact that
        # all the ngrams have the same length.
        # Also, dictionaries are fast
        # algorithm from http://practicalcryptography.com/
        def sum_ngram_scores(decoded): 

            score = 0
            l = len(decoded)
            for i in range(l - self.ngram_size + 1):
                snip = decoded[i:i+self.ngram_size]
                if snip in self.ngram_dict:
                    score += self.ngram_dict[snip]
            if score == 0:
                score = self.ngram_floor
            return score
        
        
        return self.attack(sum_ngram_scores)

    def attack_wordlist(self):

        self.wordlist = [x.rstrip('\n').upper()
                         for x in self.analysis_file.readlines()]

        def count_words(decoded):
            matches = 0
            for word in self.wordlist:
                if word in decoded:
                    matches += len(word)
            return matches

        return self.attack(count_words)

        
    def attack(self, scoring_function):
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
        total_runs = len(rotor_perms) * len(position_choices)
        print "Will now evaluate " + str(total_runs) + " decodings"


        
        for rotor_choices in rotor_perms:

            for rotor_positions in position_choices:
                
                if self.use_fast:
                    e = enigma_fast()
                    decoded = e.encode(self.ciphertext, rotor_choices, rotor_positions)

                else:
                    e = enigma(rotor_choices, rotor_positions)
                    decoded = e.encode(self.ciphertext)
                

                score = scoring_function(decoded)

                runs += 1

                if runs % 100 == 0:
                    progress_str = ("Tried " + str(runs) +
                                    " of " + str(total_runs) +" "
                                    + str(round(float(runs) / total_runs, 3)*100) + "%")


                    sys.stdout.write('\r')
                    sys.stdout.flush()
                    to_write = progress_str
                    if self.results != []:
                        to_write += ("\tHighest Score: " +
                                     str(self.results[-1][0]) +
                                     "\tResult: " +
                                     self.results[-1][1])
                        
                    sys.stdout.write(to_write)

                # sort while adding elements
                insort(self.results, [score, decoded, rotor_choices, rotor_positions])

        print # print a newline
        

    def format_results(self):

        for x in reversed(self.results):
            formatted = ("Found " + str(x[0]) +
                         " letter matches in decoding " + x[1] +
                         " Rotors: " + str(x[2]) +
                         " Start positions: " + str(x[3]))

            self.formatted_results.append(formatted)

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
    parser.add_argument('-q', '--ngrams', dest='ngrams', action='store_true', help='use ngrams instead of wordlist matching')
    parser.set_defaults(profiling=False)
    parser.set_defaults(fast=False)
    parser.set_defaults(ngrams=False)
    args = parser.parse_args()

    cracker = enigma_cracker(args.ciphertext, args.wordlist, args.fast)

    if args.profiling:
        import cProfile
        if args.ngrams:
            cProfile.run('cracker.attack_ngrams()')
        else:
            cProfile.run('cracker.attack_wordlist()')
    else:
        if args.ngrams:
            cracker.attack_ngrams()
        else:
            cracker.attack_wordlist()

    if args.outfile is not None:
        import os.path
        assert not os.path.isfile(args.outfile)
        cracker.write_results(open(args.outfile, 'w+'))

    else:
        cracker.print_results(5)
