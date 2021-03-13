from logging import error
from flask import Flask, url_for, render_template, redirect, request
import os
import re
import urllib.request


# the virtual invironment for this file has been placed wrong, because
# in order for the order files to work they should be placed inside this
# file

app = Flask(__name__)

app.config['UPLOADED_FILES'] = 'uploads_user'


def get_script_file(script_url):
    """
    The content of the url entered on the website needs to be
    downloaded. This will be a HTML file. All HTML that is not part of
    the script needs to be removed.
    
    :param script_url: the url where the script is stored.
    :returns: a string that is the script, which needs to be stored as
    a text file.
    """
    response = urllib.request.urlopen(script_url)
    html = str(response.read().decode('iso-8859-1')).replace("\n", "qq11qq")
    # I do not think any movie has "qq11qq" in their script, at
    # least I hope

    html = re.sub("<!--.*?-->", "", html)
    html = re.sub("<title.*?</title>", "", html)
    # removing some html that is not part of the script, but is in the
    # body part that should contain the script.

    pattern = re.compile("<pre>.*</pre>")
    match = pattern.search(html)

    try:
        html = match.group().replace("qq11qq", "\n")
    except AttributeError:
        error_message = """This URL did not work. Please try another
        URL and make sure the URL is from IMSDb or try to upload a file 
        instead."""
        return error_message
    # This happens when the content between the tags "<pre>.*</pre>",
    # which should be the script, cannot be found

    script_file = re.sub("<.*?>", "", html)
    return script_file


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        subtitles_file = request.files['subtitles_file']
        script_file = request.files['script_file']
        script_url = request.form['url_script']
        # Already giving variables the input the user provided

        no_file_string = "<FileStorage: '' ('application/octet-stream')>"

        if str(subtitles_file) == no_file_string:
            # With those ' and " it was difficult to use the conventions
            # of pycodestyle
            error_message = """You did not upload a subtitles file. In order
            for the generator to work, subtitles need to be uploaded."""

            return render_template('error.html', error_message=error_message)

        subtitles_file.save(os.path.join(app.config['UPLOADED_FILES'],
                                         "subtitles_file.srt"))

        if not str(script_file) == no_file_string:
            script_file.save(os.path.join(app.config['UPLOADED_FILES'],
                                          "script_file.txt"))
            # Saving the uploaded script.
        elif not script_url == "":
            script_file = get_script_file(script_url)
            if "This URL did not work." in script_file:
                print("hello")
                return render_template('error.html', error_message=script_file)
            else:
                print("not the good one")
                with open("uploads_user/script_file.txt", "w") as file:
                    file.write(script_file)
                    # Saving the cleaned HTML file to script_file.txt
        else:
            error_message = """No URL or script file has been submitted. To
            make the program work one of them needs to be submitted."""
            return render_template('error.html', error_message=error_message)

        with open("uploads_user/subtitles_file.srt") as subtitles:
            subtitles_opened = subtitles.readlines()

        with open("uploads_user/script_file.txt") as script:
            script_opened = script.readlines()
        # All outcomes url and normal files are saved as files, so they
        # can be treated the same from now on

        return render_template('output.html', subtitles=subtitles_opened,
                               script=script_opened)

        # Check if script and subtitles are from the same movie (maybe
        # here should come the code of the modules editing the file

    else:
        return render_template('index.html')
        # so the homepage gets loaded when clicking on a link to the
        # page


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
        return redirect("https://www.opensubtitles.org/nl/search2/"
                        f"sublanguageid-eng/moviename-{query}")
    else:
        return render_template('search.html')


@app.route('/error')
def error_page():
    return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=True)
