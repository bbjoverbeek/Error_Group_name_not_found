from flask import Flask, url_for, render_template, request
import os
from open_subtitles import generate_subtitles

# the virtual invironment for this file has been placed wrong, because
# in order for the order files to work they should be placed inside this
# file

app = Flask(__name__)


app.config['UPLOADED_FILES'] = 'uploads'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if request.files:
            subtitles_file = request.files['subtitles_file']
            subtitles_file.save(os.path.join(app.config['UPLOADED_FILES'],
                                             subtitles_file.filename))
            
            script_file = request.files['script_file']
            script_file.save(os.path.join(app.config['UPLOADED_FILES'],
                                          script_file.filename))

            subtitles_output = generate_subtitles(f"uploads/"
                                                  "{subtitles_file.filename}")

            # here should come the code of the modules editing the files

            return render_template('output.html', subtitles=subtitles_output)
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


if __name__ == "__main__":
    app.run(debug=True)
