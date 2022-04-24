from flask import Flask
from flask import render_template

from flask import request

import rythm_semant

app = Flask(__name__)

def get_first_word():
    if not request.args:
        return ""
    return request.args.get('first_word')


@app.route('/')
def index1():
    return index()

@app.route('/index')
def index():
    return render_template("index_poems.html", poem = rythm_semant.create_poem_fin(get_first_word()), first_word = get_first_word())


if __name__ == '__main__':
    app.run(debug=True)



    
