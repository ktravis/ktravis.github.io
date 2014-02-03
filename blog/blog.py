from functools import wraps
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, jsonify, make_response
from urllib import quote
from time import strftime, strptime, mktime, localtime

# config
# ======
CONFIG_FILE = "config"

app = Flask(__name__)
app.config.from_object(CONFIG_FILE)
# ======


# db management
# =============
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
# =============


# helpers
# =======
def make_slug(title):
    return quote(title.replace(" ", "-"), safe="%/:=&?~#+!$,;'@()*[]")

@app.template_filter('nice_time')
def time_filter(s):
    converted = localtime(mktime(strptime(s, '%Y-%m-%d %H:%M:%S')))
    sep = strftime('%A, %b %d at %I %p', converted).split(' ')
    sep[2] = sep[2].lstrip('0')
    sep[4] = sep[4].lstrip('0')
    return ' '.join(sep).lower()

@app.template_filter('short_date')
def date_filter(s):
    converted = strptime(s, '%Y-%m-%d %H:%M:%S')
    return strftime('%m/%d/%y', converted)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
# =======


# views
# =====
def stubbable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ctx = f(*args, **kwargs)
        if ctx is None:
            ctx = {}
        elif isinstance(ctx, dict):
            ctx['stub'] = request.args.get('stub', False)
        return ctx
    return decorated_function

def templated(template):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator

@app.route('/')
@templated('projects.html')
@stubbable
def projects():
    return { }

@app.route('/about')
@templated('about.html')
@stubbable
def about():
    return { }

@app.route('/blog')
@templated('show_entries.html')
@stubbable
def show_entries():
    cur = g.db.execute('select title, text, slug, timestamp, id from entries order by id desc')
    entries = [dict(title=row[0], text=row[1], slug=row[2], time=row[3], id=row[4]) for row in cur.fetchall()]
    return { 'entries' : entries }

@app.route('/post/<string:post_slug>')
@templated('show_post.html')
@stubbable
def show_post(post_slug):
    cur = g.db.execute('select title, text, timestamp, id from entries where slug=?',
                        [post_slug])
    post = cur.fetchall()
    if not post:
        return render_template('404.html'), 404
    post = {    'title'  : post[0][0],
                'text'   : post[0][1],
                'time'   : post[0][2],
                'id'     : post[0][3], }
    return { 'post' : post }

@app.route('/post/edit', methods=['POST'])
def edit_entry():
    if not session.get('logged_in'):
                abort(401)
    g.db.execute('update entries set title=?, text=? where id=?',
                 [request.form['title'], request.form['text'], int(request.form['id'])])
    g.db.commit()
    return redirect(url_for('projects'))

@app.route('/post/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
                abort(401)
    g.db.execute('insert into entries (title, text, slug) values (?, ?, ?)',
                 [request.form['title'], request.form['text'], make_slug(request.form['title'])])
    g.db.commit()
    return redirect(url_for('show_entries'))

@app.route('/post/del', methods=['POST'])
def del_entry():
    if not session.get('logged_in'):
                abort(401)
    g.db.execute('delete from entries where id=?',
                 [request.form['id']])
    g.db.commit()
    return redirect(url_for('show_entries'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect(url_for('projects'))
    return render_template('admin.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('projects'))
# =====


if __name__ == '__main__':
    app.run()
