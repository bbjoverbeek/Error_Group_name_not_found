#!/usr/bin/python3

import argparse
from collections import OrderedDict
from datetime import datetime
from difflib import SequenceMatcher
import json
import nltk
import re
import time as timer

# Remove the comment from the line below if you get the nltk punk error
# nltk.download('punkt')

from create_subtitles import order_text
import label_lines
import script_to_json


def process_subtitle(subtitles_dict, i):
    '''
    Add subtitle sentences, that are split over multiple items, together.
    This is done for better matching.

    Parameters:
        subtitles_dict(dict): all subtitles in a dictionary, done by
            create_subtitles.order_text().
        i(int): The index of the subtitle that is to be combined.

    Returns:
        subtitles_dict(dict): The updated dictionary with the subtitle(i)
        combined with the next subtitle(s) if necessary.
        i(int): The updated index for the while loop.
    '''

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
    '''
    Compares all the sentences of the subtitles to all the sentences
    of the script to find the best matches. Will add the character to
    the subtitles and the time to the script if the match is higher than
    70%. Also calculates the total similarity of the dialogue.

    Parameters:
        script(list): A list of the input script lines
        subtitles(str): A string of the subtitles file

    Returns:
        average_ratio(float): The similarity of the dialogue in percentage
        script_dict(dict): The new script, with timestamps
        subtitles_dict(dict): The new subtitles, with characters
    '''

    subtitles_dict = OrderedDict(order_text(subtitles))

    # Remove the <tags> from the text
    for item in subtitles_dict:
        subtitles_dict[item]['text'] = \
            re.sub('<.*?>', '', subtitles_dict[item]['text'])

    # merge subtitles for complete lines
    subtitle_dict_length = len(subtitles_dict)
    i = 1
    while i < subtitle_dict_length:
        subtitles_dict, i = process_subtitle(subtitles_dict, i)

    # process the script
    no_spaces = label_lines.detect_amount_of_spaces(script)

    dict_spaces_label = \
        label_lines.give_spaces_label(script, no_spaces)

    labelled_script = \
        label_lines.add_describing_letters(script, dict_spaces_label)

    script_dict = script_to_json.converter(labelled_script)

    # loop to compare the texts
    progress = [0, len(subtitles_dict)]

    average_ratio = [0, 0]

    for item in subtitles_dict:

        time = ''

        highest_ratio = 0

        for sub_sentence in subtitles_dict[item]['text']:

            character = ''

            for index in script_dict:

                if 'dialogue' in script_dict[index]:

                    dialogue_text = \
                        nltk.sent_tokenize(script_dict[index]['dialogue'])

                    for d_sentence in dialogue_text:

                        ratio = SequenceMatcher(
                            None,
                            sub_sentence,
                            d_sentence
                            ).ratio()

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

        average_ratio[0] += highest_ratio
        average_ratio[1] += 1

        progress[0] += 1

        print(f'{progress[0]}/{progress[1]}')

    for item in subtitles_dict:
        subtitles_dict[item]['text'] = ' '.join(subtitles_dict[item]['text'])

    average_ratio = (average_ratio[0] / average_ratio[1]) * 100

    return average_ratio, script_dict, subtitles_dict


def create_output_files(new_script, new_subtitles, script_out, subtitles_out):
    '''
    Creates the output files from the dictionaries with the time of creation
    in the filename.

    Parameters:
        new_script(dict): The script to be a json file
        new_subtitles(dict): The subtitles to be a json file
        script_out(bool): Boolean to decide if the file should be created
        subtitles_out(bool): Boolean to decide if the file should be created
    '''

    time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

    if script_out:
        filename = 'script_output_' + time + '.json'
        with open(filename, 'w') as output:
            json.dump(new_script, output, indent=4)

    if subtitles_out:
        filename = 'subtitles_output_' + time + '.json'
        with open(filename, 'w') as output:
            json.dump(new_subtitles, output, indent=4)


def main():
    '''Compares the subtitles and script of a movie to calculate similarity'''

    parser = argparse.ArgumentParser(
        description='Adds the character from the script to the\
            subtitles, and the time from the subtitles to the script.\
            Also calculates the similarity between the dialogue.'
        )
    parser.add_argument(
        'subtitles',
        help='The name or path to a subtitles (.srt) file.')
    parser.add_argument(
        'script',
        help='The name or path to a script (.txt) file.')
    parser.add_argument(
        '-nosub', '--no_subtitles_out',
        help='Use this option to supress the subtitles output',
        default=True)
    parser.add_argument(
        '-noscr', '--no_script_out',
        help='Use this option to supress the script output',
        default=True)

    args = parser.parse_args()

    start_time = timer.time()

    # argument order: subtitles_file script_file script_output subtitles_output
    # argument example: subtitles.txt script.txt True False

    with open(args.subtitles, 'r') as inp:
        subtitles_input = inp.read()

    with open(args.script, 'r') as inp:
        script_input = inp.readlines()

    average_ratio, new_script, new_subtitles = \
        compare_script_to_subtitles(script_input, subtitles_input)

    create_output_files(
        new_script, new_subtitles,
        args.no_subtitles_out, args.no_script_out
        )

    print(
        f'The subtitles were {average_ratio:.2f}% equal to the script',
        'dialogue'
        )

    duration = int((timer.time() - start_time) / 60)
    print(
        f'Running this program wasted {duration} minutes '
        'of your life, congrats!'
        )


if __name__ == "__main__":
    main()
