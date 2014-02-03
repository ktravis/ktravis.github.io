"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# views
app.add_url_rule('/admin', 'admin', view_func=views.admin, methods=['GET', 'POST'])

app.add_url_rule('/', 'projects', view_func=views.projects)
app.add_url_rule('/about', 'about', view_func=views.about)
app.add_url_rule('/blog', 'blog', view_func=views.blog)
app.add_url_rule('/post/<int:post_id>/edit', 'edit_entry', view_func=views.edit_entry, methods=['POST'])
app.add_url_rule('/post/add', 'add_entry', view_func=views.add_entry, methods=['POST'])
app.add_url_rule('/post/<int:post_id>/del', 'del_entry', view_func=views.del_entry, methods=['POST'])
app.add_url_rule('/post/<string:post_slug>', 'show_post', view_func=views.show_post)


## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

