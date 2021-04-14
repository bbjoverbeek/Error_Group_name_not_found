from logging import error
from flask import Flask, json, render_template, redirect, request
from flask import send_file, url_for
import os
import re
import urllib.request
import jinja2
# I think this one was necessary for some of the jinja code inside the
# html
from compare import compare_script_to_subtitles, create_website_output_files
# create_website_output_files does exist
from collections import OrderedDict


app = Flask(__name__)
app.config['UPLOADED_FILES'] = 'uploads_user'
app.config['SECRET_KEY'] = "finalprojectadvancedprogrammingrejklsfjlklfkdklsfj"


def has_character_name(item):
    key_name = "character"
    if key_name in item[1]:
        return True
    else:
        return False


def is_type(item, type_info):
    key_name = type_info
    if key_name in item[1]:
        return True
    else:
        return False


app.add_template_filter(has_character_name)
app.add_template_filter(is_type)


# SCRIPT AND SUBTITLES CODE

def get_script_file(script_url):
    """
    The content of the url entered on the website needs to be
    downloaded. This will be a HTML file. All HTML that is not part of
    the script needs to be removed.

    :param script_url: the url where the script is stored.
    :returns: a string that is the script, which needs to be stored as
    a text file.
    """
    opener = urllib.request.FancyURLopener({})
    url = script_url
    response = opener.open(url)

    # response = urllib.request.urlopen(script_url)
    html = str(response.read().decode('iso-8859-1')).replace("\n", "qq11qq")
    # I do not think any movie has "qq11qq" in their script, at
    # least I hope
    # the decoding is the one that is used on the website of imsdb.

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


# .
# .
# .
# .
# .
# Here is some whitespace to differentiate the server code from the
# subtitles and script code
# .
# .
# .
# .
# .

# THE ROUTES FOR THE WEBSITE

process_counter = 0
# Because this website will probalbly be deployed on heroku, we need to
# take into account the available space that we can use for free. That
# is why there will not be more than 5 files.


@app.route('/', methods=['GET', 'POST'])
def index():

    global process_counter

    if request.method == "POST":

        subtitles_file = request.files['subtitles_file']
        # Already giving variables the input the user provided
        no_file_string = "<FileStorage: '' ('application/octet-stream')>"
        # If the user did not give us a file, we will get this message,
        # so when we get this message the user did not give us a file

        if str(subtitles_file) == no_file_string:
            error_message = """You did not upload a subtitles file. In order
            for the generator to work, subtitles need to be uploaded."""
            return redirect(url_for('error_page', error_message=error_message))

        subtitles_file.save(os.path.join(app.config['UPLOADED_FILES'],
                                         f"subtitles_file"
                                         f"{process_counter}.srt"))

        script_file = request.files['script_file']
        script_url = request.form['url_script']
        # Already giving variables the input the user provided

        if not str(script_file) == no_file_string and not script_url == "":
            error_message = """Both a file and a URL were submitted to the
            form. Hard refresh the page the home page (ctr + shift + r on
            windows, or command + shift + r on mac) if the filenames and the
            url are still visible to delete both inputs and start over. """
            return redirect(url_for('error_page', error_message=error_message))
        elif not str(script_file) == no_file_string:
            script_file.save(os.path.join(app.config['UPLOADED_FILES'],
                                          f"script_file{process_counter}.txt"))
            # Saving the uploaded script.
        elif not script_url == "":
            script_file = get_script_file(script_url)
            if "This URL did not work." in script_file:
                return redirect(url_for('error_page',
                                        error_message=script_file))
            else:
                with open(f"uploads_user/script_file{process_counter}"
                          ".txt", "w") as file:
                    file.write(script_file)
                    # Saving the cleaned HTML file to script_file.txt

        else:
            error_message = """No URL or script file has been submitted. To
            make the program work one of them needs to be submitted."""
            return redirect(url_for('error_page', error_message=error_message))

        subtitles_file_option = request.form.get("checkbox1")
        script_file_option = request.form.get("checkbox2")

        if subtitles_file_option == "on":
            subtitles_file_option = True
        else:
            subtitles_file_option = False
        if script_file_option == "on":
            script_file_option = True
        else:
            script_file_option = False

        # Check if script and subtitles are from the same movie (maybe
        # here should come the code of the modules editing the file

        return redirect(url_for('process_files',
                                script_file_option=script_file_option,
                                subtitles_file_option=subtitles_file_option))

    else:
        return render_template('index.html')
        # so the homepage gets loaded when clicking on a link to the
        # page


@app.route('/process_files/<script_file_option>/<subtitles_file_option>')
def process_files(script_file_option, subtitles_file_option):

    global process_counter

    with open(f"uploads_user/subtitles_file{process_counter}.srt",
              "r", encoding='utf-8') as subtitles:
        subtitles_opened = subtitles.read()

    with open(f"uploads_user/script_file{process_counter}.txt", "r",
              encoding='utf-8') as script:
        script_opened = script.readlines()
    # All outcomes url and normal files are saved as files, so they
    # can be treated the same from now on

    average_ratio, new_script, new_subtitles = compare_script_to_subtitles(
        script_opened, subtitles_opened)

    create_website_output_files(new_script, new_subtitles, script_file_option,
                                subtitles_file_option,
                                f"downloads_user/script{process_counter}",
                                f"downloads_user/subtitles{process_counter}")

    normal_script_dict = dict(new_script)
    normal_subtitles_dict = dict(new_subtitles)

    process_number = process_counter

    process_counter += 1
    if process_counter == 5:
        process_counter = 0

    return render_template('output.html', average_ratio=average_ratio,
                           script_dict=normal_script_dict,
                           subtitles_dict=normal_subtitles_dict,
                           process_number=str(process_number),
                           script_file_option=str(script_file_option),
                           subtitles_file_option=str(subtitles_file_option))


@app.route('/downloads_user/<filename>')
def download_file(filename):
    return send_file(f"downloads_user/{filename}", as_attachment=True)


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
        return redirect(url_for("search"))


@app.route('/error/<error_message>')
def error_page(error_message):
    return render_template('error.html', error_message=error_message)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    # If you are running this file and you know the ip-address of your
    # computer (connected to your router), you can open the website with
    # the following url: http://<your_ip-address>:5000
