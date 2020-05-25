from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class IndexForm(FlaskForm):
    image_list = TextAreaField('Images', validators=[DataRequired()])
    submit = SubmitField('Send images')
