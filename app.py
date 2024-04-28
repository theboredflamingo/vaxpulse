import csv
from flask import Flask, render_template, request, redirect, url_for, jsonify 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
import random
from flask_login import UserMixin
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#app name
app = Flask(__name__)

#email smtp server details
smtp_server = 'smtp.office365.com'
smtp_port = 587
email_address = 'vaxpulse@outlook.com'
password = '2024PVS$'

#postgreSQL database details
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Stuthi0312@localhost:5432/vaxpulse'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'stuthiabcdefghi'
db = SQLAlchemy(app)

#Databases for the app
class newvaxlist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    age = db.Column(db.Integer(), nullable=False)
    vaccines = db.Column(db.String(80), nullable=False )

class userdetailsfin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable = False, unique=True)
    date_of_birth = db.Column(db.DateTime())

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(120), unique=True, nullable=False)

with app.app_context():
    db.create_all()

#Database population function, used once
def populate_vaccine_data():
  with app.app_context():
    with open('vaccine_data.csv', 'r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        age = int(row['Age'])
        vaccines = row['Vaccine'].split(' ')
        new_vaccine = newvaxlist(age=age, vaccines=','.join(vaccines))
        db.session.add(new_vaccine)
    db.session.commit()

#To calculate age given date of birth
def calculate_age(dob):
    today = datetime.now()
    if isinstance(dob, str):
        dob = datetime.strptime(dob, "%Y-%m-%d")
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

#To generate vaccine schedule from csv file
def generate_vaccine_schedule_from_csv(dob):
    age = calculate_age(dob)
    schedule_completed = []
    schedule_remaining = []

    with open('vaccine_data.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            i = int(row['Age'])
            if i <= age:
                age_date = datetime.strptime(dob, "%Y-%m-%d") + timedelta(days=365 * i)
                age_date_str = age_date.strftime("%Y-%m-%d")
                row["Date"] = age_date_str
                schedule_completed.append(row)
            elif i <= 18:
                age_date = datetime.strptime(dob, "%Y-%m-%d") + timedelta(days=365 * i)
                age_date_str = age_date.strftime("%Y-%m-%d")
                row["Date"] = age_date_str
                schedule_remaining.append(row)
    return schedule_completed, schedule_remaining

# App routes to all pages
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')

@app.route('/redirect')
def redirect_page():
    return redirect(url_for('index'))

# Vax Schedule Generation and Current Vaccines Retrieval Function
@app.route('/process_form', methods=['POST'])
def process_form():
  if 'button1' in request.form:
    if request.method == 'POST':
        name = request.form.get('name')
        dob_str = request.form.get('dob')
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        new_user = userdetailsfin(name=name, date_of_birth=dob)
        db.session.add(new_user)
        db.session.commit()
        print("done")
        age = calculate_age(dob)
        vaccine_row = newvaxlist.query.filter_by(age=age).first()
        return render_template('index.html', vaccine_row=vaccine_row)
    return "Current Vaccines Generated"
  elif 'button2' in request.form:
    if request.method == 'POST':
        name = request.form.get('name')
        dob = request.form['dob']
        age = calculate_age(dob)
        vaccine_schedule1, vaccine_schedule2 = generate_vaccine_schedule_from_csv(dob)
        return render_template('index.html', dob=dob, age=age, name=name, vaccine_schedule1=vaccine_schedule1, vaccine_schedule2=vaccine_schedule2)
    return render_template('index.html', dob=None, age=None, vaccine_schedule=None)
  else:
    return "Error: No button selected!"

# Subscribers function
@app.route('/subscriber', methods=['GET','POST'])
def subscriber():
    if request.method == 'POST':
       try:
        email = request.form['email']
        new_email = Email(email_address=email)
        db.session.add(new_email)
        db.session.commit()
        message = MIMEMultipart()
        message['From'] = email_address
        message['Subject'] = 'VaxPulse Subscription Confirmation'
        message['To'] = email
        body = 'Thank you for subscribing with us! Your health, simplified.'
        message.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, password)
        server.send_message(message)
        server.quit()
        print("New Subscriber Added, check spam folder")
        return render_template('index.html')
       except IntegrityError:
        db.session.rollback()
        return render_template('index.html', message="Email already exists, try with a different email")            
    else:
        return render_template('index.html')

#unused but retained functions
vaccine_data = {}
#to split the csv file into a dictionary
with open('vaccine_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        age = int(row['Age'])
        vaccines = row['Vaccine'].split(' ')
        vaccine_data[age] = vaccines

dataset_path = 'BLR-BBMP.csv'
hospital_data = pd.read_csv(dataset_path)

#to get the hospitals based on the location
@app.route('/get_hospitals', methods=['POST'])
def get_hospitals():
    location = request.form.get('location')
    filtered_hospitals = hospital_data[hospital_data['Zone'].str.contains(location, case=False)]
    return filtered_hospitals.to_json(orient='records')

#to get the vaccines based on the age
@app.route('/vaccines', methods=['POST'])
def vaccines():
    age = int(request.form.get('age'))
    if age not in vaccine_data:
        return render_template('error.html', message='No vaccines found for the specified age.')
    vaccines_list = vaccine_data[age]
    return render_template('vaccine_list.html', age=age, vaccines=vaccines_list)


#final call
if __name__ == '__main__':
    app.run(debug=True)

