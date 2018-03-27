from __future__ import print_function

from flask import Flask, render_template
from flask import Response
from flask import request
from flask import send_file

from main import run

app = Flask(__name__)


@app.route('/')
def form():
    return render_template('form_submit.html')


@app.route('/results/', methods=['POST'])
def results():
    # text = request.form['sentences']
    # return render_template('form_action.html', sentences=text)
    try:
        apply_domination = 'domination' in request.form
        text = str(request.form['sentences'])
        print('Received text = {}'.format(text))
        png_full_filename = run(text, apply_domination)
        return send_file(png_full_filename, mimetype='image/gif')
    except Exception as e:
        print(e)
        ret = 'Hit the endpoint like this http://127.0.0.1:5000?q=QUERY where QUERY is the text' \
              ' such as : Google bought IBM for 10 dollars.'

    resp = Response(ret)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0')
