#!/usr/bin/python3

import sys
import re
import label_lines


def extra_application(new_text):
    """
    Takes the new_text and will count the lines
    of the number of N lines: scene description

    new_text_split are the lines of the
    output of label_lines, but splitted on the newline.

    list_text_count is the counter
    that counts the scene descriptions.

    list_scene_count is the counter
    that counts the scene boundaries.

    average_scene_des is the final number of
    scene description lines per scene boundaries.
    """

    list_text_count = int()
    new_text_split = new_text.split('\n')
    for line in new_text_split:
        if len(line) > 0:
            if line[0] == 'N':
                list_text_count += 1

    list_scene_count = int()
    for line in new_text_split:
        if len(line) > 0:
            if line[0] == 'S':
                list_scene_count += 1

    print("'S' scene boundary      :", list_scene_count)
    print("'N' scene description   :", list_text_count)

    if list_text_count == 0 and list_scene_count == 0:
        return 'Devision by zero: scene boundary and description are 0'
    elif list_scene_count == 0:
        return 'Devision by zero: scene boundary is 0'
    elif list_text_count == 0:
        return 'Devision by zero: scene description is 0'

    average_scene_des = list_text_count / list_scene_count

    return "This movie script has {:.2f} "\
        "scene description lines per scene".format(average_scene_des)


def main(argv):
    """
    Takes the file name/-path to the script file,
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
    print(extra_application(new_text))


if __name__ == "__main__":
    main(sys.argv)
