# Error_Group_name_not_found

## Project description
For this project it is our goal to create a prepocessing tool that aligns script and subtitles. The character has to be added to the right subtitle and the timestamp has to be added to the right location in the script. For the script we have to label each line (M, metadata; S, scene boundary; N, scene desription; C, character name; D, dialoge) as well. 
We chose to make a web-based user interface, using Flask.
We have to give the output in a JSON or a CSV format.
And summarize the differences between the script and subtitles, to give a percentage.

## Who did what? 

### Björn 
- Labeled each line of the script (D for Dialoge etc.) using regular expressions.
- Created the program to compare the subtitles and the script with each other.
- Put the timestamp in the script file and the character name in the subtitles.
- Helped creating script_to_json.py

### Dennis 
- Put the '.srt'(the subtitle) file into a dictionary using the format: {number{time: x, text:"x"}}.
- Created the pytests for the python scripts.
- Improved the extra application program.
- Helped with the README.md
- Created script_to_json.py 

### Noor 
- Searched for libraries that would compare two strings or files and give the similarity ratio.
- Came up with different possible options for an extra application of the data.
- Made extra_application.py program for the extra application 
- Fixed different files > pycodestyle

### Oscar 
- Made the website using Flask (user interface).
- Made the label_lines.py script

## How to use the program / reproduce the results:
### Run the website locally
We used a web-based user interface, using flask. On this website it is possible to retreave the program for the script and the subtitles data.

Before trying to access our website, you will need to install some extensions to make it work. This can be done by running the following line of code in your terminal:

```
pip3 install -r requirements.txt
```

Once this is installed, you need to run the following code in the website folder in the terminal to access the website (Opening index.html will not work.):

``` 
source env/bin/activate
```
This will create a virtual environment to run the website with the same flask version that we have used during development.

When you have created a virtual environment, you have to run the following code in order to create a local server. With the virtual server you are able to run this website locally:

```
python3 app.py
```

Flask will provide some information about the local server you are running from your computer. Among the information, a url for the website is given. Open this link via the terminal or copy and paste it into your browser of choice.

Documentation about how to use the website, is available on the website itself. This can be accessed on the documentation page. Among the documentation page there is a page to search for subtitles on opensubtitles.org and for scripts on IMSDb. This read.me can be found on the website as well. Furthermore, you are able to run our compare script on the homepage. After loading you are able to view the output with a user interface and to download the output as JSON files. 

### Unit tests:

If you want to perform unit tests, you would have to make a little change to test.py. We open the film files in every function by using a function from create_subtitles.py. To execute test.py on a film chosen by you, you have to change the filename inside these lines of codes. So:

```
full_text = create_subtitles.open_file('test_files/shrek_subtitles.srt')
```

becomes

```
full_text = create_subtitles.open_file('yourfilm_subtitles.srt')
```

You can run the unit tests by using the following code:
```
pytest test.py
```
