import os
import pymysql
from time import strftime
import datetime
from flask import Flask, request, render_template, redirect, url_for, session, g, abort

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE='team4',
    SECRET_KEY='development key'
))

@app.route('/trips')
def trips():
    db = get_db()
    cur = db.cursor()
    cur.execute('select conf_num, name, city, start_date, end_date, total_cost, booked from trip where username=\'%s\'' % session['username'])
    entries = cur.fetchall()
    return render_template('trips.html', entries=entries)

@app.route('/attractions')
@app.route('/attractions/<conf_num>')
def attractions(conf_num=None):
    db = get_db()
    cur = db.cursor()
    cur.execute('select attr_id, name, description, opening_time, closing_time, cost, reserve_compulsory, trans_name, addr_id from attraction')
    entries = cur.fetchall()
    cur.execute('select addr_id, num, street, city, state, zip, country from address')
    addresses = cur.fetchall()
    cur.execute('select trans_name, addr_id from public_transportation')
    trans = cur.fetchall()
    addrs = []
    for address in addresses:
        addrs.append((address[0], str(address[1])+' '+address[2]+', '+address[3]+', '+address[4]+', '+str(address[5])+', '+address[6]))
    newentries = []
    for entry in entries:
        entry += ([a[1] for a in addrs if a[0] == entry[8]][0],)
        newentries.append(entry)
    return render_template('attractions.html', entries=newentries, conf_num=conf_num, addrs=addrs, trans=trans)

@app.route('/addresses')
def addresses():
    db = get_db()
    cur = db.cursor()
    cur.execute('select addr_id, num, street, city, state, zip, country from address')
    entries = cur.fetchall()
    return render_template('addresses.html', entries=entries)

@app.route('/users')
def users():
    db = get_db()
    cur = db.cursor()
    cur.execute('select username, first_name, last_name, email, is_admin, blocked from user')
    entries = cur.fetchall()
    return render_template('users.html', entries=entries)

@app.route('/credit-cards/<conf_num>')
def credit_cards(conf_num=None):
    db = get_db()
    cur = db.cursor()
    cur.execute('select ccnumber, first_name, last_name, expiry, cvv, username, addr_id from credit_card where username=\'%s\'' % session['username'])
    entries = cur.fetchall()
    cur.execute('select addr_id, num, street, city, state, zip, country from address')
    addresses = cur.fetchall()
    addrs = []
    for address in addresses:
        addrs.append((address[0], str(address[1])+' '+address[2]+', '+address[3]+', '+address[4]+', '+str(address[5])+', '+address[6]))
    newentries = []
    for entry in entries:
        entry += ([a[1] for a in addrs if a[0] == entry[6]][0],)
        newentries.append(entry)
    return render_template('credit-cards.html', entries=newentries, conf_num=conf_num, addrs=addrs)

