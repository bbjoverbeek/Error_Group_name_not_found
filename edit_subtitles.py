#!/usr/bin/python3

from create_subtitles import order_text
from label_lines import remove_front_tabs
from label_lines import add_describing_letters
import sys
import re


def open_subtitles(subtitles):
    """This function opens the srt subtitles file"""
    with open(subtitles, 'r') as inp:
        text = inp.read()

    return text

def open_script(script):
	"""This function opens the txt script file"""

    with open(script, 'r') as inp:
        text = inp.readlines()

    return text

def add_character_name(script):
	"""This function collects the character names from the script file"""

    character_name = []
    for line in script:
        if line.startswith("C|"):
        	line = line[2:].lstrip()
        	character_name.append(line)
    
    return character_name

def update_subtitles(characters, subtitles):
	"""This function adds the character names to each subtitle"""

    for element in subtitles:
        for i in range(len(characters)):
    	    new_dict = {"Characters": characters[i]}
    	    element = new_dict

    return subtitles	

def main(argv):

    subtitles = open_subtitles(argv[1])
    ordered_subtitles = order_text(subtitles)
    script = open_script(argv[2])
    clean_script = remove_front_tabs(script)
    ordered_script = add_describing_letters(clean_script)
    characters = add_character_name(ordered_script)
    new_subtitles = update_subtitles(characters, ordered_subtitles)
    print(new_subtitles)

if __name__ == "__main__":
    main(sys.argv)    