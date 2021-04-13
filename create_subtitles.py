#!/usr/bin/python3

import sys
import re


def open_file(filename):
    """This function opens the srt file"""
    with open(filename, 'r') as inp:
        subtitles = inp.read()

    return subtitles


def order_text(text):
    """This function turns the text into a dictionary"""
    script_dict = {}

    # This turns the text into different blocks per subtitle
    text = re.split("\n\n", text)

    for item in text:
        item = item.split("\n")

        # The following lines of code connect the different lines of item
        # to the correct name
        number = int(item[0])
        time = item[1]
        subtitle_text = ' '.join(item[2:])

        # The following lines of code make two dictionaries,
        # with inside_dict sitting inside of script_dict
        subtitle_dict = {'time': time, 'text': subtitle_text}
        script_dict[number] = subtitle_dict

    return script_dict


def main(argv):

    subtitles = open_file(argv[1])
    subtitle_dict = order_text(subtitles)

    # I have added a commented print statement. Remove to test the program.
    #print(subtitles_dict)


if __name__ == "__main__":
    main(sys.argv)
