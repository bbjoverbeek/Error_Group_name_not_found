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

### Dennis 
- Put the '.srt'(the subtitle) file into a dictionary using the format: {number{time: x, text:"x"}}.
- Created the pytests for the python scripts.

### Noor 
- Searched for libraries that would compare two strings or files and give the similarity ratio.
- She came up with different possible options for an extra application of the data.

### Oscar 
- Made the website using Flask (user interface).
- He made a function that takes a url from IMSDb and makes a text file.

## How to use the program / reproduce the results: 
We used a web-based user interface, using flask. On this website it is possible to retreave the program for the script and the subtitles data.

Before trying to access our website, you will need to install some extensions to make it work. This can be done by running the following line of code in your terminal:

```
pip3 install -r requirements.txt
```

Once this is installed, you need to run the following code in the terminal to access the website:

``` 
source env/bin/activate
```
  - This will create a virtual environment to run the website.

When you have created a virtual environment, you have to run the following code in order to open the website:

```
python3 app.py
```

  - Opening index.html will not work.

Additional explanation will be available on the website itself.
