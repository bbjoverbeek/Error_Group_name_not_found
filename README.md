# Error_Group_name_not_found

Project description:
For this project it is our goal to create a prepocessing tool that aligns script
and subtitles. The character and timestamp have to be added to the right subtitle.
For the script we have to label each line. (M, metadata; S, scene boundary; N, scene desription;
C, character name; D, dialoge.) 
We chose to make a web-based user interface, using Flask.
We have to give the output in a JSON or a CSV format.
And summarize the differences between the script and subtitles, to give a percentage.

Who did what? 

Björn 
labeled each line of the script (D for Dialoge etc.) 
using regular expressions.

Dennis 
put the '.str'(the subtitle)  file into a dictionary.
Using the format: {number{time: x, text:"x"}}

Noor 
searched for libraries that would compare two strings
or files and give the similarity ratio.
She came up with different possible options for an extra
application data.

Oscar 
made the website using Flask. (user interface).
He made function that takes a url from IMSDb and makes a text file.

How to use the program / reproduce the results: 