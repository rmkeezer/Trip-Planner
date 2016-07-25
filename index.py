import os
import sqlite3
from flask import Flask, request, render_template, redirect, url_for, session, g

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'test.db'),
    SECRET_KEY='development key'
))

@app.route('/trips')
def trips():
    db = get_db()
    cur = db.execute('select name, city from trip where username=\'%s\'' % session['username'])
    entries = cur.fetchall()
    return render_template('trips.html', entries=entries)

@app.route('/attractions')
def attractions():
    db = get_db()
    cur = db.execute('select name, description from attraction order by attr_id desc')
    entries = cur.fetchall()
    return render_template('attractions.html', entries=entries)

@app.route('/users')
def users():
    db = get_db()
    cur = db.execute('select username, first_name, last_name, is_admin from user order by username desc')
    entries = cur.fetchall()
    return render_template('users.html', entries=entries)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db = get_db()
        session['username']=request.form['username']
        session['password']=request.form['password']
        cur = db.execute('select username from user where username=\'%s\' and password=\'%s\''
            % (session['username'], session['password']))
        if cur.fetchall() == []:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            return redirect(url_for('trips'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['username'] = None
    session['password'] = None
    return redirect(url_for('trips'))

@app.route('/user')
@app.route('/user/<username>')
def user(username=None):
    return render_template('user.html', name=username)

@app.route('/mybrowser')
def my_browser():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent

@app.route('/add-trip', methods=['POST'])
def add_trip():
    if not session['logged_in']:
        abort(401)
    db = get_db()
    test = [request.form['name'], request.form['startdate'], request.form['enddate'], 0, request.form['city'], session['username']]
    db.execute('insert into trip (name, start_date, end_date, booked, city, username) values (?, ?, ?, ?, ?, ?)',
                 test)
    db.commit()
    return redirect(url_for('trips'))

def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(app.config['DATABASE'])
    return g.db

if __name__ == '__main__':
    app.run(debug=True)