#!/usr/bin/python3

import label_lines
import sys
import json
from collections import OrderedDict


def converter(script):

    script_dict = OrderedDict()
    line_no = 0

    while line_no < len(script):

        if script[line_no].startswith('S|'):
            script_dict[line_no] = \
                {'scene boundary': script[line_no][2:-1].lstrip()}

        elif script[line_no].startswith('N|'):
            scene_description, line_no = \
                group_scene_description(dict(), script, line_no, 0)
            script_dict[line_no] = scene_description

        elif script[line_no].startswith('M|'):
            script_dict[line_no] = {'metadata': script[line_no][2:-1].lstrip()}

        elif script[line_no].startswith('C|'):
            character_dict, line_no = \
                add_D_to_C(OrderedDict(), script, line_no, 0)
            script_dict[line_no] = character_dict

        line_no += 1

    return script_dict


def add_D_to_C(character_dict, script, line_no, i):

    if not script[line_no + i].startswith('D|') and i != 0:
        return character_dict, (line_no + i - 1)
    else:
        if i == 0:
            character_dict['character'] = script[line_no][2:-1].lstrip()
            character_dict['dialogue'] = ''
        else:
            character_dict['dialogue'] += script[line_no + i][2:-1].lstrip()

    return add_D_to_C(character_dict, script, line_no, i+1)


def group_scene_description(scene_description, script, line_no, i):

    if not script[line_no + i].startswith('N|') and i != 0:
        return scene_description, (line_no + i - 1)
    else:
        if i == 0:
            scene_description['scene description'] = \
                script[line_no + i][2:-1].lstrip()
        else:
            scene_description['scene description'] += \
               script[line_no + i][2:-1].lstrip()

    return group_scene_description(scene_description, script, line_no, i+1)


def main(argv):

    filename = argv[1]

    with open(filename, 'r') as inp:
        script = inp.readlines()

    no_spaces = label_lines.detect_amount_of_spaces(script)

    dict_spaces_label = \
        label_lines.give_spaces_label(script, no_spaces)

    labelled_script = \
        label_lines.add_describing_letters(script, dict_spaces_label)

    script_dict = converter(labelled_script)

    with open('script.json', 'w') as output:
        json.dump(script_dict, output, indent=4)


if __name__ == "__main__":
    main(sys.argv)
