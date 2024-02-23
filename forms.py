from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField(label="", validators=[DataRequired()],
                       render_kw={"placeholder": "Entrez votre Pseudo"})
    password = PasswordField(label="", validators=[DataRequired()],
                             render_kw={"placeholder": "Entrez votre Passcode"})
    submit = SubmitField("Creer Compte")


class LoginForm(FlaskForm):
    name = StringField(label="", validators=[DataRequired()],
                       render_kw={"placeholder": "Entrez votre Pseudo"})
    password = PasswordField(label="", validators=[DataRequired()],
                             render_kw={"placeholder": "Entrez votre Passcode"})
    submit = SubmitField("Se connecter")
