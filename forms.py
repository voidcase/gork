from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, ValidationError, Length, NumberRange
from wtforms.fields import StringField, PasswordField, FloatField
from werkzeug.security import check_password_hash

from config import *
from gorkdata import User

def username_free(form, field):
    if User.get_or_none(User.name == field.data) != None:
        raise ValidationError('Username is already taken.')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    
    def authenticated(self):
        alleged_user = User.get_or_none(User.name == self.username.data)
        return (
                alleged_user != None
                and check_password_hash(alleged_user.password_hash, self.password.data)
                )


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), username_free])
    email = StringField('email', validators=[InputRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=PW_MIN_LENGTH)])

class PosForm(FlaskForm):
    lat = FloatField('lat',validators=[InputRequired()])
    lon = FloatField('lon',validators=[InputRequired()])
    acc = FloatField('acc',validators=[
        InputRequired(),
        NumberRange(max=100, message="You don't know where you are."),
        ])
    
    def pos(self) -> tuple:
        return (self.lat.data, self.lon.data)

