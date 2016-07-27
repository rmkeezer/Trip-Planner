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
    cur = db.execute('select conf_num, name, city from trip where username=\'%s\'' % session['username'])
    entries = cur.fetchall()
    return render_template('trips.html', entries=entries)

@app.route('/attractions')
@app.route('/attractions/<conf_num>')
def attractions(conf_num=None):
    db = get_db()
    cur = db.execute('select attr_id, name, description, opening_time, closing_time, cost, reserve_compulsory, trans_name, addr_id from attraction')
    entries = cur.fetchall()
    cur = db.execute('select addr_id, num, street, city, state, zip, country from address')
    addresses = cur.fetchall()
    addrs = []
    for address in addresses:
        addrs.append((address[0], str(address[1])+' '+address[2]+', '+address[3]+', '+address[4]+', '+str(address[5])+', '+address[6]))
    newentries = []
    for entry in entries:
        entry += ([a[1] for a in addrs if a[0] == entry[8]][0],)
        print(entry)
        newentries.append(entry)
    return render_template('attractions.html', entries=newentries, conf_num=conf_num, addrs=addrs)

@app.route('/users')
def users():
    db = get_db()
    cur = db.execute('select username, first_name, last_name, is_admin from user order by username desc')
    entries = cur.fetchall()
    return render_template('users.html', entries=entries)

@app.route('/addresses')
def addresses():
    db = get_db()
    cur = db.execute('select addr_id, num, street, city, state, zip, country from address')
    entries = cur.fetchall()
    return render_template('addresses.html', entries=entries)

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

@app.route('/add-address', methods=['POST'])
def add_address():
    if not session['logged_in']:
        abort(401)
    db = get_db()
    test = [request.form['num'], request.form['street'], request.form['city'], request.form['state'], request.form['zip'], request.form['country']]
    db.execute('insert into address (num, street, city, state, zip, country) values (?, ?, ?, ?, ?, ?)',
                 test)
    db.commit()
    return redirect(url_for('addresses'))

@app.route('/remove-address/<addr_id>', methods=['POST'])
def remove_address(addr_id=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    db.execute('delete from address where addr_id=\'%s\'' % addr_id)
    db.commit()
    return redirect(url_for('addresses'))

@app.route('/remove-attraction/<attr_id>', methods=['POST'])
def remove_attraction(attr_id=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    db.execute('delete from attraction where attr_id=\'%s\'' % attr_id)
    db.commit()
    return redirect(url_for('attractions'))

@app.route('/remove-trip/<conf_num>', methods=['POST'])
def remove_trip(conf_num=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    db.execute('delete from trip where conf_num=\'%s\'' % conf_num)
    db.commit()
    return redirect(url_for('trips'))

@app.route('/view-trip/<conf_num>', methods=['GET'])
def view_trip(conf_num=None):
    db = get_db()
    cur = db.execute('select activity_id, start_datetime, end_datetime, cost, attr_id from activity where conf_num=\'%s\'' % conf_num)
    entries = cur.fetchall()
    newentries = []
    for entry in entries:
        cur = db.execute('select name from attraction where attr_id=\'%s\'' % entry[4])
        entry += cur.fetchone()
        newentries.append(entry)
    return render_template('activities.html', entries=newentries, conf_num=conf_num)

@app.route('/remove-activity/<conf_num>/<activity_id>', methods=['POST'])
def remove_activity(conf_num=None, activity_id=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    db.execute('delete from activity where activity_id=\'%s\'' % activity_id)
    db.commit()
    return redirect(url_for('view_trip', conf_num=conf_num))

@app.route('/add-attraction', methods=['POST'])
def add_attraction():
    if not session['logged_in']:
        abort(401)
    db = get_db()
    test = [request.form['name'], request.form['description'], 0 if request.form.get('monday')==None else 1, request.form['opening'], request.form['closing'], request.form['cost'], 0 if request.form.get('reserve')==None else 1, request.form['address']]
    db.execute('insert into attraction (name, description, day_of_week, opening_time, closing_time, cost, reserve_compulsory, addr_id) values (?, ?, ?, ?, ?, ?, ?, ?)',
                 test)
    db.commit()
    return redirect(url_for('attractions'))

@app.route('/create-activity/<attr_id>/<conf_num>')
def create_activity(attr_id=None, conf_num=None):
    if not session['logged_in']:
        abort(401)
    return render_template('create-activity.html', attr_id=attr_id, conf_num=conf_num)

@app.route('/add-activity/<attr_id>/<conf_num>', methods=['POST'])
def add_activity(attr_id=None, conf_num=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    test = [request.form['start'], request.form['end'], conf_num, 0, attr_id, request.form['num']]
    db.execute('insert into activity (start_datetime, end_datetime, conf_num, cost, attr_id, num_in_party) values (?, ?, ?, ?, ?, ?)',
                 test)
    db.commit()
    return redirect(url_for('view_trip', conf_num=conf_num))

def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(app.config['DATABASE'])
    return g.db

if __name__ == '__main__':
    app.run(debug=True)