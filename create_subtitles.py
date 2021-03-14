#!/usr/bin/python3

import sys
import re


def open_file(text):
    """This function opens the srt file"""
    with open(text, 'r') as inp:
        file = inp.read()

    return file


def order_text(text):
    """This function turns the text into a dictionary"""
    mydict = {}

    # This turns the text into different blocks per subtitle
    text = re.split("\n\n", text)

    for element in text:
        element = element.split("\n")

        # The following lines of code connect the different lines of element
        # to the correct name
        number = element[0]
        time = element[1]
        text = ' '.join(element[2:])

        # The following lines of code make two dictionaries,
        # with inside_dict sitting inside of mydict
        inside_dict = {"time": time, "text": text}
        mydict[number] = inside_dict

    return mydict


def main(argv):

    text = open_file(argv[1])
    text_dict = order_text(text)

    # I have added a commented print statement. Remove to test the program.
    # print(text_dict)


if __name__ == "__main__":
    main(sys.argv)
