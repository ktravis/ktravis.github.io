"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect, abort

from flask_cache import Cache

from application import app
from decorators import login_required, admin_required, templated, stubbable
from forms import EntryForm
from models import EntryModel
from urllib import quote
from time import strftime
from pytz.gae import pytz
from markdown import markdown

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)

def make_slug(title):
    return quote(title.replace(" ", "-"), safe="%/:=&?~#+!$,;'@()*[]")

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    user_tz = pytz.timezone('US/Pacific-New')
    value = value.replace(tzinfo=pytz.utc).astimezone(user_tz)
    return value.strftime(format)

def nice_time(value):
    sep = datetimeformat(value, "%A, %b %d at %I %p").split(' ')
    sep[2] = sep[2].lstrip('0')
    sep[4] = sep[4].lstrip('0')
    return ' '.join(sep).lower()

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['nice_time'] = nice_time

# @app.template_filter('nice_time')
# def time_filter(s):
#     converted = strptime(s, '%Y-%m-%d %H:%M:%S')
#     print converted
#     sep = strftime('%A, %b %d at %I %p', converted).split(' ')
#     sep[2] = sep[2].lstrip('0')
#     sep[4] = sep[4].lstrip('0')
#     print ' '.join(sep).lower() + "==============="
#     return "TEST"

# @app.template_filter('short_date')
# def date_filter(s):
#     converted = strptime(s, '%Y-%m-%d %H:%M:%S')
#     return strftime('%m/%d/%y', converted)


@templated('projects.html')
@stubbable
def projects():
    return { }

@templated('about.html')
@stubbable
def about():
    return { }

@templated('show_entries.html')
@stubbable
def blog():
    entries = EntryModel.query().order(-EntryModel.timestamp)

    form = None
    if users.is_current_user_admin():
        form = EntryForm()
    return { 'entries' : entries, 'form' : form }

@templated('show_post.html')
@stubbable
def show_post(post_slug):
    post = EntryModel.query(EntryModel.slug == post_slug).get()
    if not post:
        return render_template('404.html'), 404
    form = None
    if users.is_current_user_admin():
        form = EntryForm(obj=post)
    return { 'post' : post, 'form' : form }

@admin_required
def edit_entry(post_id):
    post = EntryModel.get_by_id(post_id)

    if not post:
        return render_template('404.html'), 404
    form = EntryForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = markdown(form.text.data)
        post.slug = make_slug(post.title)
        try:
            post.put()
        except CapabilityDisabledError:
            flash(u'Read-only mode.')
    return redirect(url_for('projects'))

@admin_required
def add_entry():
    form = EntryForm()
    if form.validate_on_submit():
        post = EntryModel(
            title=form.title.data,
            text=markdown(form.text.data),
            slug=make_slug(form.title.data)
        )
        try:
            post.put()
        except CapabilityDisabledError:
            flash(u'Read-only mode.')
    return redirect(url_for('projects'))

@admin_required
def del_entry(post_id):
    EntryModel.get_by_id(post_id).key.delete()
    return redirect(url_for('projects'))

@templated("admin.html")
@stubbable
def admin():
    return {
        'logged_in' : users.is_current_user_admin(),
        'login_url' : users.create_login_url('/')
        }

# @login_required
# def list_examples():
#     """List all examples"""
#     examples = ExampleModel.query()
#     form = ExampleForm()
#     if form.validate_on_submit():
#         example = ExampleModel(
#             example_name=form.example_name.data,
#             example_description=form.example_description.data,
#             added_by=users.get_current_user()
#         )
#         try:
#             example.put()
#             example_id = example.key.id()
#             flash(u'Example %s successfully saved.' % example_id, 'success')
#             return redirect(url_for('list_examples'))
#         except CapabilityDisabledError:
#             flash(u'App Engine Datastore is currently in read-only mode.', 'info')
#             return redirect(url_for('list_examples'))
#     return render_template('list_examples.html', examples=examples, form=form)


# @login_required
# def edit_example(example_id):
#     example = ExampleModel.get_by_id(example_id)
#     form = ExampleForm(obj=example)
#     if request.method == "POST":
#         if form.validate_on_submit():
#             example.example_name = form.data.get('example_name')
#             example.example_description = form.data.get('example_description')
#             example.put()
#             flash(u'Example %s successfully saved.' % example_id, 'success')
#             return redirect(url_for('list_examples'))
#     return render_template('edit_example.html', example=example, form=form)


# @login_required
# def delete_example(example_id):
#     """Delete an example object"""
#     example = ExampleModel.get_by_id(example_id)
#     try:
#         example.key.delete()
#         flash(u'Example %s successfully deleted.' % example_id, 'success')
#         return redirect(url_for('list_examples'))
#     except CapabilityDisabledError:
#         flash(u'App Engine Datastore is currently in read-only mode.', 'info')
#         return redirect(url_for('list_examples'))


# @admin_required
# def admin_only():
#     """This view requires an admin account"""
#     return 'Super-seekrit admin page.'


# @cache.cached(timeout=60)
# def cached_examples():
#     """This view should be cached for 60 sec"""
#     examples = ExampleModel.query()
#     return render_template('list_examples_cached.html', examples=examples)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

