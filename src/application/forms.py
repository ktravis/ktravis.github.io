"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form

from .models import EntryModel


class EntryForm(wtf.Form):
	title = wtf.TextField('title', validators=[validators.Required()])
	text = wtf.TextAreaField('text', validators=[validators.Required()])

# EntryForm = model_form(EntryModel, wtf.Form, field_args={
# 		'title': dict(validators=[validators.Required()]),
#     	'text': dict(validators=[validators.Required()]),
# 	})

# class ClassicExampleForm(wtf.Form):
#     example_name = wtf.TextField('Name', validators=[validators.Required()])
#     example_description = wtf.TextAreaField('Description', validators=[validators.Required()])