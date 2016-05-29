# documentazione qui:
# http://flask.pocoo.org/docs/0.11/tutorial/
# http://flask.pocoo.org/docs/0.11/quickstart/
#
# codice inziale copiato da
# https://github.com/pallets/flask/blob/master/examples/flaskr/flaskr.py

# lanciare il server con
# export FLASK_APP=my_application
# export FLASK_DEBUG=1
# flask run
# usare set anziché export su windows

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json

# configurazione

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'database.db'),
    DEBUG=True,
    SECRET_KEY='i am a secret key',
    USERNAME='admin',
    PASSWORD='default'
))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    #retrieved rows are dictionaries
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# codice che gestisce le richieste

def get_question_by_id(id):
    db = get_db()
    cur = db.execute('SELECT * FROM questions WHERE id = ?', (id ,))
    question = cur.fetchone()
    return question

@app.route('/')
def random_question():
    """Takes a random question from the database and shows it"""
    db = get_db()
    cur = db.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT 1;')
    question = cur.fetchone()
    return render_template("question.html", question= question)

@app.route('/admin')
def show_questions():
    """Shows a list of all questions in the database entered, and a form to insert new ones"""
    db = get_db()
    cur = db.execute('select * from questions order by id desc')
    questions = cur.fetchall()
    return render_template('question_list.html', questions=questions)

@app.route('/admin/preview/<question_id>')
def preview_question(question_id):
    question = get_question_by_id(question_id)
    return render_template("question.html", question= question)

@app.route('/admin/add', methods=['POST'])
def add_question():
    db = get_db()
    new_question_data = [request.form['title'], request.form['prompt'], request.form['text'],  request.form['answer']]
    print("assssd")
    db.execute('insert into questions (title, prompt, text, answer) values (?, ?, ?, ?)', new_question_data)
    db.commit()
    print("asad")
    flash('New question was successfully posted')
    return redirect(url_for('show_questions'))

@app.route('/admin/edit/<id>', methods=['GET'])
def edit_question_form(id):
    db = get_db()
    question = get_question_by_id(id)
    if not question:
        print("Question not found")
        abort(404)
    return render_template("question_edit.html", question= question)

@app.route('/admin/edit/<id>', methods=['POST'])
def edit_question(id):
    db = get_db()
    question = get_question_by_id(id)
    if not question:
        print("Question not found")
        abort(404)

    new_question_data = [request.form['title'], request.form['prompt'], request.form['text'],  request.form['answer']]

    db.execute('update questions set title=?, prompt=?, text=?, answer=? where id=?', new_question_data + [id])

    db.commit()

    flash('Question edited')
    return redirect(url_for('show_questions'))

@app.route('/admin/delete/<id>', methods=['POST'])
def delete_question(id):
    db = get_db()
    db.execute("delete from questions where id=?", (id,))
    db.commit()
    return "done"


def check_answer(question, answer):
    """takes a question, the answer provided by the user, and returns True if they match"""
    # TODO Writeme
    return True

@app.route('/answer/<id>', methods=['POST'])
def answer_question(id):
    db = get_db()
    cur = db.execute('SELECT * FROM questions WHERE id = ?', (id ,))

    question = cur.fetchone()
    answer = request.form['answer']

    if(check_answer(question, answer)):
        return "right"
    else:
        return "wrong"