@app.route('/transports')
def transports():
    db = get_db()
    cur = db.cursor()
    cur.execute('select trans_name, addr_id from public_transportation')
    entries = cur.fetchall()
    cur.execute('select addr_id, num, street, city, state, zip, country from address')
    addresses = cur.fetchall()
    addrs = []
    for address in addresses:
        addrs.append((address[0], str(address[1])+' '+address[2]+', '+address[3]+', '+address[4]+', '+str(address[5])+', '+address[6]))
    newentries = []
    for entry in entries:
        entry += ([a[1] for a in addrs if a[0] == entry[1]][0],)
        newentries.append(entry)
    return render_template('transports.html', entries=newentries, addrs=addrs)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db = get_db()
        cur = db.cursor()
        cur.execute('select username, is_admin from user where username=\'%s\' and password=\'%s\''
            % (request.form['username'], request.form['password']))
        check = cur.fetchall()
        if check == ():
            error = 'Invalid username or password'
        else:
            print(check)
            username, is_admin = check[0]
            session['logged_in'] = True
            session['username'] = username
            session['is_admin'] = True if is_admin else False
            return redirect(url_for('trips'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['username'] = None
    session['password'] = None
    return redirect(url_for('login'))

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
    cur = db.cursor()
    test = (request.form['name'], request.form['startdate'], request.form['enddate'], 0, request.form['city'], session['username'], 0)
    cur.execute('insert into trip (name, start_date, end_date, booked, city, username, total_cost) values (%s, %s, %s, %s, %s, %s, %s)',
                 test)
    db.commit()
    return redirect(url_for('trips'))

@app.route('/add-transport', methods=['POST'])
def add_transport():
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    test = (request.form['name'], request.form['address'])
    cur.execute('insert into public_transportation (trans_name, addr_id) values (%s, %s)',
                 test)
    db.commit()
    return redirect(url_for('transports'))

@app.route('/add-address', methods=['POST'])
def add_address():
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    test = (request.form['num'], request.form['street'], request.form['city'], request.form['state'], request.form['zip'], request.form['country'])
    cur.execute('insert into address (num, street, city, state, zip, country) values (%s, %s, %s, %s, %s, %s)',
                 test)
    db.commit()
    return redirect(url_for('addresses'))

@app.route('/add-user', methods=['POST'])
def add_user():
    db = get_db()
    cur = db.cursor()
    test = (request.form['username'], request.form['password'], request.form['first'], request.form['last'], request.form['email'], 0 if request.form.get('admin')==None else 1, 0)
    cur.execute('insert into user (username, password, first_name, last_name, email, is_admin, blocked) values (%s, %s, %s, %s, %s, %s, %s)', test)
    db.commit()
    return redirect(url_for('users'))

@app.route('/add-card/<conf_num>', methods=['POST'])
def add_card(conf_num=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    test = (request.form['num'], request.form['first'], request.form['last'], request.form['expiry'], request.form['cvv'], request.form['address'], session['username'])
    cur.execute('insert into credit_card (ccnumber, first_name, last_name, expiry, cvv, addr_id, username) values (%s, %s, %s, %s, %s, %s, %s)',
                 test)
    db.commit()
    return redirect(url_for('credit_cards', conf_num=conf_num))

@app.route('/remove-address/<addr_id>', methods=['POST'])
def remove_address(addr_id=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    cur.execute('delete from address where addr_id=\'%s\'' % addr_id)
    db.commit()
    return redirect(url_for('addresses'))

@app.route('/remove-user/<username>', methods=['POST'])
def remove_user(username=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    cur.execute('delete from user where username=\'%s\'' % username)
    db.commit()
    return redirect(url_for('users'))

@app.route('/block-user/<username>', methods=['POST'])
def block_user(username=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    cur.execute('update user set blocked=1 where username=\'%s\'' % username)
    db.commit()
    return redirect(url_for('users'))

@app.route('/remove-transport/<trans_name>', methods=['POST'])
def remove_transport(trans_name=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    cur.execute('delete from public_transportation where trans_name=\'%s\'' % trans_name)
    db.commit()
    return redirect(url_for('transports'))

@app.route('/remove-attraction/<attr_id>', methods=['POST'])
def remove_attraction(attr_id=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    cur.execute('delete from attraction where attr_id=\'%s\'' % attr_id)
    db.commit()
    return redirect(url_for('attractions'))

@app.route('/remove-trip/<conf_num>', methods=['POST'])
def remove_trip(conf_num=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    cur.execute('delete from trip where conf_num=\'%s\'' % conf_num)
    db.commit()
    return redirect(url_for('trips'))

@app.route('/view-trip/<conf_num>', methods=['GET'])
def view_trip(conf_num=None):
    db = get_db()
    cur = db.cursor()
    cur.execute('select activity_id, start_datetime, end_datetime, cost, attr_id, num_in_party from activity where conf_num=\'%s\'' % conf_num)
    entries = cur.fetchall()
    newentries = []
    for entry in entries:
        cur.execute('select name from attraction where attr_id=\'%s\'' % entry[4])
        entry += cur.fetchone()
        newentries.append(entry)
    return render_template('activities.html', entries=newentries, conf_num=conf_num)

@app.route('/remove-activity/<conf_num>/<activity_id>', methods=['POST'])
def remove_activity(conf_num=None, activity_id=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    cur.execute('select total_cost from trip where conf_num=\'%s\'' % conf_num)
    total_cost = cur.fetchall()[0][0]
    cur.execute('select cost, num_in_party, attr_id, start_datetime from activity where activity_id=\'%s\'' % activity_id)
    cost, num_in_party, attr_id, starttime = cur.fetchall()[0]
    total_cost -= cost
    cur.execute('update trip set total_cost=%s where conf_num=\'%s\'' % (total_cost, conf_num))
    db.commit()
    cur.execute('select start_datetime, quantity from time_slot where attr_id=\'%s\'' % attr_id)
    slots = cur.fetchall()
    if slots != None:
        try:
            stime = datetime.datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%S')
        except:
            stime = datetime.datetime.strptime(starttime, '%Y-%m-%dT%H:%M')
        for start_datetime, quantity in slots:
            margin = datetime.timedelta(minutes = 59)
            low = stime - margin
            high = stime + margin
            if (low <= datetime.datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S') <= high):
                sdt = start_datetime
                newquantity = quantity + num_in_party
                cur.execute('update time_slot set quantity=\'%s\' where start_datetime=\'%s\'' % (newquantity, sdt))
                db.commit()
    cur.execute('delete from activity where activity_id=\'%s\'' % activity_id)
    db.commit()
    return redirect(url_for('view_trip', conf_num=conf_num))

@app.route('/add-attraction', methods=['POST'])
def add_attraction():
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    ohr, omin = request.form['opening'].split(":")
    days = str('Monday' if request.form.get('monday')!=None else "") + ' ' + str('Tuesday' if request.form.get('tuesday')!=None else "") + ' ' + str('Wednesday' if request.form.get('wednesday')!=None else "") + ' ' + str('Thursday' if request.form.get('thursday')!=None else "") + ' ' + str('Friday' if request.form.get('friday')!=None else "") + ' ' + str('Saturday' if request.form.get('saturday')!=None else "") + ' ' + str('Sunday' if request.form.get('sunday')!=None else "")
    test = (request.form['name'], request.form['description'], days, request.form['opening'], request.form['closing'], request.form['cost'], 0 if request.form.get('reserve')==None else 1, request.form['address'], None if request.form['trans'] == "0" else request.form['trans'])
    cur.execute('insert into attraction (name, description, days_open, opening_time, closing_time, cost, reserve_compulsory, addr_id, trans_name) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                 test)
    db.commit()
    cur.execute('select last_insert_id() from attraction')
    attr_id = cur.fetchall()[0][0]
    print(attr_id)
    if request.form.get('reserve') != None:
        opening = int(ohr)*60 + int(omin)
        clhr, clmin = request.form['closing'].split(":")
        closing = int(clhr)*60 + int(clmin)
        slot_intervals = range(opening, closing, int(request.form['slots']))
        for i in range(0, len(slot_intervals)-1):
            start = slot_intervals[i]
            end = slot_intervals[i+1]
            for i in range(0, 7):
                today = datetime.date.today()
                sdate = datetime.datetime(today.year, today.month, today.day, int(start/60), start%60, 0)
                edate = datetime.datetime(today.year, today.month, today.day, int(end/60), end%60, 0)
                test = (str(sdate + datetime.timedelta(days=i)), str(edate + datetime.timedelta(days=i)), int(request.form['quantity']), attr_id)
                cur.execute('insert into time_slot (start_datetime, end_datetime, quantity, attr_id) values (%s, %s, %s, %s)', test)
    db.commit()
    return redirect(url_for('attractions'))

@app.route('/create-activity/<attr_id>/<conf_num>')
def create_activity(attr_id=None, conf_num=None):
    if not session['logged_in']:
        abort(401)
    return render_template('create-activity.html', attr_id=attr_id, conf_num=conf_num)

@app.route('/book-trip/<conf_num>')
def book_trip(conf_num=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    cur.execute('select total_cost, booked from trip where conf_num=\'%s\'' % conf_num)
    total_cost, booked = cur.fetchall()[0]
    if total_cost == 0 or booked == 1:
        cur.execute('update trip set booked=1 where conf_num=\'%s\'' % conf_num)
        db.commit()
        return redirect(url_for('trips'))
    cur.execute('select ccnumber from credit_card where username=\'%s\'' % session['username'])
    cards = cur.fetchall()
    return render_template('book-trip.html', conf_num=conf_num, cards=cards)

@app.route('/pay-trip/<conf_num>')
def pay_trip(conf_num=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    cur.execute('update trip set booked=1 where conf_num=\'%s\'' % conf_num)
    db.commit()
    return redirect(url_for('trips'))

@app.route('/review-attraction/<attr_id>')
def review_attraction(attr_id=None):
    if not session['logged_in']:
        abort(401)
    return render_template('review-attraction.html', attr_id=attr_id)

@app.route('/view-attraction/<attr_id>', methods=['GET'])
def view_attraction(attr_id=None):
    db = get_db()
    cur = db.cursor()
    cur.execute('select date_time, title, body, username from review where attr_id=\'%s\'' % attr_id)
    entries = cur.fetchall()
    return render_template('view-attraction.html', entries=entries, attr_id=attr_id)

@app.route('/add-activity/<attr_id>/<conf_num>', methods=['POST'])
def add_activity(attr_id=None, conf_num=None):
    if not session['logged_in']:
        abort(401)
    try:
        stime = datetime.datetime.strptime(request.form['start'], '%Y-%m-%dT%H:%M:%S')
    except:
        stime = datetime.datetime.strptime(request.form['start'], '%Y-%m-%dT%H:%M')
    try:
        etime = datetime.datetime.strptime(request.form['end'], '%Y-%m-%dT%H:%M:%S')
    except:
        etime = datetime.datetime.strptime(request.form['end'], '%Y-%m-%dT%H:%M')
    if etime <= stime:
        return render_template('create-activity.html', attr_id=attr_id, conf_num=conf_num)
    db = get_db()
    cur = db.cursor()
    cur.execute('select cost, opening_time, closing_time, reserve_compulsory from attraction where attr_id=\'%s\'' % attr_id)
    cost, opening_time, closing_time, reserve_compulsory = cur.fetchall()[0]
    opening_time = int(opening_time.split(":")[0]) * 60 + int(opening_time.split(":")[1])
    closing_time = int(closing_time.split(":")[0]) * 60 + int(closing_time.split(":")[1])
    if (stime.hour * 60 + stime.minute) < opening_time or (etime.hour * 60 + etime.minute) > closing_time:
        return render_template('create-activity.html', attr_id=attr_id, conf_num=conf_num)
    cur.execute('select start_datetime, quantity from time_slot where attr_id=\'%s\'' % attr_id)
    slots = cur.fetchall()
    noslotfound = True
    if slots != None:
        for start_datetime, quantity in slots:
            margin = datetime.timedelta(minutes = 59)
            low = stime - margin
            high = stime + margin
            if (low <= datetime.datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S') <= high):
                noslotfound = False
                if quantity - int(request.form['num']) < 0:
                    return render_template('create-activity.html', attr_id=attr_id, conf_num=conf_num)
                else:
                    sdt = start_datetime
                    newquantity = quantity - int(request.form['num'])
                    cur.execute('update time_slot set quantity=\'%s\' where start_datetime=\'%s\'' % (newquantity, sdt))
                    db.commit()
    if noslotfound and reserve_compulsory:
        return render_template('create-activity.html', attr_id=attr_id, conf_num=conf_num)
    cur.execute('select start_date, end_date from trip where conf_num=\'%s\'' % conf_num)
    start_date, end_date = cur.fetchall()[0]
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days = 1)
    if stime < start_date or etime > end_date:
        return render_template('create-activity.html', attr_id=attr_id, conf_num=conf_num)
    cur.execute('select start_datetime, end_datetime from activity')
    times = cur.fetchall()
    if times != ():
        for start_datetime, end_datetime in times:
            try:
                if (datetime.datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M:%S') <= stime <= datetime.datetime.strptime(end_datetime, '%Y-%m-%dT%H:%M:%S') or datetime.datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M:%S') <= etime <= datetime.datetime.strptime(end_datetime, '%Y-%m-%dT%H:%M:%S')):
                    return render_template('create-activity.html', attr_id=attr_id, conf_num=conf_num)
            except:
                if (datetime.datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M') <= stime <= datetime.datetime.strptime(end_datetime, '%Y-%m-%dT%H:%M') or datetime.datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M') <= etime <= datetime.datetime.strptime(end_datetime, '%Y-%m-%dT%H:%M')):
                    return render_template('create-activity.html', attr_id=attr_id, conf_num=conf_num)
    cost = cost * int(request.form['num'])
    test = (request.form['start'], request.form['end'], conf_num, cost, attr_id, request.form['num'])
    cur.execute('insert into activity (start_datetime, end_datetime, conf_num, cost, attr_id, num_in_party) values (%s, %s, %s, %s, %s, %s)',
                 test)
    db.commit()
    cur.execute('select total_cost from trip where conf_num=\'%s\'' % conf_num)
    total_cost = cur.fetchall()[0][0]
    total_cost += cost
    cur.execute('update trip set total_cost=%s where conf_num=\'%s\'' % (total_cost, conf_num))
    db.commit()
    return redirect(url_for('view_trip', conf_num=conf_num))

@app.route('/add-review/<attr_id>', methods=['POST'])
def add_review(attr_id=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    test = (strftime("%Y-%m-%dT%H:%M:%S"), request.form['title'], request.form['body'], session['username'], attr_id)
    cur.execute('insert into review (date_time, title, body, username, attr_id) values (%s, %s, %s, %s, %s)',
                 test)
    db.commit()
    return redirect(url_for('view_attraction', attr_id=attr_id))

@app.route('/remove-review/<date_time>/<attr_id>', methods=['POST'])
def remove_review(date_time=None, attr_id=None):
    if not session['logged_in']:
        abort(401)
    db = get_db()
    cur = db.cursor()
    db.execute('delete from review where date_time=\'%s\'' % date_time)
    db.commit()
    return redirect(url_for('view_attraction', attr_id=attr_id))

def get_db():
    if not hasattr(g, 'db'):
        g.db = pymysql.connect(host='localhost', port=3306, user='root', passwd='smoothie42', db=app.config['DATABASE'])
    return g.db

if __name__ == '__main__':
    app.run(debug=True)