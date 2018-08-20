import checkdmarc
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'
bootstrap = Bootstrap(app)


class CheckDmarcForm(FlaskForm):
    domain = StringField('Domain', validators=[Required()])
    submit = SubmitField('Submit')


@app.route("/", methods=['GET', 'POST'])
def check():
    form = CheckDmarcForm()
    domains = []
    results = []
    if form.validate_on_submit():
        nameservers = ['8.8.8.8.', '8.8.4.4']
        domains.append(form.domain.data)
        form.domain.data = None

        results = checkdmarc.check_domains(domains, nameservers=nameservers)

    return render_template('check.html',
                           form=form, results=results)
