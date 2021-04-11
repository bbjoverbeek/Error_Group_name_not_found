#!/usr/bin/python3

import label_lines
import sys
import json
from collections import OrderedDict


def converter(text):

    output_dict = OrderedDict()
    counter = int()

    text = text.split('\n')

    for line in text:
        counter += 1
        if line.startswith('S|'):
            output_dict[counter] = {'Scene Boundary': line[2:].lstrip()}
        elif line.startswith('N|'):
            output_dict[counter] = {'Scene Description': line[2:].lstrip()}
        elif line.startswith('M|'):
            output_dict[counter] = {'Metadata': line[2:].lstrip()}
        elif line.startswith('C|'):
            character_dict = add_D_to_C(text, counter, 0, True)
            output_dict[counter] = character_dict


    return output_dict


def add_D_to_C(text, counter, i, C_line):

    if not text[counter + i].startswith('D|'):
        return character_dict
    else:
        if C_line == True:
            character_dict = OrderedDict()
            character = text[counter - 1][2:-1].lstrip()
            second_dict = {'Character': str(character)}
        else:
            dialogue = text[counter - 1 + i][2:-1].lstrip()
            second_dict = {'Dialogue': str(dialogue)}
        character_dict = second_dict
        i += 1
    
    return add_D_to_C(text, counter, i, False)


def main(argv):

    filename = argv[1]

    with open(filename, 'r') as inp:
        text = inp.readlines()

    list_number_of_spaces = label_lines.detect_amount_of_spaces(text)
    dict_spaces_label = label_lines.give_spaces_label(text, list_number_of_spaces)

    new_text = "".join(label_lines.add_describing_letters(text, dict_spaces_label))

    output_dict = converter(new_text)
    print(output_dict)

if __name__ == "__main__":
    main(sys.argv)