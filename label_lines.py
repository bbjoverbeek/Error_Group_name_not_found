# M for Metadata
# S for Scene boundary
# N for Scene decription
# C for Character name
# D for dialogue

import sys
import re

def main(argv):

    filename = argv[1]

    metadata = True
    newline_count = 0

    with open(filename, 'r') as inp:
        for line in inp.readlines():
            if metadata == True:
                line = re.sub(r'(.+)', r'M|\1', line)
                if line == '\n':
                    newline_count += 1 
                    if newline_count == 5:
                        metadata = False
            if metadata == False:
                if re.match(r'(\s)\1{23}', line):
                    line = re.sub(r'(\s)\1{23}', 'C|\t\t\t\t\t\t', line)
                elif re.match(r'(\s)\1{11}', line):
                    line = re.sub(r'(\s)\1{11}', 'D|\t\t\t', line)
                elif line.isupper():
                    line = re.sub(r'(.+)', r'S|\t\1', line)
                elif line != "\n":
                    line = "N|\t" + line

            print(line)

if __name__ == "__main__":
    main(sys.argv)