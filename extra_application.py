#!/usr/bin/python3

import sys
import re
import label_lines


def extra_application(new_text):
    """Takes the new_text and will count the lines
    of the number of N lines: scene description
    """

    list_text_count = int()
    new_text_split = new_text.split('\n')
    for line in new_text_split:
        if len(line) > 0:
            if line[0] == 'N':
                list_text_count += 1
    return list_text_count


def main(argv):
    """Takes the file name/-path to the script file,
    applies the functions, and prints the number of
    scene descriptions in a movie.
    """

    filename = argv[1]

    with open(filename, 'r') as inp:
        text = inp.readlines()

    list_number_of_spaces = \
        label_lines.detect_amount_of_spaces(text)
    dict_spaces_label = \
        label_lines.give_spaces_label(text, list_number_of_spaces)

    new_text = \
        "".join(label_lines.add_describing_letters(text, dict_spaces_label))
    print('This movie script has ', extra_application(new_text), end=" ")
    print(' movie scene description lines.')


if __name__ == "__main__":
    main(sys.argv)
