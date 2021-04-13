#!/usr/bin/python3

import sys
import re


def open_file(filename):
    """This function opens the srt file"""
    with open(filename, 'r') as inp:
        subtitles = inp.read()

    return subtitles


def order_text(text):
    """This function turns the text into a dictionary

    subtitles_dict (dict) = The final dictionary

    subtitle_dict (dict) = The temporary dictionary containing
    the data that will be put into subtitles_dict

    """
    subtitles_dict = {}

    text = re.split("\n\n", text)

    for item in text:
        item = item.split("\n")

        # The following lines of code connect the different lines of item
        # to the correct name
        number = int(item[0])
        time = item[1]
        subtitle_text = ' '.join(item[2:])

        subtitle_dict = {'time': time, 'text': subtitle_text}
        subtitles_dict[number] = subtitle_dict

    return subtitles_dict


def main(argv):

    subtitles = open_file(argv[1])
    subtitle_dict = order_text(subtitles)

    # I have added a commented print statement. Remove to test the program.
    # print(subtitles_dict)


if __name__ == "__main__":
    main(sys.argv)
