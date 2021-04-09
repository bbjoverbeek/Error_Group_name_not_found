#!/usr/bin/python3

import sys
import re


def remove_front_tabs(text):
    """Removes the excessive space in front of a text."""

    smallest_count = 1000

    for line in text:
        front_space_count = len(line) - len(line.lstrip())
        if front_space_count < smallest_count and front_space_count != 1:
            smallest_count = front_space_count

    return [line[smallest_count:] for line in text]


def add_describing_letters(text):
    """Adds the following letters to the start of a sentence,
    based on the amount of space before the text element:

    M for Metadata
    S for Scene boundary
    N for Scene decription
    C for Character name
    D for dialogue
    """

    new_text = []

    metadata = True
    newline_count = 0

    for i in range(len(text)):
        if metadata is True:
            text[i] = re.sub(r'(.+)', r'M|\1', text[i])
            if text[i] != '':
                newline_count = 0
            if text[i] == '':
                newline_count += 1
                if newline_count == 4:
                    if text[i+1] == '' or re.match(r'^(\s)\1{23}[A-Z]+', text[i+1]):
                        newline_count = 0
                    elif re.match(r'^(\s)\1{5}.+', text[i+1]):
                        metadata = False
                    else:
                        metadata = False
        if metadata is False:
            if re.match(r'(\s)\1{23}', text[i]):
                text[i] = re.sub(r'(\s)\1{23}', 'C|\t\t\t\t\t\t', text[i])
            elif re.match(r'(\s)\1{11}', text[i]):
                text[i] = re.sub(r'(\s)\1{11}', 'D|\t\t\t', text[i])
            elif text[i].isupper():
                text[i] = re.sub(r'(.+)', r'S|\t\1', text[i])
            elif text[i] != '':
                text[i] = "N|\t" + text[i]

        new_text.append(text[i])

    return new_text


def main(argv):
    """Takes the file name/-path to the script file,
    applies the functions, and prints the text.
    """

    filename = argv[1]

    with open(filename, 'r') as inp:
        text = inp.readlines()

    text = remove_front_tabs(text)
    text = add_describing_letters(text)

    print('\n'.join(text))


if __name__ == "__main__":
    main(sys.argv)
