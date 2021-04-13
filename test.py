#!/usr/bin/python3

import re
import create_subtitles
import label_lines
import extra_application


def test_open_file():

    with open('test_files/shrek_subtitles.srt', 'r') as inp:
        full_text = inp.read()

    text = create_subtitles.open_file('test_files/shrek_subtitles.srt')

    assert len(full_text) == len(text)


def test_order_text():

    text = create_subtitles.open_file('test_files/shrek_subtitles.srt')
    mydict = create_subtitles.order_text(text)
    subtitle_text = re.split("\n\n", text)
    assert len(mydict) == len(subtitle_text)
    for item in mydict:
        assert len(mydict[item]) == 2

        time = mydict[item]['time']
        text = mydict[item]['text']
        m = re.match('([0-9]+:)+[0-9]+,[0-9]+ --> ([0-9]+:)+[0-9]+,[0-9]+',
                     time)
        assert mydict[item] == {'time': m.group(), 'text': str(text)}


def test_detect_amount_of_spaces():

    with open('test_files/shrek_script.txt', 'r') as inp:
        full_text = inp.readlines()

    mylist = label_lines.detect_amount_of_spaces(full_text)
    for item in mylist:
        assert item == int(item)


def test_give_spaces_label():

    with open('test_files/shrek_script.txt', 'r') as inp:
        full_text = inp.readlines()

    first_list = label_lines.detect_amount_of_spaces(full_text)
    second_list = label_lines.give_spaces_label(full_text, first_list)

    assert second_list['spaces_N'] == second_list['spaces_S'] == first_list[0]
    assert second_list['spaces_C'] == max(first_list)


def test_add_describing_letters():

    with open('test_files/shrek_script.txt', 'r') as inp:
        full_text = inp.readlines()

    first_list = label_lines.detect_amount_of_spaces(full_text)
    second_list = label_lines.give_spaces_label(full_text, first_list)
    text = ''.join(label_lines.add_describing_letters(full_text, second_list))
    for line in text:
        assert line.startswith(('M|', 'C|', 'D|', 'S|', 'N|', ''))
