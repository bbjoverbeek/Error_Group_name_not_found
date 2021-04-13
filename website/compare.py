#!/usr/bin/python3

import sys
from difflib import SequenceMatcher
import nltk
import re
import json
import time as timer
from datetime import datetime

# Remove the comment from the line below if you get the nltk punk error
# nltk.download('punkt')

from create_subtitles import order_text
import label_lines
import script_to_json

# Modules for development purposes
import pprint
from collections import OrderedDict


def process_subtitle(subtitles_dict, i):
    '''Add sentences split over multiple items together.'''

    item = i

    subtitles_dict[item]['text'] = str(subtitles_dict[item]['text'])
    subtitles_dict[item]['text'] = \
        nltk.sent_tokenize(subtitles_dict[item]['text'])

    if len(subtitles_dict[item]['text']) > 1:

        return subtitles_dict, i+1

    next_item = i + 1
    next_sentence = nltk.sent_tokenize(subtitles_dict[next_item]['text'])

    if len(nltk.sent_tokenize(' '.join(
                subtitles_dict[item]['text'] + next_sentence
                ))) > 1:

        return subtitles_dict, i+1

    else:

        subtitles_dict[item]['text'] = \
            ' '.join(subtitles_dict[item]['text'] + next_sentence)

        start_time = re.match('.*-->', subtitles_dict[item]['time']).group(0)

        try:
            end_time = re.search(' -->.*', subtitles_dict[next_item]['time'])
        except KeyError:
            end_time = re.search(' -->.*', subtitles_dict[item]['time'])

        end_time = end_time.group(0)[4:]

        subtitles_dict[item]['time'] = start_time + end_time

        subtitles_dict[next_item] = subtitles_dict[item]
        del subtitles_dict[item]

        return process_subtitle(subtitles_dict, i+1)


def compare_script_to_subtitles(script, subtitles):

    subtitles_dict = OrderedDict(order_text(subtitles))

    # Remove the <tags> from the text
    for item in subtitles_dict:
        subtitles_dict[item]['text'] = \
            re.sub('<.*?>', '', subtitles_dict[item]['text'])

    # merge subtitles for complete lines
    i = 1
    while i < len(subtitles_dict) + 1:
        subtitles_dict, i = process_subtitle(subtitles_dict, i)

    no_spaces = label_lines.detect_amount_of_spaces(script)

    dict_spaces_label = \
        label_lines.give_spaces_label(script, no_spaces)

    labelled_script = \
        label_lines.add_describing_letters(script, dict_spaces_label)

    script_dict = script_to_json.converter(labelled_script)

    total_items = len(subtitles_dict)

    #print (f'total items: {total_items}')

    progress = 0

    average_ratio = [0, 0]

    for item in subtitles_dict:

        highest_ratio = 0

        for sub_sentence in subtitles_dict[item]['text']:

            character = ''

            for index in script_dict:

                if 'dialogue' in script_dict[index]:

                    dialogue_text = \
                        nltk.sent_tokenize(script_dict[index]['dialogue'])

                    for d_sentence in dialogue_text:

                        ratio = \
                            SequenceMatcher(None, sub_sentence, d_sentence).ratio()

                        if ratio > highest_ratio:

                            highest_ratio = ratio
                            highest_D_match = index

                            if ratio >= 0.7:
                                time = subtitles_dict[item]['time']
                                character = script_dict[index]['character']

            if character != '':
                subtitles_dict[item]['character'] = character

            if time != '':
                script_dict[highest_D_match]['time'] = time

        if highest_ratio >= 0.7:

            average_ratio[0] += highest_ratio
            average_ratio[1] += 1

        progress += 1

        print(f'{progress}/{total_items}', file=sys.stderr)

    average_ratio = (average_ratio[0] / average_ratio[1]) * 100

    return average_ratio, script_dict, subtitles_dict


def create_output_files(new_script, new_subtitles, script_out, subtitles_out,
                        filename_sub, filename_script):

    if script_out:
        filename = filename_script + '.json'
        with open(filename, 'w') as output:
            json.dump(new_script, output, indent=4)

    if subtitles_out:
        filename = filename_sub + '.json'
        with open(filename, 'w') as output:
            json.dump(new_subtitles, output, indent=4)


def main(argv):

    start_time = timer.time()

    # argument order: subtitles file   script file   script output   subtitles output
    # argument example: subtitles.txt script.txt True False

    with open(argv[1], 'r') as inp:
        #with open('shrek_subtitles.srt', 'r') as inp:
        subtitles_input = inp.read()

    with open(argv[2], 'r') as inp:
        #with open('shrek_script.txt', 'r') as inp:
        script_input = inp.readlines()

    average_ratio, new_script, new_subtitles = \
        compare_script_to_subtitles(script_input, subtitles_input)

    if argv[3] == 'True':
        script_out = True
    else:
        script_out = False
    if argv[4] == 'True':
        subtitles_out = True
    else:
        subtitles_out = False

    create_output_files(new_script, new_subtitles, script_out, subtitles_out)

    print(f'The subtitles were {average_ratio:.2f}% equal to the script', file=sys.stderr)

    duration = int((timer.time() - start_time) / 60)
    print(f'Running this program wasted {duration} minutes of your life, congrats!', file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv)
