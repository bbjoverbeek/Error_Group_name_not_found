#!/usr/bin/python3

import sys
import re
from collections import defaultdict, Counter


def detect_amount_of_spaces(text):
    """
    Every script has another number of spaces to differentiate the
    different kinds of information. This function will get all possible
    amounts of spaces before the start of the text.

    Parameters:
        text (list): the text of the script file as a list.

    Returns:
        (list): all the number of spaces that come before the start of a
        piece of text
    """

    pattern = re.compile("^ +[^ \n]")
    list_number_of_spaces = []
    for i in range(100, len(text) // 4):
        # Not looping whole text, because of inefficiency. Starting at
        # 100 to avoid the title.

        spaces = pattern.match(text[i])
        if spaces:
            list_number_of_spaces.append(len(spaces.group()) - 1)
    return sorted(set(list_number_of_spaces))


def give_spaces_label(text, list_number_of_spaces):
    """
    Parameters:
        text (list): the text of the script in a list with every line as
        an item
        list_number_of_spaces (list): It contains all the possible
        amounts of spaces before the line starts. Created by the
        detect_amount_of_spaces function.

    Returns:
        (dict): it the most probable amount of spaces that are used
        before the line that is not metadata. So the spaces before the
        dialoge and the scene discription.
    """

    spaces_and_label = defaultdict()
    spaces_and_label["spaces_N"] = list_number_of_spaces[0]
    spaces_and_label["spaces_S"] = list_number_of_spaces[0]
    # Both the scene discription and the scene boundary always have the
    # least amount of spaces

    for spaces in list_number_of_spaces:
        if spaces > 40:
            # if there are more spaces, it will probably be metadata
            # like "CUT TO:"

            list_number_of_spaces.remove(spaces)
    spaces_and_label["spaces_C"] = max(list_number_of_spaces)
    # the dialoge always comes after a character is named, so that one
    # will be chosen based on that property. Metadata is all the other
    # text.

    pattern_C = re.compile(" {" + str(spaces_and_label["spaces_C"]) +
                           "}[A-Z]*")
    pattern_to_find_spaces_D = re.compile("^ *")
    # Will be used to find the number of spaces that is most common
    # after the name of a character. Most of the time after the name of
    # the character, the dialoge begins.

    spaces_after_dialogue = list()
    # all amounts of spaces after a character name will be placed in
    # this list

    for i in range(100, len(text) // 4):
        # Not looping whole text, because of inefficiency. Starting at
        # 100 to avoid the title.

        match_C = pattern_C.search(text[i])
        if match_C:
            match_D = pattern_to_find_spaces_D.search(text[i + 1])
            spaces_after_dialogue.append(len(match_D.group()))

    counter = Counter(spaces_after_dialogue)
    spaces_and_label["spaces_D"] = max(counter, key=counter.get)
    # Getting the most common amount of spaces, which is probably
    # dialogue.

    return spaces_and_label


def surrounding_empty(i, text):
    """
    This is mostly added to the code for the beginning of mission
    impossible.

    Parameters:
        i (int): index of the current sentence. The surrounding of this
        sentence will be checked if it is empty
        text (list): the text to get the previous and next lines

    Returns:
        (bool): whether the lines were empty "True" and were not
        empty "False"
    """
    counter = 0
    try:
        surrounding_lines = [text[index] for index in [i - 5, i - 4, i - 3,
                                                       i + 3, i + 4]]
        for line in surrounding_lines:
            if line == "\n":
                counter += 1
        if counter == 5:
            return True
        else:
            return False
    except IndexError:
        return False
        # This could happen when the title has the same amount of spaces
        # as the scene discription / boundary.


def add_describing_letters(text, spaces_and_label):
    """
    Adds the following letters to the start of a sentence, based on the
    amount of space before the text element:

    M for Metadata
    S for Scene boundary
    N for Scene decription
    C for Character name
    D for dialogue

    Parameters:
        text (list): the script with each line as a item of a list
        spaces_and_label (dict): the labels and the spaces you would
        expect to be in front of that text

    Returns:
        (str): the text with the labels before each line
    """

    start_s = re.compile(" {" + str(spaces_and_label["spaces_N"]) + "}[^ ?]")
    start_n = re.compile(" {" + str(spaces_and_label["spaces_N"]) + "}[^ ]")
    start_d = re.compile(" {" + str(spaces_and_label["spaces_D"]) + "}[^ ]")
    start_c = re.compile(" {" + str(spaces_and_label["spaces_C"]) + "}[^ ]")
    not_only_spaces = re.compile("[^ \n]+")

    for i in range(len(text)):
        if not_only_spaces.search(text[i]):
            if re.search("THE END", text[i]):
                # The text with "the end" seems to be placed differenly
                # for all movies
                text[i] = re.sub("^ *", "M|\t\t\t\t", text[i])

            elif start_c.match(text[i]) and text[i].upper() == text[i]:
                text[i] = re.sub("^ {" + str(spaces_and_label["spaces_C"])
                                 + "}", "C|\t\t\t\t\t\t", text[i])

            elif start_d.match(text[i]):
                text[i] = re.sub("^ {" + str(spaces_and_label["spaces_D"])
                                 + "}", "D|\t\t\t", text[i])

            elif (start_s.match(text[i]) and text[i].upper() == text[i] and not
                  surrounding_empty(i, text)):
                text[i] = re.sub("^ {" + str(spaces_and_label["spaces_S"])
                                 + "}", "S|\t", text[i])

            elif start_n.match(text[i]) and not surrounding_empty(i, text):
                text[i] = re.sub("^ {" + str(spaces_and_label["spaces_N"])
                                 + "}", "N|\t", text[i])

            elif text[i] != "":
                text[i] = re.sub("^ *", "M|\t\t\t\t", text[i])

    return text


def main(argv):
    """Takes the file name/-path to the script file,
    applies the functions, and prints the text.
    """

    filename = argv[1]

    with open(filename, 'r') as inp:
        text = inp.readlines()

    list_number_of_spaces = detect_amount_of_spaces(text)
    dict_spaces_label = give_spaces_label(text, list_number_of_spaces)

    new_text = "".join(add_describing_letters(text, dict_spaces_label))
    print(new_text)


if __name__ == "__main__":
    main(sys.argv)
