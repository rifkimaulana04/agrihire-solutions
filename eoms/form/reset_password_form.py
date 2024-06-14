from wtforms import Form, PasswordField, validators, EmailField
from eoms.form.registration_form import EmailValidator

class ResetPasswordForm(Form):
    email = EmailField(
        'Email Address',
        validators=[
            validators.DataRequired(),
            validators.Email(),
            EmailValidator()
        ]
    )

class ResetPasswordConfirmForm(Form):
    password = PasswordField(
        'Password',
        validators=[
            validators.DataRequired(),
            validators.Regexp('^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).*$',
                              message='Password should include number, uppercase letter, lowercase letter and special character.')
            ]
    )
    confirm = PasswordField(
        'Confirm Password',
        validators=[
            validators.DataRequired(),
            validators.EqualTo('password', message='Passwords must match.')
        ]
    )
