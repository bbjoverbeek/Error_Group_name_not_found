import sys
from difflib import SequenceMatcher

from create_subtitles import order_text
from label_lines import add_describing_letters, remove_front_tabs

import pprint


def add_D_to_C(script_list, index, i, script_D_dict, C_line):

    if script_list[index + i] == '':
        return script_D_dict
    else:
        if C_line == True:
            script_D_dict[index] = {}
            script_D_dict[index]['Dialogue'] = ''

            character = script_list[index][2:-1].lstrip()
            script_D_dict[index]['Character'] = str(character)
        else:
            script_D_dict[index]['Dialogue'] += script_list[index + i][2:-1].lstrip()
        i += 1
    
    return add_D_to_C(script_list, index, i, script_D_dict, False)

def main(argv):

    with open(argv[1], 'r') as inp:
        subtitles_str = inp.read()
    subtitles_dict = order_text(subtitles_str)

    with open(argv[2], 'r') as inp:
        script_list = inp.readlines()
    script_list = remove_front_tabs(script_list)
    script_list = add_describing_letters(script_list)

    script_D_dict = {}

    for index in range(len(script_list)):
        if script_list[index].startswith('C|'):

            script_D_dict = add_D_to_C(script_list, index, 0, script_D_dict, True)

    for item in subtitles_dict:

        highest_ratio = 0
        highest_D_no = ''

        subtitle = subtitles_dict[item]['text']

        for dialogue_no in script_D_dict:
            print(dialogue_no)
            dialogue_text = script_D_dict[dialogue_no]['Dialogue']
            print(dialogue_text)
            print(subtitle)
            ratio = SequenceMatcher(None, subtitle, dialogue_text ).ratio()

            if ratio != 0.0:
                print ('WINNER', ratio)
            else:
                print(ratio)


            print()
            if ratio > highest_ratio:
                highest_ratio = ratio
                highest_D_no = dialogue_no

            #print(subtitle, highest_D_no, highest_ratio)
        #print(subtitle, highest_D_no, highest_ratio)

if __name__ == "__main__":
    main(sys.argv)
