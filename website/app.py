from flask import Flask, url_for, render_template, redirect, request
import os, re, requests


# the virtual invironment for this file has been placed wrong, because
# in order for the order files to work they should be placed inside this
# file

app = Flask(__name__)


app.config['UPLOADED_FILES'] = 'uploads_user'


def get_script_file(link_html):
    content = requests.get(link_html).content
    pattern = re.compile("<pre>.*</pre>")
    match = pattern.search(content)
    html_script = match.group()
    
    text_script = re.sub("<.*?>", "", html_script)
    
    return text_script


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if request.files:
            subtitles_file = request.files['subtitles_file']
            subtitles_file.save(os.path.join(app.config['UPLOADED_FILES'],
                                             "subtitles_file.srt"))
            
            
            # add the option for the user to either paste a url of the
            # webpage containing the script or a input button to upload
            # a .txt file. creating our own .txt file from the html file
            # from imsdb can be done with the get_script_file function.
            
            script_file = request.files['script_file']
            script_file.save(os.path.join(app.config['UPLOADED_FILES'],
                                          "script_file.txt"))
            
            # Check if script and subtitles are from the same movie (maybe)

            with open(f"uploads_user/subtitles_file.srt") as subtitles:
                subtitles_opened = subtitles.readlines()
            # here should come the code of the modules editing the files

            return render_template('output.html', subtitles=subtitles_opened)
            # render_template('output.html', results=results) to add the
            # values of the results into the output.html file
    else:
        return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/documentation')
def documentation():
    return render_template('documentation.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/search_subtitles', methods=['GET', 'POST'])
def search_subtitles():
    if request.method == "POST":
        query = request.form.get('movie_name')
        query = str(query).rstrip()
        return redirect(f"https://www.opensubtitles.org/nl/search2/sublanguageid-eng/moviename-{query}")
    else:
        return render_template('search.html')


if __name__ == "__main__":
    app.run(debug=True)
