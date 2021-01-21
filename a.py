from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_mail import Mail
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)

mail = Mail(app)
app = Flask(__name__)
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Contacts(db.Model):
    # '''
    # Sl_no, fname, lname, email,feedback
    # '''
    Sl_no = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    email = db.Column(db.String(20))
    feedback = db.Column(db.String(120))


@app.route("/")
def home():
    return render_template('my5th.html')


@app.route("/my5th.html")
def home1():
    return render_template('my5th.html')


@app.route("/about.html")
def about():
    return render_template('about.html')


@app.route("/Services.html")
def Services():
    return render_template('Services.html')


@app.route("/Contact.html")
def Contact():
    return render_template('Contact.html')


@app.route("/Feedback.html", methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        add = request.form
        first_name = add["first_name"]
        last_name = add['last_name']
        Email = add['Email']
        Subject = add['Subject']
        entry = Contacts(fname=first_name, lname=last_name,
                         email=Email, feedback=Subject)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + first_name,
                          sender=Email,
                          recipients=[params['gmail-user']],
                          body=Subject + "\n" + first_name
                          )
    return render_template('Feedback.html', params=params)


if __name__ == '__main__':
    app.run()
