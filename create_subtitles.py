#!/usr/bin/python3

import sys
import re


def open_file(text):
    """This function opens the srt file"""
    with open(text, 'r') as inp:
        file = inp.read()

    return file


def order_text(text):
    """This function turns the subtitles into a dictionary"""
    mydict = {}

    text = re.split("\n\n", text)

    for item in text:
        item = item.split("\n")

        # The following lines of code connect the different lines of item
        # to the correct name
        number = int(item[0])
        time = item[1]
        text = ' '.join(item[2:])

        # The following lines of code make two dictionaries,
        # with inside_dict sitting inside of mydict
        inside_dict = {'time': time, 'text': text}
        mydict[number] = inside_dict

    return mydict


def main(argv):

    text = open_file(argv[1])
    text_dict = order_text(text)

    # I have added a commented print statement. Remove to test the program.
    # print(text_dict)


if __name__ == "__main__":
    main(sys.argv)
