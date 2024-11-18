from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)


# databse setup 
def setup_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    # create table if it doesn't exists
    c.execute('''CREATE TABLE IF NOT EXISTS todos 
              ( task TEXT NOT NULL,
                email TEXT NOT NULL,
                priority TEXT NOT NULL
              )''')
    conn.commit()
    conn.close()

# get todo from db
def get_todos():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT task, email, priority FROM todos')
    todos = [{'task': row[0], 'email': row[1], 'priority': row[2]} for row in c.fetchall()]
    conn.close()
    return todos


@app.route('/')
def index():
    todo_list = get_todos()
    return render_template('index.html', todo_list=todo_list)

@app.route('/submit', methods=['POST'])
def submit():
    print(request.form)
    task = request.form.get('task').strip()
    email = request.form.get('email').strip()
    priority = request.form.get('priority')

    # validate task is not empty
    if not task:
        return redirect(url_for('index'))
    
    # basic data validation
    if '@' not in email or '.' not in email:
        return redirect(url_for('index'))
    
    # priortiy validation
    if priority not in ['Low', 'Medium', 'High']:
        return redirect(url_for('index'))
    
    # add item to list in db
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('INSERT INTO todos (task, email, priority) VALUES (?, ?, ?)',
              (task, email, priority))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/clear')
def clear():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('DELETE FROM todos')
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # initilize the db when starting
    setup_db()
    app.run(debug=True)
