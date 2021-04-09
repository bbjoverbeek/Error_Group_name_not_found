#!/usr/bin/python3

import re
import create_subtitles
import label_lines

def test_open_file():

    with open('shrek_subtitles.srt', 'r') as inp:
        full_text = inp.read()
    
    text = create_subtitles.open_file('shrek_subtitles.srt')

    assert len(full_text) == len(text)    


def test_order_text():

    text = create_subtitles.open_file('shrek_subtitles.srt')
    mydict = create_subtitles.order_text(text)
    subtitle_text = re.split("\n\n", text)
    assert len(mydict) == len(subtitle_text)
    for item in mydict:
        assert len(mydict[item]) == 2

        time = mydict[item]['time']
        text = mydict[item]['text']
        m = re.match('([0-9]+:)+[0-9]+,[0-9]+ --> ([0-9]+:)+[0-9]+,[0-9]+', time)
        p = re.search('(<i>)?([A-Za-z0-9,-.!?\']+ *)+[.!?]*....', text)
        assert mydict[item] == {'time': m.group(), 'text': p.group()}

#def test_add_describing_letters():

    #full_text = create_subtitles.open_file('shrek_script.txt')

    #text = label_lines.remove_front_tabs(full_text)
    #text = label_lines.add_describing_letters(text)
    #for line in text:
        #assert line.startswith(('M|', 'C|', 'D|', 'S|', 'N|', ''))
    #assert len(text) == len(full_text)
