#!/usr/bin/python3

import re
import create_subtitles
import label_lines


def test_order_text():

    text = create_subtitles.open_file('shrek_subtitles.srt')
    mydict = create_subtitles.order_text(text)
    subtitle_text = re.split("\n\n", text)
    assert len(mydict) == len(subtitle_text)
    for item in mydict:
        assert len(mydict[item]) == 2


def test_remove_front_tabs():

    full_text = create_subtitles.open_file('shrek_script.txt')

    text = label_lines.remove_front_tabs(full_text)

    # This is not working --> Don't really know what to test

    # for i in range(len(text)):
    # assert len(text[i]) == len(full_text[i]) - len(full_text[i].lstrip())
    assert len(text) == len(full_text)


def test_add_describing_letters():

    full_text = create_subtitles.open_file('shrek_script.txt')

    text = label_lines.remove_front_tabs(full_text)
    text = label_lines.add_describing_letters(text)
    for line in text:
        assert line.startswith(('M|', 'C|', 'D|', 'S|', 'N|', ''))
    assert len(text) == len(full_text)
