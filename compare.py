#!/usr/bin/python3

import sys
from difflib import SequenceMatcher
import nltk
import re
import json

# Remove the comment from the line below if you get the nltk punk error
#nltk.download('punkt')

from create_subtitles import order_text
from label_lines import *

# Modules for development purposes
import pprint
from collections import OrderedDict

def add_D_to_C(script_list, index, i, script_D_dict, C_line):

    if script_list[index + i] == ' \n':
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


def process_subtitle(subtitles_dict, i):
    '''Add sentences split over multiple items together.'''

    item = i

    subtitles_dict[item]['text'] = str(subtitles_dict[item]['text'])
    subtitles_dict[item]['text'] = nltk.sent_tokenize(subtitles_dict[item]['text'])


    if len(subtitles_dict[item]['text']) > 1:

        return subtitles_dict, i+1


    next_item = i + 1
    next_sentence = nltk.sent_tokenize(subtitles_dict[next_item]['text'])


    if len(nltk.sent_tokenize(' '.join(
                subtitles_dict[item]['text'] + next_sentence
                ))) > 1:

        return subtitles_dict, i+1

    else:

        subtitles_dict[item]['text'] = ' '.join(subtitles_dict[item]['text'] + next_sentence)


        start_time = re.match('.*-->', subtitles_dict[item]['time']).group(0)

        try:
            end_time = re.search('-->.*', subtitles_dict[next_item]['time'])
        except KeyError:
            end_time = re.search('-->.*', subtitles_dict[item]['time'])

        end_time = end_time.group(0)[4:]


        subtitles_dict[item]['time'] = start_time + end_time


        subtitles_dict[next_item] = subtitles_dict[item]
        del subtitles_dict[item]

        return process_subtitle(subtitles_dict, i+1)


def main(argv):

    # argument order: subtitles file   script file   subtitles output   script output   combined output
    # argument example: subtitles.txt script.txt True False True

    output_files = (argv[3], argv[4], argv[5])
    #output_files = ('True', 'True', 'True')

    with open(argv[1], 'r') as inp:
    #with open('shrek_subtitles.srt', 'r') as inp:
        subtitles_str = inp.read()
    subtitles_dict = OrderedDict(order_text(subtitles_str))


    # Remove the <tags> from the text
    for item in subtitles_dict:
        subtitles_dict[item]['text'] = re.sub('<.*?>', '', subtitles_dict[item]['text'])

    # merge subtitles for complete lines
    i = 1
    while i < len(subtitles_dict) +1:
        subtitles_dict, i = process_subtitle(subtitles_dict, i)

    with open(argv[2], 'r') as inp:
    #with open('shrek_script.txt', 'r') as inp:
        script_str = inp.readlines()

    dict_spaces_label = give_spaces_label(script_str, detect_amount_of_spaces(script_str))

    script_list = add_describing_letters(script_str, dict_spaces_label)

    script_D_dict = {}

    for index in range(len(script_list)):
        if script_list[index].startswith('C|'):

            script_D_dict = add_D_to_C(script_list, index, 0, script_D_dict, True)

    total_items = len(subtitles_dict)

    #print (f'total items: {total_items}')

    progress = 0

    average_ratio = [0, 0]

    time = ''
    
    for item in subtitles_dict:

        #print(f'item: {item}')

        highest_ratio = 0

        for sub_sentence in subtitles_dict[item]['text']:

            #print(f'sub_sentence: {sub_sentence}')

            #time = subtitles_dict[item]['time']  

            #print(f'time: {time}')

            character = ''

            for dialogue_no in script_D_dict:

                #print(f'dialogue_no: {dialogue_no}')

                #character = script_D_dict[dialogue_no]['Character']

                #print(f'character: {character}')

                dialogue_text = nltk.sent_tokenize(script_D_dict[dialogue_no]['Dialogue'])

                for D_sentence in dialogue_text:

                    #print(f'D_sentence: {D_sentence}')

                    ratio = SequenceMatcher(None, sub_sentence, D_sentence).ratio()

                    #print(f'ratio: {ratio}')

                    if ratio > highest_ratio:

                        #print(f'highest ratio:{highest_ratio}')

                        highest_ratio = ratio
                        highest_D_match = dialogue_no

                        if ratio >= 0.7:
                            time = subtitles_dict[item]['time']
                            character = script_D_dict[dialogue_no]['Character']

                #character = script_D_dict[dialogue_no]['Character']
                
            if character != '':
                subtitles_dict[item]['character'] = character

            if time != '':
                #print(f'time ({time}) added ye', file=sys.stderr)
                script_D_dict[highest_D_match]['time'] = time
                print(script_D_dict[highest_D_match])

        if highest_ratio >= 0.7:

            average_ratio[0] += highest_ratio 
            average_ratio[1] += 1

        progress += 1

        print(f'{progress}/{total_items}', file=sys.stderr)

        #print(f'subtitle_sentence:\n\t{sub_sentence}\nbest Dialogue match:\n\t{best_D_match}\nratio:{highest_ratio}\n'

    print(average_ratio[0], average_ratio[1], file=sys.stderr)
    average_ratio = (average_ratio[0] / average_ratio[1]) * 100
    print(f'The subtitles were {average_ratio:.2f}% equal to the script', file=sys.stderr)
    

    if output_files[0] == 'True':
        with open('subtitles_output.json', 'w') as output:
            json.dump(subtitles_dict, output, indent=4)
    if output_files[1] == 'True':
        with open('script_output.json', 'w') as output:
            json.dump(script_D_dict, output, indent=4)
    if output_files[2] == 'True':
        with open('combined_output.json', 'w') as output:
            json.dump(script_D_dict, output, indent=4)
            # TODO: this file needs help


if __name__ == "__main__":
    main(sys.argv)