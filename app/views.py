import mysql.connector
import string
import random
import hashlib
import time
import os
from flask import render_template, flash, redirect, g, session, abort, request
from random import randrange
from app import app
from app.forms import LoginForm, SigupForm, VerCode
from login import fuck_bilibili

def connect_db():
    # 仅用作测试, 不定时DROP一次
    return mysql.connector.connect(host='114.215.137.141', port=3306, user='test', password='123456', database='test')

def md5Password(password, salt0 = '', salt1 = ''):
    dic = string.ascii_letters + string.digits

    if '' == salt0 and '' == salt1:
        salt0 = ''.join(random.sample(dic, 3))
        salt1 = ''.join(random.sample(dic, 7))

    password = salt0 + password
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))

    password = password + salt1
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))

    return md5.hexdigest(), salt0, salt1

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title = 'Home')

@app.route('/sigup', methods=['GET', 'POST'])
def sigup():
    if session.get('bisLogin'):
        flash('You have login in bilibili!')
        return redirect('/go')

    if session.get('isLogin'):
        flash('You have login!')
        return redirect('/blogin')

    form = SigupForm()
    if form.validate_on_submit():
        username = form.username.data
        password0 = str(form.password0.data)
        password1 = str(form.password1.data)

        if password0 == password1:
            password, salt0, salt1 = md5Password(password1)
            cur = g.db.cursor()
            cur.execute("INSERT INTO user (username, password, salt0, salt1) VALUES ('%s', '%s', '%s', '%s')"
                                  % (username, password, salt0, salt1))
            g.db.commit()
            cur.close()
            flash('sigup success')
            return redirect('/login')
        else:
            flash('Bad password!')
    return render_template('sigup.html',
                           title = 'Sign up',
                           form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('bisLogin'):
        flash('You have login in bilibili!')
        return redirect('/go')

    form = LoginForm()
    if session.get('isLogin'):
        flash('You have login!')
        return redirect('/blogin')

    if form.validate_on_submit():
        username = form.username.data
        _password = str(form.password.data)
        print(_password)

        cur = g.db.cursor()
        cur.execute("SELECT password, salt0, salt1 FROM user WHERE username = '%s'" % username)
        try:
            res = cur.fetchall()[0]
            cur.close()
            password = res[0]
            salt0 = res[1]
            salt1 = res[2]
            _password = md5Password(_password, salt0, salt1)[0]
            if password == _password:
                flash('Login success')
                session['isLogin'] = True
                return redirect('/blogin')
            else:
                flash('Bad username or password')
        except:
            flash('Bad username or password')
    return render_template('login.html',
                           title = 'Sign in',
                           form = form)

@app.route('/logout')
def logout():
    session.pop('isLogin', None)
    session.pop('username', None)
    session.pop('password', None)
    session.pop('mySession', None)
    session.pop('bisLogin', None)
    flash('Logout success!')
    return redirect('login')

@app.route('/blogin', methods=['GET', 'POST'])
def blogin():
    if not session.get('isLogin'):
        abort(401)
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        session['username'] = username
        session['password'] = password

        return redirect('/go')
    return render_template('blogin.html',
                           title='Sign in',
                           form=form)

@app.route('/go', methods=['GET'])
def go_get():
    if not session.get('isLogin'):
        abort(401)

    try:
        fuck = fuck_bilibili(session['username'])
    except:
        flash('Please enter your BILIBILI account and password!')
        return redirect('/blogin')

    if fuck.loadCookies() and fuck.isLogin():
        flash('Welcome %s' % fuck.userData['data']['uname'])
        session['bisLogin'] = True
        return redirect('/index')
    else:
        fuck.initCookies()
        session['mySession'] = fuck.session.cookies.get_dict()

    if not fuck.rsaEncrypt(session['password']):
        flash('Can not get the key!')
        return redirect('/blogin')

    session['password'] = fuck.password

    if not fuck.getVerCode():
        flash('Can not get verify image!')
        return redirect('/blogin')

    form = VerCode()
    return render_template('blogin-go.html',
                           title='Sign in',
                           username=session['username'],
                           form=form)

@app.route('/go', methods=['POST'])
def go_post():
    if not session.get('isLogin'):
        abort(401)

    try:
        fuck = fuck_bilibili(session['username'], session['password'])
    except:
        flash('Please enter your BILIBILI account and password!')
        return redirect('/blogin')

    fuck.session.cookies.update(session['mySession'])

    form = VerCode()
    if form.is_submitted():
        if fuck.login(form.vercode.data) and fuck.isLogin():
            fuck.saveCookies()
            session['bisLogin'] = True

            try:
                cur = g.db.cursor()
                cur.execute("INSERT INTO buser (b_user, isQiandao) VALUES ('%s', '%s')"
                            % (session['username'], 0))
                g.db.commit()
                cur.close()
            except:
                flash("Username have exist!")

            flash('Welcome %s' % fuck.userData['data']['uname'])
        else:
            return redirect('/blogin')

    return redirect('/index')

@app.route('/img/<account>')
def img(account):
    filename = "./img/%s.jpg" % account
    with open(filename, 'rb') as f:
        res = app.make_response(f.read())
    res.headers['Content-Type'] = 'image / jpeg'
    return res

@app.route('/qiandao')
def qiandao():
    cur = g.db.cursor()
    curentTime = time.localtime(time.time())
    if 0 == curentTime.tm_hour and 0 == curentTime.tm_min and 0 == curentTime.tm_sec:
        cur.execute("UPDATE buser SET isQiandao = 0 WHERE isQiandao = 1")
        g.db.commit()
        cur.close()
        flash("finish")
        return redirect('/index')

    cur.execute("SELECT b_user FROM buser WHERE isQiandao = 0")
    try:
        res = cur.fetchall()
        num = randrange(0, len(res))
        username = res[num][0]

        fuck = fuck_bilibili(username)
        fuck.loadCookies()
        if not fuck.isLogin():
            filename = "./cookies/%s.cookies" % username
            os.remove(filename)
            cur.execute("DELETE FROM buser WHERE b_user = '%s'" % username)
        else:
            fuck.qiandao()
            cur.execute("UPDATE buser SET isQiandao = 1 WHERE b_user = '%s'" % username)
        flash("finish")
    except:
        flash("all finish")
    g.db.commit()
    cur.close()
    return redirect('/index')
