from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    blood_group = db.Column(db.String(5))
    genotype = db.Column(db.String(5))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    diagnosis = db.Column(db.String(200))
    treatment = db.Column(db.String(200))
    doctor_name = db.Column(db.String(100))
    notes = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)