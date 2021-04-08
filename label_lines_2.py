#!/usr/bin/python3
import sys
import re
from collections import defaultdict, Counter


def detect_amount_of_spaces(text):
    """
    :param text: the text of the script file as a list.
    :returns: all the number of spaces that come before the start of a
    piece of text

    Every script has another number of spaces to differentiate the
    different kinds of information. This function will get all possible
    amounts of spaces before the start of the text.
    """

    pattern = re.compile("^ +[^ \n]")
    list_number_of_spaces = list()
    for i in range(100, len(text) // 4):
        # We do not want to loop through the whole text, but we do want
        # to get a good impression so we loop a fourth of the text. The
        # first 100 lines are skipped because they contain a title and
        # some other metadata, which will include a lot of unnecessary
        # spaces in out list.

        spaces = pattern.match(text[i])
        if spaces:
            list_number_of_spaces.append(len(spaces.group()) - 1)
    return sorted(set(list_number_of_spaces))


def give_spaces_label(text, list_number_of_spaces):
    """
    :param text: the text of the script in a list with every line as an
    item
    :param list_number_of_spaces: the list that was created in the
    function above. It contains all the possible amounts of spaces
    before the text starts.

    :returns: a dictionary with the most probable amount of spaces that
    are used before the text that is not metadata. So the spaces before
    the dialoge and the scene discription.
    """

    spaces_and_label = defaultdict()
    spaces_and_label["spaces_N"] = list_number_of_spaces[0]
    spaces_and_label["spaces_S"] = list_number_of_spaces[0]
    # Both the scene discription and the scene boundary always have the
    # least amount of spaces between the start of the line and the start
    # of the text.

    for spaces in list_number_of_spaces:
        if spaces > 40:
            # if there are more spaces between the left side of the
            # document and the text, it will probably be metadata like
            # "CUT TO:"

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
    # the character, the dialoge begins. So finding the most common
    # amount of spaces after the character will be the spaces that are
    # placed before the text of the dialoge.

    list_number_of_spaces_D = list()
    # all amounts of spaces after a character name will be placed in
    # this list

    for i in range(100, len(text) // 4):
        # same as the for loop in detect_amount_of_spaces, getting a
        # good impression of the text without looping through the whole
        # text

        match_C = pattern_C.search(text[i])
        if match_C:
            match_D = pattern_to_find_spaces_D.search(text[i + 1])
            list_number_of_spaces_D.append(len(match_D.group()))
    counter = Counter(list_number_of_spaces_D)
    # This counter is used to count the different amounts of spaces that
    # are used at the start of a new line after a character.

    spaces_and_label["spaces_D"] = max(counter, key=counter.get)
    # Getting the most common amount of spaces.

    return spaces_and_label


def surrounding_empty(i, text):
    """
    :param i: index of the current sentence. The surrounding of this
    sentence will be checked if it is empty
    :param text: the text to get the previous and next lines
    :returns: a boolean whether the lines were empty "True" and were not
    empty "False"

    This is mostly added to the code for the beginning of mission
    impossible.
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


def add_describing_letters(text, spaces_and_label):
    """
    :param text: the text of the script with each line as a item of a
    list
    :param spaces_and_label: a dict with the labels and the spaces you
    would expect to be in front of that text
    :returns: the next as a string with the labels before each line

    Adds the following letters to the start of a sentence,
    based on the amount of space before the text element:

    M for Metadata
    S for Scene boundary
    N for Scene decription
    C for Character name
    D for dialogue
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
                # if has the amount of spaces you would expect and if
                # the text is uppercase
                text[i] = re.sub("^ {" + str(spaces_and_label["spaces_C"])
                                 + "}", "C|\t\t\t\t\t\t", text[i])

            elif start_d.match(text[i]):
                # if the text has the amount of spaces you would expect
                text[i] = re.sub("^ {" + str(spaces_and_label["spaces_D"])
                                 + "}", "D|\t\t\t", text[i])

            elif (start_s.match(text[i]) and text[i].upper() == text[i] and not
                  surrounding_empty(i, text)):
                # if the text has the spaces you would expect and the
                # text is uppercase and if it is not surrounded by empty
                # space
                text[i] = re.sub("^ {" + str(spaces_and_label["spaces_S"])
                                 + "}", "S|\t", text[i])

            elif start_n.match(text[i]) and not surrounding_empty(i, text):
                # if it has the spaces you would expect and is not surrounded
                # by empty space
                text[i] = re.sub("^ {" + str(spaces_and_label["spaces_N"])
                                 + "}", "N|\t", text[i])

            elif text[i] != "":
                # if the text is not empty
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
