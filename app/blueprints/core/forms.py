from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=1, max=200, message="Title must be between 1 and 200 characters")
    ])
    content = TextAreaField('Content', validators=[
        DataRequired(),
        Length(min=1, max=10000, message="Content must be between 1 and 10000 characters")
    ])
    is_completed = BooleanField('Mark as completed')
    submit = SubmitField('Save Note')

class UploadForm(FlaskForm):
    file = FileField('File', validators=[
        FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'], 'File type not allowed!')
    ])
    submit = SubmitField('Upload')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')