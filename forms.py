from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField(label="", validators=[DataRequired()],
                       render_kw={"placeholder": "Entrez votre Pseudo"})
    password = PasswordField(label="", validators=[DataRequired()],
                             render_kw={"placeholder": "Entrez votre Passcode"})
    submit = SubmitField("Créer Compte")


class LoginForm(FlaskForm):
    name = StringField(label="", validators=[DataRequired()],
                       render_kw={"placeholder": "Entrez votre Pseudo"})
    password = PasswordField(label="", validators=[DataRequired()],
                             render_kw={"placeholder": "Entrez votre Passcode"})
    submit = SubmitField("Se connecter")

import pytz
# from datetime import datetime
# now = datetime.now()
# print(f"Current time: {now.strftime('%I:%M %p')}")
# # Get a list of all time zones
# all_timezones = pytz.all_timezones
#
# # Iterate through the time zones and find the one that matches your current time
# for tz in all_timezones:
#     try:
#         local_tz = pytz.timezone(tz)
#         local_time = local_tz.localize(now)
#         if local_time.strftime('%I:%M %p') == now.strftime('%I:%M %p'):
#             print(f"Your local time zone is: {tz}")
#             break
#     except pytz.exceptions.NonExistentTimeError:
#         # Ignore time zones that don't have the current time
#         pass
# else:
#     print("Unable to determine your local time zone.")